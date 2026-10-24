package dashboard

import (
	"encoding/json"
	"io"
	"os"
	"os/exec"
	"testing"
	"time"

	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
)

// The child is an ordinary-user protocol double: no sudo, root admission or
// storage operation. Extra pipes hold actual hello/inspect/process completion.
func TestFeedbackChild(t *testing.T) {
	mode := os.Getenv("NFS_FEEDBACK_CHILD")
	if mode == "" {
		return
	}
	gate := func(fd uintptr) {
		f := os.NewFile(fd, "test gate")
		var b [1]byte
		_, _ = io.ReadFull(f, b[:])
		f.Close()
	}
	gate(3)
	if mode == "denied" {
		os.Exit(1)
	}
	role, digest, version := os.Getenv("NFS_FEEDBACK_ROLE"), "feedback-test", adminwire.Version
	switch mode {
	case "digest":
		digest = "wrong"
	case "role":
		role = "wrong"
	case "version":
		version++
	}
	data, _ := json.Marshal(adminwire.Hello{Role: role, Digest: digest})
	_ = adminwire.Write(os.Stdout, adminwire.Reply{Version: version, Kind: "hello", Data: data}, adminwire.ReplyLimit)
	scanner := adminwire.NewReader(os.Stdin, adminwire.RequestLimit)
	for scanner.Scan() {
		var req adminwire.Request
		if adminwire.Decode(scanner.Bytes(), &req) != nil || req.Kind != "inspect" {
			os.Exit(3)
		}
		gate(4)
		if mode == "lost" {
			os.Exit(1)
		}
		reply := adminwire.Reply{Version: adminwire.Version, Kind: req.Kind, ID: req.ID, Data: json.RawMessage(`{"state":"` + mode + `","private":"PRIVATE_CONFIG_CANARY"}`)}
		if mode == "refused" {
			reply.Error = &adminwire.Failure{Code: "private", Detail: "PRIVATE_ERROR_CANARY"}
		}
		if mode == "cleanup" {
			reply.ID++
		}
		_ = adminwire.Write(os.Stdout, reply, adminwire.ReplyLimit)
		if mode == "cleanup" {
			gate(5)
			os.Exit(1)
		}
	}
	os.Exit(0)
}

type feedbackChild struct {
	hello, inspect, finish *os.File
	launch                 Launcher
}

func newFeedbackChild(t *testing.T, role, mode string) feedbackChild {
	t.Helper()
	readers := make([]*os.File, 3)
	writers := make([]*os.File, 3)
	for i := range readers {
		var err error
		readers[i], writers[i], err = os.Pipe()
		if err != nil {
			t.Fatal(err)
		}
		t.Cleanup(func() { readers[i].Close(); writers[i].Close() })
	}
	return feedbackChild{writers[0], writers[1], writers[2], func() (*exec.Cmd, string, error) {
		cmd := exec.Command(os.Args[0], "-test.run=^TestFeedbackChild$")
		cmd.Env = append(os.Environ(), "NFS_FEEDBACK_CHILD="+mode, "NFS_FEEDBACK_ROLE="+role)
		cmd.ExtraFiles = readers
		return cmd, "feedback-test", nil
	}}
}
func releaseFeedbackGate(t *testing.T, gate *os.File) {
	t.Helper()
	if _, err := gate.Write([]byte{1}); err != nil {
		t.Fatal(err)
	}
}
func waitFeedback(t *testing.T, check func() bool) {
	t.Helper()
	deadline := time.Now().Add(5 * time.Second)
	for time.Now().Before(deadline) {
		if check() {
			return
		}
		time.Sleep(time.Millisecond)
	}
	t.Fatal("feedback condition did not complete")
}
