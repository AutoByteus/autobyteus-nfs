package admin

import (
	"context"
	"encoding/json"
	"errors"
	"io"
	"time"

	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
)

// ServePipe has one reader and at most one administrative worker. EOF, signal
// or EPIPE closes admission then drains the worker before releasing its scope.
// The caller closes input on exit so the sole reader cannot outlive the helper.
func (s *Session) ServePipe(ctx context.Context, in io.Reader, out io.Writer) error {
	defer s.Close()
	hello, _ := json.Marshal(adminwire.Hello{Role: s.role, Digest: s.digest})
	if err := adminwire.Write(out, adminwire.Reply{Version: adminwire.Version, Kind: "hello", Data: hello}, adminwire.ReplyLimit); err != nil {
		return err
	}
	requests := make(chan adminwire.Request)
	readErr := make(chan error, 1)
	stopped := make(chan struct{})
	defer close(stopped)
	go func() {
		scanner := adminwire.NewReader(in, adminwire.RequestLimit)
		var last uint64
		for scanner.Scan() {
			var request adminwire.Request
			if err := adminwire.Decode(scanner.Bytes(), &request); err != nil {
				readErr <- err
				return
			}
			if request.Version != adminwire.Version || request.ID == 0 || request.ID <= last {
				readErr <- errors.New("invalid protocol version or repeated request")
				return
			}
			if _, err := adminwire.Input(request); err != nil {
				readErr <- err
				return
			}
			last = request.ID
			select {
			case requests <- request:
			case <-stopped:
				return
			}
		}
		err := scanner.Err()
		if err == nil {
			err = io.EOF
		}
		readErr <- err
	}()
	finished := make(chan adminwire.Reply, 1)
	running := false
	idle := time.NewTimer(15 * time.Minute)
	defer idle.Stop()
	drain := func() {
		if running {
			<-finished
		}
	}
	for {
		select {
		case <-ctx.Done():
			drain()
			return ctx.Err()
		case err := <-readErr:
			drain()
			if err == io.EOF {
				return nil
			}
			return err
		case <-idle.C:
			if !running {
				return nil
			}
		case request := <-requests:
			if running {
				drain()
				return errors.New("overlapping administrative requests")
			}
			if request.Kind == "close" {
				var empty struct{}
				if err := adminwire.Decode(request.Payload, &empty); err != nil {
					return err
				}
				return nil
			}
			running = true
			idle.Stop()
			go func() { finished <- s.dispatch(request) }()
		case reply := <-finished:
			running = false
			if err := adminwire.Write(out, reply, adminwire.ReplyLimit); err != nil {
				return err
			}
			if reply.Error != nil && reply.Error.Code == "invalid-request" {
				return errors.New("invalid administrative request")
			}
			idleFor := 15 * time.Minute
			s.mu.Lock()
			if s.lease != nil {
				idleFor += time.Until(s.lease.expires)
			}
			s.mu.Unlock()
			idle.Reset(idleFor)
		}
	}
}
func (s *Session) dispatch(request adminwire.Request) adminwire.Reply {
	reply := adminwire.Reply{Version: adminwire.Version, ID: request.ID, Kind: request.Kind}
	input, err := adminwire.Input(request)
	if err != nil {
		reply.Error = &adminwire.Failure{Code: "invalid-request", Detail: "invalid administrative request"}
		return reply
	}
	var data any
	switch request.Kind {
	case "beginServer":
		data, err = s.BeginServer(*input.(*adminwire.ServerInput))
	case "beginClient":
		data, err = s.BeginClient(*input.(*adminwire.ClientInput))
	case "commit":
		data, err = s.Commit(*input.(*adminwire.CommitInput))
	case "cancelReview":
		err = s.CancelReview(input.(*adminwire.LeaseInput).LeaseID)
	case "inspect":
		data, err = s.InspectConfiguration()
	case "checkReadiness":
		data, err = s.CheckReadiness()
	case "beginReconnect":
		data, err = s.BeginReconnect()
	case "beginDetach":
		data, err = s.BeginDetach()
	}
	if data != nil {
		reply.Data, _ = json.Marshal(data)
	}
	if err != nil {
		detail := err.Error()
		truncated := len(detail) > 4096
		if truncated {
			detail = detail[:4096]
		}
		effects := false
		if result, ok := data.(adminwire.Result); ok {
			effects = result.EffectsMayHaveStarted
		}
		reply.Error = &adminwire.Failure{Code: "refused-or-incomplete", Detail: detail, Truncated: truncated, EffectsMayHaveStarted: effects}
	}
	return reply
}
