package dashboard

import (
	"bytes"
	"errors"
	"os/exec"
	"strings"
	"testing"
	"time"

	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
)

func feedbackSession(t *testing.T, role, mode string) (*Session, *bytes.Buffer, feedbackChild) {
	t.Helper()
	child := newFeedbackChild(t, role, mode)
	s, err := New(role, child.launch)
	if err != nil {
		t.Fatal(err)
	}
	var log bytes.Buffer
	s.terminal.setOutput(&log)
	t.Cleanup(func() {
		child.hello.Close()
		child.inspect.Close()
		child.finish.Close()
		s.listener.Close()
		s.Drain()
	})
	return s, &log, child
}
func startFeedback(t *testing.T, s *Session, id uint64) {
	t.Helper()
	if _, err := s.submit(Submission{ID: id, Kind: "authorize", Payload: []byte(`{}`)}); err != nil {
		t.Fatal(err)
	}
}
func requireFeedback(t *testing.T, text string, required ...string) {
	t.Helper()
	last := -1
	for _, message := range required {
		at := strings.Index(text, message)
		if at <= last {
			t.Fatalf("missing/out-of-order %q in %q", message, text)
		}
		last = at
	}
	for _, private := range []string{"PRIVATE_CONFIG_CANARY", "PRIVATE_ERROR_CANARY", "PRIVATE_START_CANARY", "PID", "Password accepted"} {
		if strings.Contains(text, private) {
			t.Fatal("private/misleading feedback", text)
		}
	}
}
func TestAuthorizationFeedbackBothRolesAndOutcomes(t *testing.T) {
	for _, role := range []string{"server", "client"} {
		for _, mode := range []string{"empty", "configured", "pending", "opposite-role", "refused", "denied", "digest", "role", "version", "lost"} {
			t.Run(role+"/"+mode, func(t *testing.T) {
				s, log, child := feedbackSession(t, role, mode)
				releaseFeedbackGate(t, child.hello)
				releaseFeedbackGate(t, child.inspect)
				startFeedback(t, s, 1)
				s.workers.Wait()
				text := terminalText(s.terminal, log)
				requireFeedback(t, text, approvalWaiting)
				unconfirmed := mode == "denied" || mode == "digest" || mode == "role" || mode == "version"
				failed := unconfirmed || mode == "refused" || mode == "lost"
				if failed != (s.snapshot().Operation.State == "incomplete") {
					t.Fatal(s.snapshot())
				}
				if unconfirmed {
					requireFeedback(t, text, approvalWaiting, approvalUnconfirmed)
					if strings.Contains(text, controlsPreparing) {
						t.Fatal(text)
					}
				} else {
					requireFeedback(t, text, approvalWaiting, controlsPreparing)
					switch mode {
					case "refused":
						requireFeedback(t, text, inspectionRefused)
					case "lost":
						requireFeedback(t, text, controlsDraining, controlsUnavailable)
					default:
						requireFeedback(t, text, controlsReady)
						if !strings.Contains(text, "Administrator access confirmed.") || !strings.Contains(text, "Dashboard ready—continue in your browser.") || !strings.Contains(text, "this has not created a share, connected storage or checked storage readiness") {
							t.Fatal("missing public success meaning", text)
						}
					}
				}
				if failed && strings.Contains(text, controlsReady) {
					t.Fatal("false ready", text)
				}
			})
		}
	}
}
func TestLocalHelperStartFailureCategory(t *testing.T) {
	original := errors.New("PRIVATE_START_CANARY")
	for _, mode := range []string{"launch", "stdin", "stdout", "start"} {
		t.Run(mode, func(t *testing.T) {
			launch := func() (*exec.Cmd, string, error) {
				if mode == "launch" {
					return nil, "", original
				}
				cmd := exec.Command("/nonexistent-feedback-helper")
				if mode == "stdin" {
					cmd.Stdin = strings.NewReader("")
				}
				if mode == "stdout" {
					cmd.Stdout = &bytes.Buffer{}
				}
				return cmd, "feedback-test", nil
			}
			_, err := authorize(launch, "server")
			var start *helperStartError
			if !errors.As(err, &start) || start.Unwrap() == nil {
				t.Fatal(err)
			}
			if mode == "launch" && !errors.Is(err, original) {
				t.Fatal("lost original error")
			}
			s, e := New("server", launch)
			if e != nil {
				t.Fatal(e)
			}
			defer s.listener.Close()
			defer s.Drain()
			var log bytes.Buffer
			s.terminal.setOutput(&log)
			startFeedback(t, s, 1)
			s.workers.Wait()
			requireFeedback(t, terminalText(s.terminal, &log), approvalWaiting, helperStartFailed)
		})
	}
}
func TestHeldPhasesDedupAndExplicitNewAttempt(t *testing.T) {
	s, log, child := feedbackSession(t, "client", "empty")
	startFeedback(t, s, 1)
	startFeedback(t, s, 1)
	if terminalText(s.terminal, log) != approvalWaiting+"\n" {
		t.Fatal("premature or duplicate feedback")
	}
	releaseFeedbackGate(t, child.hello)
	waitFeedback(t, func() bool { return strings.Contains(terminalText(s.terminal, log), controlsPreparing) })
	if strings.Contains(terminalText(s.terminal, log), controlsReady) {
		t.Fatal("ready before inspect")
	}
	releaseFeedbackGate(t, child.inspect)
	s.workers.Wait()
	s.helper.close() // actual expired child; a new explicit ID must get feedback again
	second := newFeedbackChild(t, "client", "empty")
	s.launch = second.launch
	releaseFeedbackGate(t, second.hello)
	releaseFeedbackGate(t, second.inspect)
	startFeedback(t, s, 2)
	s.workers.Wait()
	if strings.Count(terminalText(s.terminal, log), approvalWaiting) != 2 || strings.Count(terminalText(s.terminal, log), controlsReady) != 2 {
		t.Fatal(terminalText(s.terminal, log))
	}
}
func TestStopSuppressesFeedbackButDrainsAdmittedWork(t *testing.T) {
	for _, phase := range []string{"hello", "inspect", "cleanup"} {
		t.Run(phase, func(t *testing.T) {
			mode := "empty"
			if phase == "cleanup" {
				mode = "cleanup"
			}
			s, log, child := feedbackSession(t, "server", mode)
			startFeedback(t, s, 1)
			if phase != "hello" {
				releaseFeedbackGate(t, child.hello)
				waitFeedback(t, func() bool { return strings.Contains(terminalText(s.terminal, log), controlsPreparing) })
			}
			if phase == "cleanup" {
				releaseFeedbackGate(t, child.inspect)
				waitFeedback(t, func() bool { return strings.Contains(terminalText(s.terminal, log), controlsDraining) })
			}
			s.Stop()
			before := terminalText(s.terminal, log)
			done := make(chan struct{})
			go func() { s.Drain(); close(done) }()
			select {
			case <-done:
				t.Fatal("drain abandoned admitted child")
			case <-time.After(20 * time.Millisecond):
			}
			if phase == "hello" {
				releaseFeedbackGate(t, child.hello)
			}
			if phase != "cleanup" {
				releaseFeedbackGate(t, child.inspect)
			} else {
				releaseFeedbackGate(t, child.finish)
			}
			select {
			case <-done:
			case <-time.After(5 * time.Second):
				t.Fatal("drain did not finish")
			}
			if terminalText(s.terminal, log) != before {
				t.Fatal("late phase after Stop", terminalText(s.terminal, log))
			}
		})
	}
}
func TestInspectionCleanupPrecedesRetryGuidance(t *testing.T) {
	s, log, child := feedbackSession(t, "server", "cleanup")
	releaseFeedbackGate(t, child.hello)
	releaseFeedbackGate(t, child.inspect)
	startFeedback(t, s, 1)
	waitFeedback(t, func() bool { return strings.Contains(terminalText(s.terminal, log), controlsDraining) })
	if strings.Contains(terminalText(s.terminal, log), controlsUnavailable) || s.snapshot().Operation.State != "running" {
		t.Fatal("retry before drain")
	}
	releaseFeedbackGate(t, child.finish)
	s.workers.Wait()
	requireFeedback(t, terminalText(s.terminal, log), controlsPreparing, controlsDraining, controlsUnavailable)
}
func TestKnownDeadHelperCannotReportReady(t *testing.T) {
	s, log, child := feedbackSession(t, "client", "empty")
	releaseFeedbackGate(t, child.hello)
	releaseFeedbackGate(t, child.inspect)
	h, err := authorize(child.launch, "client")
	if err != nil {
		t.Fatal(err)
	}
	s.helper = h
	h.close()
	s.mu.Lock()
	s.authorizationFeedback(adminwire.Reply{}, nil)
	s.mu.Unlock()
	if text := terminalText(s.terminal, log); text != controlsUnavailable+"\n" {
		t.Fatal(text)
	}
}

func TestHeldApprovalTenSecondReminderIsNotAuthority(t *testing.T) {
	s, log, child := feedbackSession(t, "client", "empty")
	began := time.Now()
	startFeedback(t, s, 1)
	deadline := time.Now().Add(15 * time.Second)
	for !strings.Contains(terminalText(s.terminal, log), approvalReminder) && time.Now().Before(deadline) {
		time.Sleep(10 * time.Millisecond)
	}
	elapsed := time.Since(began)
	requireFeedback(t, terminalText(s.terminal, log), approvalWaiting, approvalReminder)
	if elapsed < 10*time.Second || s.snapshot().Authorized || s.snapshot().Operation.State != "running" {
		t.Fatal("timer changed authority", elapsed, s.snapshot())
	}
	t.Logf("actual held-hello reminder after %s; still running, not authorized", elapsed)
	releaseFeedbackGate(t, child.hello)
	releaseFeedbackGate(t, child.inspect)
	s.workers.Wait()
	requireFeedback(t, terminalText(s.terminal, log), approvalReminder, controlsPreparing, controlsReady)
	s.terminal.mu.Lock()
	defer s.terminal.mu.Unlock()
	if s.terminal.cancel != nil {
		t.Fatal("timer retained after completion")
	}
}
