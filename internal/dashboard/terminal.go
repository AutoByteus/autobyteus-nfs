package dashboard

import (
	"fmt"
	"io"
	"sync"
	"time"
)

const (
	approvalWaiting     = "Waiting for administrator approval and setup helper. Complete any approval prompt only in this terminal."
	approvalReminder    = "Still waiting for administrator approval or helper startup. Check this terminal for an approval prompt or diagnostic; do not start a second attempt."
	controlsPreparing   = "Administrator access confirmed.\nPreparing setup controls—reading saved configuration…"
	controlsReminder    = "Still reading saved configuration. Keep this terminal open; do not start another attempt."
	controlsReady       = "Dashboard ready—continue in your browser. Keep this terminal open. If needed, use the private URL above.\nSetup controls are ready; this has not created a share, connected storage or checked storage readiness."
	helperStartFailed   = "Could not start the administrator helper. Reopen this command as an ordinary user in an interactive terminal and authorize again; review the terminal diagnostic."
	approvalUnconfirmed = "Administrator access was not confirmed. Approval may have been denied/cancelled or the helper failed to start. Review the terminal diagnostic, then reopen and authorize again."
	controlsDraining    = "Setup controls could not be initialized. Waiting for the helper to finish safely; do not retry yet."
	controlsUnavailable = "Setup controls unavailable. Reopen the dashboard and inspect configuration before deciding how to retry."
	inspectionRefused   = "Administrator access is confirmed, but saved configuration could not be read. Review the dashboard error and use Inspect configuration before retrying setup."
)

// terminalFeedback is a disposable presentation sink, not operation state. Session
// calls phase/stop under Session.mu; this sink never calls back into Session.
// All parent output shares this lock. OS approval diagnostics remain untouched.
type terminalFeedback struct {
	mu         sync.Mutex
	writer     io.Writer
	after      func(time.Duration, func()) func()
	cancel     func()
	generation uint64
	stopped    bool
}

func newTerminalFeedback() *terminalFeedback {
	return &terminalFeedback{writer: io.Discard, after: func(delay time.Duration, callback func()) func() {
		timer := time.AfterFunc(delay, callback)
		return func() { timer.Stop() }
	}}
}
func (f *terminalFeedback) setOutput(writer io.Writer) {
	f.mu.Lock()
	defer f.mu.Unlock()
	f.writer = writer
}
func (f *terminalFeedback) invalidate() {
	f.generation++
	if f.cancel != nil {
		f.cancel()
		f.cancel = nil
	}
}
func (f *terminalFeedback) phase(message, reminder string) {
	f.mu.Lock()
	defer f.mu.Unlock()
	if f.stopped {
		return
	}
	f.invalidate()
	fmt.Fprintln(f.writer, message)
	if reminder == "" {
		return
	}
	generation := f.generation
	f.cancel = f.after(10*time.Second, func() {
		f.mu.Lock()
		defer f.mu.Unlock()
		if !f.stopped && generation == f.generation {
			// Consume once, even if a test scheduler invokes the callback again.
			f.generation++
			f.cancel = nil
			fmt.Fprintln(f.writer, reminder)
		}
	})
}
func (f *terminalFeedback) stop() {
	f.mu.Lock()
	defer f.mu.Unlock()
	f.stopped = true
	f.invalidate()
}

// guidance suppresses asynchronous opener invitations after Stop. The initial
// private fallback is deliberately passed here once, never stored or repeated.
func (f *terminalFeedback) guidance(values ...any) {
	f.mu.Lock()
	defer f.mu.Unlock()
	if !f.stopped {
		fmt.Fprintln(f.writer, values...)
	}
}

// print remains available for stopping/drain messages after admission closes.
func (f *terminalFeedback) print(values ...any) {
	f.mu.Lock()
	defer f.mu.Unlock()
	fmt.Fprintln(f.writer, values...)
}
