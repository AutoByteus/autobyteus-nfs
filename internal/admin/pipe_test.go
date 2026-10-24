package admin

import (
	"bufio"
	"context"
	"encoding/json"
	"io"
	"os"
	"os/exec"
	"os/signal"
	"strings"
	"syscall"
	"testing"
	"time"

	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
	"github.com/AutoByteus/autobyteus-nfs/internal/platform"
	"github.com/AutoByteus/autobyteus-nfs/internal/setup"
)

func TestPipeEOFReleasesReview(t *testing.T) {
	s := testSession(t)
	scope, err := s.acquire()
	if err != nil {
		t.Fatal(err)
	}
	_, err = s.retain(scope, "setup", setup.Plan{}, []string{"display"}, adminwire.Configuration{})
	if err != nil {
		t.Fatal(err)
	}
	inR, inW, _ := os.Pipe()
	outR, outW, _ := os.Pipe()
	defer inR.Close()
	defer outR.Close()
	defer outW.Close()
	done := make(chan error, 1)
	go func() { done <- s.ServePipe(context.Background(), inR, outW) }()
	scanner := bufio.NewScanner(outR)
	if !scanner.Scan() {
		t.Fatal("no hello")
	}
	inW.Close()
	if err = <-done; err != nil {
		t.Fatal(err)
	}
	unlocked(t, s)
}
func TestPipeRejectsMalformedAndRepeatedRequests(t *testing.T) {
	for _, frames := range []string{
		`{"version":99,"id":1,"kind":"inspect","payload":{}}`,
		`{"version":1,"id":1,"kind":"inspect","payload":{},"uid":0}`,
		`{"version":1,"id":1,"kind":"inspect","payload":{"store":"/"}}`,
		`{"version":1,"id":1,"kind":"shell","payload":{}}`,
	} {
		s := testSession(t)
		if err := s.ServePipe(context.Background(), strings.NewReader(frames+"\n"), io.Discard); err == nil {
			t.Fatal("invalid frame accepted", frames)
		}
		unlocked(t, s)
	}
}

// Actual fd1 broken-pipe subprocess, not a context-only substitute. The child's
// controlled operation holds a real flock while stdout closes before the operation completes.
func TestHelperBrokenOutputDrain(t *testing.T) {
	if os.Getenv("NFS_TEST_PIPE_CHILD") == "1" {
		signals := make(chan os.Signal, 1)
		signal.Notify(signals, syscall.SIGPIPE)
		defer signal.Stop(signals)
		s := testSession(t)
		save(t, s, "attachment.json", attachment())
		s.runner = func(*os.File) platform.Runner {
			return runnerFunc(func(string, ...string) ([]byte, error) {
				os.WriteFile(os.Getenv("NFS_TEST_PIPE_DIR")+"/started", []byte(s.base.Store.Directory), 0600)
				for {
					if _, err := os.Stat(os.Getenv("NFS_TEST_PIPE_DIR") + "/finish"); err == nil {
						break
					}
					time.Sleep(time.Millisecond)
				}
				return nil, io.EOF
			})
		}
		_ = s.ServePipe(context.Background(), os.Stdin, os.Stdout)
		unlocked(t, s)
		os.WriteFile(os.Getenv("NFS_TEST_PIPE_DIR")+"/drained", []byte("yes"), 0600)
		// The Go test harness writes its own PASS after this entry returns. It
		// is not helper output and must not write to the intentionally broken fd.
		os.Stdout.Close()
		return
	}
	dir := t.TempDir()
	cmd := exec.Command(os.Args[0], "-test.run=^TestHelperBrokenOutputDrain$")
	cmd.Env = append(os.Environ(), "NFS_TEST_PIPE_CHILD=1", "NFS_TEST_PIPE_DIR="+dir)
	in, _ := cmd.StdinPipe()
	out, _ := cmd.StdoutPipe()
	if err := cmd.Start(); err != nil {
		t.Fatal(err)
	}
	scanner := bufio.NewScanner(out)
	if !scanner.Scan() {
		t.Fatal("missing handshake")
	}
	req := adminwire.Request{Version: 1, ID: 1, Kind: "checkReadiness", Payload: json.RawMessage(`{}`)}
	if err := adminwire.Write(in, req, adminwire.RequestLimit); err != nil {
		t.Fatal(err)
	}
	var state []byte
	deadline := time.Now().Add(5 * time.Second)
	for time.Now().Before(deadline) {
		state, _ = os.ReadFile(dir + "/started")
		if len(state) > 0 {
			break
		}
		time.Sleep(time.Millisecond)
	}
	if len(state) == 0 {
		t.Fatal("child operation not started")
	}
	out.Close()
	defer in.Close()
	time.Sleep(30 * time.Millisecond)
	if f, err := platform.Lock(string(state)); err == nil {
		f.Close()
		t.Fatal("broken output released in-flight lock")
	}
	if _, err := os.Stat(dir + "/drained"); err == nil {
		t.Fatal("claimed drain early")
	}
	os.WriteFile(dir+"/finish", nil, 0600)
	if err := cmd.Wait(); err != nil {
		t.Fatal("SIGPIPE killed helper before drain", err)
	}
	if _, err := os.Stat(dir + "/drained"); err != nil {
		t.Fatal("no drain receipt", err)
	}
}
