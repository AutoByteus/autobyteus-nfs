// Package admin owns the complete locked administrative sequence for terminal,
// private-pipe and installed-service entry forms. It never serves HTTP.
package admin

import (
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"io"
	"os"
	"sync"
	"time"

	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/docker"
	"github.com/AutoByteus/autobyteus-nfs/internal/platform"
	"github.com/AutoByteus/autobyteus-nfs/internal/setup"
)

const reviewLifetime = 5 * time.Minute

type lease struct {
	id, kind string
	expires  time.Time
	plan     setup.Plan
	service  *setup.Service
	timer    *time.Timer
}

type Session struct {
	mu     sync.Mutex
	closed bool
	base   setup.Service
	role   string // empty for preserved terminal/service entry forms
	digest string
	lease  *lease
	// Mechanism seams are private; production callers cannot override admission,
	// paths, locking, execution or identity through the administrative API.
	admit      func(string, string) error
	runner     func(*os.File) platform.Runner
	openDocker func(string) (*docker.Client, error)
	wait       func() <-chan time.Time
}

func New(release setup.Release, user setup.User, role string) (*Session, error) {
	if os.Geteuid() != 0 {
		return nil, errors.New("administration requires OS approval")
	}
	if role != "" && role != "server" && role != "client" {
		return nil, errors.New("invalid administrative role")
	}
	binary := config.BinaryPath()
	if err := platform.TrustedPath(binary, false); err != nil {
		return nil, err
	}
	if err := platform.RootDirectory(config.PrivateDirectory(), 0700); err != nil {
		return nil, err
	}
	executable, err := os.Executable()
	if err != nil {
		return nil, err
	}
	digest, err := Digest(executable)
	if err != nil {
		return nil, err
	}
	if err = admitBinary(binary, digest); err != nil {
		return nil, err
	}
	return &Session{base: setup.Service{Store: config.Store{Directory: config.PrivateDirectory(), Owner: 0}, Binary: binary, Release: release, User: user}, role: role, digest: digest, admit: admitBinary, runner: func(lock *os.File) platform.Runner { return platform.Commands{Lock: lock} }, openDocker: docker.New, wait: func() <-chan time.Time { return time.After(30 * time.Second) }}, nil
}

func Digest(path string) (string, error) {
	f, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer f.Close()
	info, err := f.Stat()
	if err != nil {
		return "", err
	}
	if !info.Mode().IsRegular() || info.Size() > 100<<20 {
		return "", errors.New("invalid control executable")
	}
	h := sha256.New()
	if _, err = io.Copy(h, io.LimitReader(f, 100<<20+1)); err != nil {
		return "", err
	}
	return hex.EncodeToString(h.Sum(nil)), nil
}
func admitBinary(binary, digest string) error {
	if err := platform.TrustedPath(binary, false); err != nil {
		return err
	}
	current, err := Digest(binary)
	if err != nil {
		return err
	}
	if current != digest {
		return errors.New("control binary changed; close and authorize again")
	}
	return nil
}

// Each operation acquires once; setup and its children receive this exact lock.
func (s *Session) acquire() (*setup.Service, error) {
	if s.closed {
		return nil, errors.New("administrative session is closed")
	}
	if s.lease != nil {
		return nil, errors.New("review already reserves storage management")
	}
	lock, err := platform.Lock(s.base.Store.Directory)
	if err != nil {
		return nil, err
	}
	service := s.base
	service.Lock = lock
	service.Runner = s.runner(lock)
	service.Docker = nil
	if err = config.CheckStandaloneState(service.Store); err == nil {
		err = s.admit(service.Binary, s.digest)
	}
	if err != nil {
		closeScope(&service)
		return nil, err
	}
	return &service, nil
}
func closeScope(service *setup.Service) {
	if service.Docker != nil {
		service.Docker.Close()
		service.Docker = nil
	}
	if service.Lock != nil {
		service.Lock.Close()
		service.Lock = nil
	}
}
func (s *Session) savedDocker(service *setup.Service) {
	var endpoint struct {
		Socket string `json:"socket"`
	}
	// Preserve existing saved-daemon behavior: operations that require it report
	// unavailable from their authoritative setup check; status may not need it.
	if service.Store.Read("docker-endpoint.json", &endpoint) == nil && endpoint.Socket != "" {
		service.Docker, _ = s.openDocker(endpoint.Socket)
	}
}
func (s *Session) enter() error {
	if !s.mu.TryLock() {
		return errors.New("administrative operation is still running")
	}
	if s.closed {
		s.mu.Unlock()
		return errors.New("administrative session is closed")
	}
	return nil
}
func (s *Session) releaseReview() {
	if s.lease != nil {
		s.lease.timer.Stop()
		closeScope(s.lease.service)
		s.lease = nil
	}
}

// Close drains a running operation; it never cancels a mount or releases the
// operation's inherited lock early. Only uncommitted review is cancelled.
func (s *Session) Close() { s.mu.Lock(); defer s.mu.Unlock(); s.closed = true; s.releaseReview() }
