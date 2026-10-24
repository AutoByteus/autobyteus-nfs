package admin

import (
	"context"
	"errors"
	"io"
	"os"
	"strings"
	"sync/atomic"
	"testing"
	"time"

	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/docker"
	"github.com/AutoByteus/autobyteus-nfs/internal/platform"
	"github.com/AutoByteus/autobyteus-nfs/internal/setup"
)

type runnerFunc func(string, ...string) ([]byte, error)

func (f runnerFunc) Run(p string, a ...string) ([]byte, error) { return f(p, a...) }
func testSession(t *testing.T) *Session {
	t.Helper()
	root := t.TempDir()
	if err := os.Chmod(root, 0700); err != nil {
		t.Fatal(err)
	}
	s := &Session{base: setup.Service{Store: config.Store{Directory: root, Owner: uint32(os.Getuid())}, Binary: "/usr/bin/false"}, admit: func(string, string) error { return nil }, runner: func(*os.File) platform.Runner {
		return runnerFunc(func(string, ...string) ([]byte, error) { return nil, errors.New("unexpected backend call") })
	}, openDocker: docker.New, wait: func() <-chan time.Time { return time.After(30 * time.Second) }}
	t.Cleanup(s.Close)
	return s
}
func attachment() config.Attachment {
	return config.Attachment{Connection: config.Connection{StorageID: "11111111-1111-4111-8111-111111111111", Endpoint: "192.168.8.10", Export: "/srv/project", Protocol: "3", MountRoot: "/Volumes/dashboard-test"}, InstallationID: "22222222-2222-4222-8222-222222222222", UserUID: uint32(os.Getuid()), UserGID: uint32(os.Getgid())}
}
func save(t *testing.T, s *Session, name string, value any) {
	t.Helper()
	if err := s.base.Store.Write(name, value); err != nil {
		t.Fatal(err)
	}
}
func unlocked(t *testing.T, s *Session) {
	t.Helper()
	f, err := platform.Lock(s.base.Store.Directory)
	if err != nil {
		t.Fatal("leaked administrative lock", err)
	}
	f.Close()
}
func TestScopeAdmissionLockAndCleanup(t *testing.T) {
	for _, fail := range []bool{false, true} {
		t.Run(map[bool]string{false: "success", true: "admission-failure"}[fail], func(t *testing.T) {
			s := testSession(t)
			s.admit = func(string, string) error {
				if lock, e := platform.Lock(s.base.Store.Directory); e == nil {
					lock.Close()
					t.Fatal("admission outside lock")
				}
				if fail {
					return errors.New("changed binary")
				}
				return nil
			}
			scope, err := s.acquire()
			if fail {
				if err == nil {
					t.Fatal("admission ignored")
				}
			} else {
				if err != nil {
					t.Fatal(err)
				}
				closeScope(scope)
				closeScope(scope)
			}
			unlocked(t, s)
		})
	}
	s := testSession(t)
	save(t, s, "pending-setup.json", map[string]any{"attachment": map[string]any{"nodes": []string{"old"}}})
	called := false
	s.admit = func(string, string) error { called = true; return nil }
	if _, err := s.acquire(); err == nil || called {
		t.Fatal("predecessor admission order", err, called)
	}
	unlocked(t, s)
}
func TestInspectIsMetadataOnlyAndRoleIsExplicit(t *testing.T) {
	s := testSession(t)
	c, err := s.InspectConfiguration()
	if err != nil || c.State != "empty" {
		t.Fatal(c, err)
	}
	a := attachment()
	save(t, s, "attachment.json", a)
	s.role = "server"
	c, err = s.InspectConfiguration()
	if err != nil || c.State != "configured" || c.Role != "client" {
		t.Fatal(c, err)
	}
	if _, err = s.BeginReconnect(); err == nil || !strings.Contains(err.Error(), "autobyteus-nfs client") {
		t.Fatal(err)
	}
	save(t, s, "pending-setup.json", setup.Plan{Attachment: a})
	c, err = s.InspectConfiguration()
	if err != nil || c.State != "pending" {
		t.Fatal(c, err)
	}
	unlocked(t, s)
}
func TestReviewCancelExpiryAndConsumedBeforeFailure(t *testing.T) {
	for _, mode := range []string{"cancel", "expiry", "timer", "commit"} {
		t.Run(mode, func(t *testing.T) {
			s := testSession(t)
			scope, err := s.acquire()
			if err != nil {
				t.Fatal(err)
			}
			r, err := s.retain(scope, "reconnect", setup.Plan{}, []string{"exact saved plan"}, adminwire.Configuration{State: "configured", Role: "client"})
			if err != nil {
				t.Fatal(err)
			}
			if lock, e := platform.Lock(s.base.Store.Directory); e == nil {
				lock.Close()
				t.Fatal("review lost lock")
			}
			if err = s.CancelReview("foreign"); err == nil {
				t.Fatal("foreign review accepted")
			}
			if _, err = s.Commit(adminwire.CommitInput{LeaseID: r.LeaseID}); err == nil {
				t.Fatal("missing consent")
			}
			switch mode {
			case "cancel":
				err = s.CancelReview(r.LeaseID)
			case "expiry":
				s.lease.expires = time.Now().Add(-time.Second)
				_, err = s.Commit(adminwire.CommitInput{LeaseID: r.LeaseID, Consent: true})
				if err == nil {
					t.Fatal("expired commit accepted")
				}
			case "timer":
				s.lease.timer.Reset(time.Millisecond)
				time.Sleep(30 * time.Millisecond)
			case "commit":
				_, err = s.Commit(adminwire.CommitInput{LeaseID: r.LeaseID, Consent: true})
				if err == nil {
					t.Fatal("missing state unexpectedly reconnected")
				}
			}
			if _, err = s.Commit(adminwire.CommitInput{LeaseID: r.LeaseID, Consent: true}); err == nil {
				t.Fatal("replay accepted")
			}
			unlocked(t, s)
		})
	}
}
func TestSupervisorBusyWaitAndPendingNeverResumes(t *testing.T) {
	s := testSession(t)
	save(t, s, "pending-setup.json", setup.Plan{Attachment: attachment()})
	before, _ := os.ReadFile(s.base.Store.Directory + "/pending-setup.json")
	var calls atomic.Int32
	s.runner = func(*os.File) platform.Runner {
		return runnerFunc(func(string, ...string) ([]byte, error) { calls.Add(1); return nil, errors.New("effect") })
	}
	ticks := make(chan time.Time)
	waiting := make(chan struct{}, 2)
	s.wait = func() <-chan time.Time { waiting <- struct{}{}; return ticks }
	lock, err := platform.Lock(s.base.Store.Directory)
	if err != nil {
		t.Fatal(err)
	}
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	done := make(chan error, 1)
	go func() { done <- s.Supervise(ctx, io.Discard) }()
	<-waiting
	if calls.Load() != 0 {
		t.Fatal("busy reached backend")
	}
	lock.Close()
	ticks <- time.Now()
	<-waiting
	if calls.Load() != 0 {
		t.Fatal("pending resumed")
	}
	cancel()
	if err = <-done; err != nil {
		t.Fatal(err)
	}
	after, _ := os.ReadFile(s.base.Store.Directory + "/pending-setup.json")
	if string(before) != string(after) {
		t.Fatal("pending changed")
	}
	unlocked(t, s)
}
func TestSupervisorStopDrainsOneInFlightAttempt(t *testing.T) {
	s := testSession(t)
	save(t, s, "attachment.json", attachment())
	entered := make(chan struct{})
	release := make(chan struct{})
	defer func() {
		select {
		case <-release:
		default:
			close(release)
		}
	}()
	var calls atomic.Int32
	// Shared admission runs under the operation lock on both OSes. Do not
	// depend on Darwin's command-based mount observation to pause Linux.
	s.admit = func(string, string) error {
		calls.Add(1)
		close(entered)
		<-release
		return errors.New("controlled admission failure")
	}
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	done := make(chan error, 1)
	go func() { done <- s.Supervise(ctx, io.Discard) }()
	select {
	case <-entered:
	case <-time.After(5 * time.Second):
		t.Fatal("attempt never reached shared admission")
	}
	cancel()
	select {
	case <-done:
		t.Fatal("did not drain")
	case <-time.After(20 * time.Millisecond):
	}
	if f, err := platform.Lock(s.base.Store.Directory); err == nil {
		f.Close()
		t.Fatal("lock released in flight")
	}
	close(release)
	if err := <-done; err != nil {
		t.Fatal(err)
	}
	if calls.Load() != 1 {
		t.Fatal(calls.Load())
	}
	unlocked(t, s)
}
func TestSupervisorAlreadyStoppedDoesNotAdmit(t *testing.T) {
	s := testSession(t)
	s.admit = func(string, string) error { t.Fatal("admitted stopped service"); return nil }
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	if err := s.Supervise(ctx, io.Discard); err != nil {
		t.Fatal(err)
	}
}
func TestSavedUserRetainsIdentityAndRejectsMissing(t *testing.T) {
	a := attachment()
	u, err := savedUser(a)
	if err != nil || u.UID != a.UserUID || u.GID != a.UserGID || u.Home == "" {
		t.Fatal(u, err)
	}
	a.UserUID = 0
	if _, err = savedUser(a); err == nil {
		t.Fatal("root substituted")
	}
}
