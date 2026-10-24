// Package dashboard owns ordinary-user management lifetime and presentation
// transport, not storage policy. No administrative filesystem work runs in HTTP.
package dashboard

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"errors"
	"io"
	"net"
	"net/http"
	"os"
	"runtime"
	"sync"
	"time"

	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
)

type Operation struct {
	ID          string             `json:"id"`
	RequestID   uint64             `json:"requestId"`
	Kind        string             `json:"kind"`
	State       string             `json:"state"`
	StartedAt   time.Time          `json:"startedAt"`
	CompletedAt *time.Time         `json:"completedAt,omitempty"`
	Data        json.RawMessage    `json:"data,omitempty"`
	Error       *adminwire.Failure `json:"error,omitempty"`
}
type Submission struct {
	ID      uint64          `json:"id"`
	Kind    string          `json:"kind"`
	Payload json.RawMessage `json:"payload"`
}
type Snapshot struct {
	Role       string     `json:"role"`
	Platform   string     `json:"platform"`
	Home       string     `json:"home"`
	Authorized bool       `json:"authorized"`
	Closing    bool       `json:"closing"`
	Operation  *Operation `json:"operation,omitempty"`
}
type Session struct {
	mu                                      sync.Mutex
	role, home, host, origin, secret, token string
	launch                                  Launcher
	log                                     io.Writer
	helper                                  *helper
	operation                               *Operation
	fingerprint                             [32]byte
	closing                                 bool
	workers                                 sync.WaitGroup
	listener                                net.Listener
	http                                    *http.Server
	stop                                    chan struct{}
	stopOnce                                sync.Once
	bootstrap                               string
	directories                             directorySlot
}

func secret() string {
	var b [32]byte
	if _, err := rand.Read(b[:]); err != nil {
		panic(err)
	}
	return base64.RawURLEncoding.EncodeToString(b[:])
}
func New(role string, launch Launcher) (*Session, error) {
	if os.Geteuid() == 0 {
		return nil, errors.New("dashboard must run as an ordinary user, not under sudo")
	}
	if role != "server" && role != "client" {
		return nil, errors.New("unknown dashboard role")
	}
	home, err := os.UserHomeDir()
	if err != nil {
		return nil, err
	}
	listener, err := net.Listen("tcp4", "127.0.0.1:0")
	if err != nil {
		return nil, err
	}
	s := &Session{role: role, home: home, host: listener.Addr().String(), secret: secret(), launch: launch, log: io.Discard, listener: listener, stop: make(chan struct{})}
	s.origin = "http://" + s.host
	s.http = &http.Server{Handler: http.NewCrossOriginProtection().Handler(http.HandlerFunc(s.serve)), ReadHeaderTimeout: 5 * time.Second, ReadTimeout: 10 * time.Second, WriteTimeout: 10 * time.Second, IdleTimeout: 30 * time.Second, MaxHeaderBytes: 8 << 10}
	return s, nil
}
func (s *Session) snapshot() Snapshot {
	s.mu.Lock()
	defer s.mu.Unlock()
	v := Snapshot{Role: s.role, Platform: runtime.GOOS, Home: s.home, Closing: s.closing, Authorized: s.helper != nil && s.helper.alive()}
	if s.operation != nil {
		copy := *s.operation
		v.Operation = &copy
	}
	return v
}
func (s *Session) submit(request Submission) (Operation, error) {
	if request.ID == 0 {
		return Operation{}, errors.New("request id is required")
	}
	if request.Kind == "authorize" {
		var empty struct{}
		if err := adminwire.Decode(request.Payload, &empty); err != nil {
			return Operation{}, err
		}
	} else {
		if request.Kind == "close" {
			return Operation{}, errors.New("use stop dashboard")
		}
		if _, err := adminwire.Input(adminwire.Request{Kind: request.Kind, Payload: request.Payload}); err != nil {
			return Operation{}, err
		}
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	fingerprint := sha256.Sum256(append([]byte(request.Kind), request.Payload...))
	if s.closing {
		return Operation{}, errors.New("dashboard is stopping")
	}
	if s.operation != nil {
		if request.ID == s.operation.RequestID && fingerprint == s.fingerprint {
			return *s.operation, nil
		}
		if request.ID <= s.operation.RequestID {
			return Operation{}, errors.New("stale or conflicting request; refresh state")
		}
		if s.operation.State == "running" {
			return Operation{}, errors.New("operation still running; restore storage and wait")
		}
	}
	if request.Kind != "authorize" && (s.helper == nil || !s.helper.alive()) {
		return Operation{}, errors.New("authorize administration in the terminal first")
	}
	if request.Kind == "authorize" && s.helper != nil && s.helper.alive() {
		return Operation{}, errors.New("already authorized")
	}
	operation := Operation{ID: secret(), RequestID: request.ID, Kind: request.Kind, State: "running", StartedAt: time.Now()}
	s.operation = &operation
	s.fingerprint = fingerprint
	s.workers.Add(1)
	go s.perform(request)
	return operation, nil
}
func (s *Session) perform(request Submission) {
	defer s.workers.Done()
	var reply adminwire.Reply
	var err error
	if request.Kind == "authorize" {
		if s.helper != nil {
			s.helper.close()
		}
		var child *helper
		child, err = authorize(s.launch, s.role, s.log)
		s.mu.Lock()
		s.helper = child
		s.mu.Unlock()
		// Authorization reads metadata, never probes readiness or mutates storage.
		if err == nil {
			reply, err = child.call("inspect", json.RawMessage(`{}`))
		}
	} else {
		reply, err = s.helper.call(request.Kind, request.Payload)
	}
	if err != nil && s.helper != nil {
		s.helper.close()
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	now := time.Now()
	s.operation.CompletedAt = &now
	s.operation.Data = reply.Data
	s.operation.Error = reply.Error
	s.operation.State = "succeeded"
	if err != nil {
		s.operation.Error = &adminwire.Failure{Code: "disconnected", Detail: "Administrative connection failed; outcome may be incomplete. Reopen and inspect before retry.", EffectsMayHaveStarted: request.Kind == "commit" || request.Kind == "authorize"}
	}
	if s.operation.Error != nil {
		s.operation.State = "incomplete"
	}
}
func (s *Session) Stop() {
	s.stopOnce.Do(func() { s.mu.Lock(); s.closing = true; s.mu.Unlock(); close(s.stop) })
}

// Drain is called after HTTP shutdown. It does not cancel committed host work.
func (s *Session) Drain() {
	s.Stop()
	s.workers.Wait()
	if s.helper != nil {
		s.helper.close()
	}
	s.removeBootstrap()
	s.mu.Lock()
	s.token = ""
	s.secret = ""
	s.mu.Unlock()
}
