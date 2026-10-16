package setup

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/platform"
)

func TestStandaloneRefusesPredecessorObligationsBeforeEffects(t *testing.T) {
	for _, name := range []string{"attachment.json", "pending-setup.json"} {
		for _, nodes := range []any{[]string{"node-one"}, "malformed"} {
			t.Run(name, func(t *testing.T) {
				dir := t.TempDir()
				_ = os.Chmod(dir, 0700)
				s := Service{Store: config.Store{Directory: dir, Owner: uint32(os.Getuid())}}
				lock, err := platform.Lock(dir)
				if err != nil {
					t.Fatal(err)
				}
				defer lock.Close()
				s.Lock = lock
				a := map[string]any{"storageId": "5544dadc-86b0-43ba-9799-74728b442227", "installationId": "5544dadc-86b0-43ba-9799-74728b442227", "endpoint": "192.168.1.2", "export": "/Projects", "protocol": "3", "mountRoot": config.DefaultMountRoot, "userUid": 501, "userGid": 20, "nodes": nodes}
				var value any = a
				if name == "pending-setup.json" {
					value = map[string]any{"Attachment": a, "NewSource": false}
				}
				if err = s.Store.Write(name, value); err != nil {
					t.Fatal(err)
				}
				before, _ := os.ReadFile(filepath.Join(dir, name))
				// Dependencies deliberately absent: any runner/Docker use would panic.
				actions := []func() error{
					func() error { _, e := s.Plan(Request{}); return e }, func() error { return s.Apply(Plan{}, true) },
					s.Reconnect, func() error { return s.Detach(true) }, func() error { _, e := s.Status(); return e }, func() error { _, e := s.PendingPlan(); return e },
				}
				for _, action := range actions {
					if err = action(); err == nil {
						t.Fatal("accepted obligation")
					}
				}
				after, _ := os.ReadFile(filepath.Join(dir, name))
				if string(after) != string(before) {
					t.Fatal("changed predecessor bytes")
				}
				entries, _ := os.ReadDir(dir)
				if len(entries) != 2 {
					t.Fatal("created resource/config", entries)
				}
			})
		}
	}
}
