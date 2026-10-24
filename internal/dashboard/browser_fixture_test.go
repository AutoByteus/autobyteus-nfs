//go:build dashboardpreview

package dashboard

// This build-tagged preview uses the actual HTTP/session/assets and a subprocess
// root-protocol double. It cannot run an installer or storage operation. Native
// privilege/storage evidence is separate; these controlled states prove the UI.
import (
	"encoding/json"
	"os"
	"os/exec"
	"path/filepath"
	"testing"
	"time"

	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
	"github.com/AutoByteus/autobyteus-nfs/internal/config"
)

func TestBrowserFixture(t *testing.T) {
	if os.Getenv("NFS_PREVIEW_CHILD") == "1" {
		previewChild()
		os.Exit(0)
	}
	output := os.Getenv("NFS_PREVIEW_OUTPUT")
	if output == "" {
		t.Fatal("preview requires an owned output path")
	}
	role := os.Getenv("NFS_PREVIEW_ROLE")
	launch := func() (*exec.Cmd, string, error) {
		cmd := exec.Command(os.Args[0], "-test.run=^TestBrowserFixture$")
		cmd.Env = append(os.Environ(), "NFS_PREVIEW_CHILD=1")
		return cmd, "preview-double-not-product-proof", nil
	}
	s, err := New(role, launch)
	if err != nil {
		t.Fatal(err)
	}
	s.home = filepath.Dir(output)
	os.Mkdir(filepath.Join(s.home, "visible-folder"), 0700)
	os.WriteFile(filepath.Join(s.home, "private-file"), []byte("not listed"), 0600)
	path, err := s.bootstrapFile()
	if err != nil {
		t.Fatal(err)
	}
	b, _ := json.Marshal(map[string]string{"bootstrap": path, "origin": s.origin})
	if err = os.WriteFile(output, b, 0600); err != nil {
		t.Fatal(err)
	}
	go s.http.Serve(s.listener)
	<-s.stop
	s.http.Close()
	s.Drain()
}
func previewChild() {
	role, scenario := os.Getenv("NFS_PREVIEW_ROLE"), os.Getenv("NFS_PREVIEW_SCENARIO")
	c := adminwire.Configuration{State: "empty"}
	connection := config.Connection{StorageID: "c87ff813-c2ce-4bd5-9208-7f6e3b7d7cf7", Endpoint: "192.168.1.20", Export: "/Shared", Protocol: "3", MountRoot: "/Volumes/autobyteus-shared"}
	if scenario == "pending" || scenario == "wrong-role" {
		c = adminwire.Configuration{State: "pending", Role: role, Connection: &connection, Source: "/Shared"}
		if scenario == "wrong-role" {
			c.State = "configured"
			if role == "server" {
				c.Role = "client"
			} else {
				c.Role = "server"
			}
		}
	}
	send := func(id uint64, kind string, data any, failure *adminwire.Failure) {
		b, _ := json.Marshal(data)
		adminwire.Write(os.Stdout, adminwire.Reply{Version: 1, ID: id, Kind: kind, Data: b, Error: failure}, adminwire.ReplyLimit)
	}
	send(0, "hello", adminwire.Hello{Role: role, Digest: "preview-double-not-product-proof"}, nil)
	scanner := adminwire.NewReader(os.Stdin, adminwire.RequestLimit)
	var review adminwire.Review
	for scanner.Scan() {
		var req adminwire.Request
		if adminwire.Decode(scanner.Bytes(), &req) != nil {
			os.Exit(2)
		}
		f, _ := os.OpenFile(os.Getenv("NFS_PREVIEW_OUTPUT")+".calls", os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0600)
		if f != nil {
			json.NewEncoder(f).Encode(req)
			f.Close()
		}
		switch req.Kind {
		case "inspect":
			send(req.ID, req.Kind, c, nil)
		case "beginServer", "beginClient", "beginReconnect", "beginDetach":
			if scenario == "error" {
				send(req.ID, req.Kind, nil, &adminwire.Failure{Code: "fixture", Detail: "<img src=x onerror=alert(1)> refused source — literal error fixture"})
				continue
			}
			kind := "setup"
			if req.Kind == "beginReconnect" {
				kind = "resume"
			}
			if req.Kind == "beginDetach" {
				kind = "detach"
			}
			review = adminwire.Review{LeaseID: "fixed-preview-lease", Kind: kind, ExpiresAt: time.Now().Add(5 * time.Minute), Summary: []string{"Exact controlled review (root protocol double, no storage effects)", "Mount 192.168.1.20:/Shared at /Volumes/autobyteus-shared", "Source and private data remain in place"}, Configuration: c}
			if review.Configuration.Connection == nil {
				review.Configuration.Connection = &connection
			}
			if scenario == "expired" {
				review.ExpiresAt = time.Now().Add(-time.Second)
			}
			send(req.ID, req.Kind, review, nil)
		case "cancelReview":
			send(req.ID, req.Kind, struct{}{}, nil)
		case "commit":
			if scenario == "slow" || scenario == "stop-running" {
				time.Sleep(3 * time.Second)
			}
			if review.Kind == "detach" {
				c = adminwire.Configuration{State: "empty"}
				send(req.ID, req.Kind, adminwire.Result{Configuration: &c}, nil)
				continue
			}
			c = adminwire.Configuration{State: "configured", Role: role, Connection: &connection}
			send(req.ID, req.Kind, map[string]any{"configuration": c, "status": map[string]any{"hostReady": true, "mountRoot": connection.MountRoot}, "checkedAt": time.Now()}, nil)
		case "checkReadiness":
			send(req.ID, req.Kind, map[string]any{"configuration": c, "status": map[string]any{"hostReady": true}, "checkedAt": time.Now()}, nil)
		default:
			os.Exit(3)
		}
	}
}
