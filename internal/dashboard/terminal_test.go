package dashboard

import (
	"bytes"
	"errors"
	"strings"
	"sync"
	"testing"
	"time"
)

type scheduledReminder struct {
	callback  func()
	cancelled bool
}
type manualReminders struct{ entries []*scheduledReminder }

func (m *manualReminders) after(delay time.Duration, callback func()) func() {
	if delay != 10*time.Second {
		panic("unexpected reminder delay")
	}
	entry := &scheduledReminder{callback: callback}
	m.entries = append(m.entries, entry)
	return func() { entry.cancelled = true }
}
func terminalText(f *terminalFeedback, b *bytes.Buffer) string {
	f.mu.Lock()
	defer f.mu.Unlock()
	return b.String()
}
func TestTerminalReminderGenerationAndStop(t *testing.T) {
	f := newTerminalFeedback()
	var b bytes.Buffer
	f.setOutput(&b)
	clock := &manualReminders{}
	f.after = clock.after
	f.phase(approvalWaiting, approvalReminder)
	old := clock.entries[0]
	f.phase(controlsPreparing, controlsReminder)
	if !old.cancelled {
		t.Fatal("phase failed to cancel previous timer")
	}
	old.callback()
	current := clock.entries[1]
	current.callback()
	current.callback()
	text := terminalText(f, &b)
	if strings.Contains(text, approvalReminder) || strings.Count(text, controlsReminder) != 1 {
		t.Fatal(text)
	}
	f.phase(approvalWaiting, approvalReminder)
	pending := clock.entries[2]
	f.stop()
	before := terminalText(f, &b)
	pending.callback()
	f.phase(controlsReady, "")
	f.guidance("late opener invitation")
	if !pending.cancelled || terminalText(f, &b) != before {
		t.Fatal("post-stop invitation/reminder")
	}
	f.print("drained")
	if !strings.HasSuffix(terminalText(f, &b), "drained\n") {
		t.Fatal("shutdown output missing")
	}
}
func TestTerminalConcurrentOutputAndStop(t *testing.T) {
	f := newTerminalFeedback()
	var b bytes.Buffer
	f.setOutput(&b)
	clock := &manualReminders{}
	f.after = clock.after
	f.phase(approvalWaiting, approvalReminder)
	callback := clock.entries[0].callback
	var workers sync.WaitGroup
	for i := 0; i < 100; i++ {
		workers.Add(1)
		go func() { defer workers.Done(); f.guidance("opener"); callback() }()
	}
	f.stop()
	afterStop := terminalText(f, &b)
	workers.Wait()
	if terminalText(f, &b) != afterStop {
		t.Fatal("output after Stop returned")
	}
	for _, line := range strings.Split(strings.TrimSpace(afterStop), "\n") {
		if line != approvalWaiting && line != approvalReminder && line != "opener" {
			t.Fatal("interleaved output", line)
		}
	}
}

type brokenTerminal struct{}

func (brokenTerminal) Write([]byte) (int, error) { return 0, errors.New("terminal unavailable") }
func TestTerminalWriteFailureDoesNotControlOperation(t *testing.T) {
	s, _ := testDashboard(t)
	s.terminal.setOutput(brokenTerminal{})
	if _, err := s.submit(Submission{ID: 1, Kind: "authorize", Payload: []byte(`{}`)}); err != nil {
		t.Fatal(err)
	}
	waitFeedback(t, func() bool { return s.snapshot().Operation.State != "running" })
	if s.snapshot().Operation.State != "succeeded" {
		t.Fatal(s.snapshot())
	}
}
