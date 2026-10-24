package dashboard

import (
	"encoding/json"
	"os"
	"os/exec"
	"testing"

	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
)

func TestPrivateClientHandshakeAndCorrelation(t *testing.T) {
	if mode := os.Getenv("NFS_TEST_HELPER"); mode != "" {
		digest := "measured-test-binary"
		if mode == "mismatch" {
			digest = "different"
		}
		data, _ := json.Marshal(adminwire.Hello{Role: "client", Digest: digest})
		adminwire.Write(os.Stdout, adminwire.Reply{Version: 1, Kind: "hello", Data: data}, adminwire.ReplyLimit)
		scanner := adminwire.NewReader(os.Stdin, adminwire.RequestLimit)
		for scanner.Scan() {
			var req adminwire.Request
			if err := adminwire.Decode(scanner.Bytes(), &req); err != nil {
				os.Exit(3)
			}
			id := req.ID
			if mode == "wrong-id" {
				id++
			}
			adminwire.Write(os.Stdout, adminwire.Reply{Version: 1, ID: id, Kind: req.Kind, Data: json.RawMessage(`{"state":"empty"}`)}, adminwire.ReplyLimit)
		}
		os.Exit(0)
	}
	for _, mode := range []string{"current", "mismatch", "wrong-id"} {
		t.Run(mode, func(t *testing.T) {
			launch := func() (*exec.Cmd, string, error) {
				cmd := exec.Command(os.Args[0], "-test.run=^TestPrivateClientHandshakeAndCorrelation$")
				cmd.Env = append(os.Environ(), "NFS_TEST_HELPER="+mode)
				return cmd, "measured-test-binary", nil
			}
			h, err := authorize(launch, "client")
			if mode == "mismatch" {
				if err == nil {
					h.close()
					t.Fatal("mismatched binary accepted")
				}
				return
			}
			if err != nil {
				t.Fatal(err)
			}
			defer h.close()
			reply, err := h.call("inspect", json.RawMessage(`{}`))
			if mode == "wrong-id" {
				if err == nil {
					t.Fatal("foreign reply accepted")
				}
				return
			}
			if err != nil || reply.ID != 1 {
				t.Fatal(reply, err)
			}
			if err = h.close(); err != nil {
				t.Fatal(err)
			}
			if _, err = h.call("inspect", json.RawMessage(`{}`)); err == nil {
				t.Fatal("closed helper used")
			}
		})
	}
}
