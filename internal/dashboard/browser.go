package dashboard

import (
	"context"
	"html"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"time"
)

func (s *Session) removeBootstrap() {
	s.mu.Lock()
	path := s.bootstrap
	s.bootstrap = ""
	s.mu.Unlock()
	if path != "" {
		os.Remove(path)
		os.Remove(filepath.Dir(path))
	}
}
func (s *Session) bootstrapFile() (string, error) {
	dir, err := os.MkdirTemp("", "autobyteus-nfs-dashboard-")
	if err != nil {
		return "", err
	}
	if err = os.Chmod(dir, 0700); err != nil {
		os.Remove(dir)
		return "", err
	}
	path := filepath.Join(dir, "open-dashboard.html")
	data := `<!doctype html><meta name="referrer" content="no-referrer"><meta http-equiv="refresh" content="0;url=` + html.EscapeString(s.origin+"/#"+s.secret) + `"><title>Opening local NFS dashboard</title>`
	if err = os.WriteFile(path, []byte(data), 0600); err != nil {
		os.Remove(dir)
		return "", err
	}
	s.mu.Lock()
	s.bootstrap = path
	s.mu.Unlock()
	return path, nil
}
func (s *Session) Run(ctx context.Context, log io.Writer) error {
	s.terminal.setOutput(log)
	path, err := s.bootstrapFile()
	if err != nil {
		s.listener.Close()
		return err
	}
	fallback := s.origin + "/#" + s.secret
	serverErr := make(chan error, 1)
	go func() { serverErr <- s.http.Serve(s.listener) }()
	// Deliberate private terminal fallback is the only place that displays the
	// one-time secret. Never place it in the opener's process argv/access logs.
	s.terminal.guidance("Local", s.role, "dashboard. If the HTML association does not open a browser, open this PRIVATE one-time URL in a browser:", fallback)
	openerDone := make(chan struct{})
	var opener *exec.Cmd
	if runtime.GOOS == "darwin" {
		opener = exec.Command("/usr/bin/open", path)
	} else {
		if binary, e := exec.LookPath("xdg-open"); e == nil {
			opener = exec.Command(binary, path)
		}
	}
	if opener == nil {
		close(openerDone)
		s.terminal.guidance("Browser opener unavailable; use the private URL above.")
	} else if openerErr := opener.Start(); openerErr != nil {
		close(openerDone)
		s.terminal.guidance("Browser opener failed; use the private URL above.")
	} else {
		// Opener lifetime is tracked, but does not authorize or stall HTTP serving.
		go func() {
			defer close(openerDone)
			if e := opener.Wait(); e != nil {
				s.terminal.guidance("Browser association failed; use the private URL above.")
			}
		}()
	}
	select {
	case <-ctx.Done():
		s.Stop()
	case <-s.stop:
	case err = <-serverErr:
		s.Stop()
	}
	s.terminal.print("Stopping dashboard admission. Waiting for any admitted host operation/directory read to finish; restore storage if it is waiting. Storage is NOT disconnected.")
	shutdown, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	_ = s.http.Shutdown(shutdown)
	cancel()
	s.Drain()
	select {
	case <-openerDone:
	default:
		s.terminal.print("Waiting for browser association process PID", opener.Process.Pid, "to exit; close that opener if needed. No browser or host operation will be force-killed.")
		<-openerDone
	}
	return err
}
