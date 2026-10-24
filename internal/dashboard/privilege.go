package dashboard

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os/exec"
	"sync"

	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
)

// Launcher supplies fixed process plumbing, never administrative callbacks.
type Launcher func() (*exec.Cmd, string, error)
type helper struct {
	mu         sync.Mutex
	cmd        *exec.Cmd
	input      io.WriteCloser
	output     io.ReadCloser
	replies    chan adminwire.Reply
	done       chan struct{}
	stopReader chan struct{}
	waitErr    error
	sequence   uint64
	closed     bool
}

func authorize(launch Launcher, role string, log io.Writer) (*helper, error) {
	cmd, digest, err := launch()
	if err != nil {
		return nil, err
	}
	input, err := cmd.StdinPipe()
	if err != nil {
		return nil, err
	}
	output, err := cmd.StdoutPipe()
	if err != nil {
		input.Close()
		return nil, err
	}
	if err = cmd.Start(); err != nil {
		input.Close()
		output.Close()
		return nil, err
	}
	fmt.Fprintf(log, "Administrator approval/helper process PID %d started. Confirm only in this terminal; stopping waits for safe completion.\n", cmd.Process.Pid)
	h := &helper{cmd: cmd, input: input, output: output, replies: make(chan adminwire.Reply, 2), done: make(chan struct{}), stopReader: make(chan struct{})}
	go h.receive()
	reply, err := h.read()
	if err == nil {
		var hello adminwire.Hello
		err = adminwire.Decode(reply.Data, &hello)
		if err == nil && (reply.Kind != "hello" || reply.ID != 0 || reply.Error != nil || hello.Role != role || hello.Digest != digest) {
			err = errors.New("helper identity differs; close and authorize again")
		}
	}
	if err != nil {
		h.close()
		return nil, err
	}
	return h, nil
}
func (h *helper) receive() {
	scanner := adminwire.NewReader(h.output, adminwire.ReplyLimit)
	for scanner.Scan() {
		var reply adminwire.Reply
		if err := adminwire.Decode(scanner.Bytes(), &reply); err != nil || reply.Version != adminwire.Version {
			h.waitErr = errors.New("invalid private helper reply")
			break
		}
		select {
		case h.replies <- reply:
		case <-h.stopReader:
		}
	}
	if err := scanner.Err(); err != nil {
		h.waitErr = err
	}
	h.input.Close()
	h.output.Close()
	err := h.cmd.Wait()
	if h.waitErr == nil {
		h.waitErr = err
	}
	close(h.replies)
	close(h.done)
}
func (h *helper) read() (adminwire.Reply, error) {
	reply, ok := <-h.replies
	if !ok {
		return reply, errors.New("administrator helper disconnected or approval failed; reconcile current state before retry")
	}
	return reply, nil
}
func (h *helper) alive() bool {
	select {
	case <-h.done:
		return false
	default:
		return true
	}
}
func (h *helper) call(kind string, payload json.RawMessage) (adminwire.Reply, error) {
	h.mu.Lock()
	defer h.mu.Unlock()
	if h.closed || !h.alive() {
		return adminwire.Reply{}, errors.New("administrator authorization expired")
	}
	h.sequence++
	req := adminwire.Request{Version: adminwire.Version, ID: h.sequence, Kind: kind, Payload: payload}
	if err := adminwire.Write(h.input, req, adminwire.RequestLimit); err != nil {
		return adminwire.Reply{}, err
	}
	reply, err := h.read()
	if err == nil && (reply.ID != req.ID || reply.Kind != kind) {
		err = errors.New("helper reply does not match operation")
	}
	return reply, err
}
func (h *helper) close() error {
	h.mu.Lock()
	defer h.mu.Unlock()
	if h.closed {
		return nil
	}
	h.closed = true
	close(h.stopReader)
	h.input.Close()
	<-h.done
	return h.waitErr
}
