package cli

import (
	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/platform"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestInstallRefusesPredecessorBeforeBinaryEffects(t *testing.T) {
	for _, record := range []string{"attachment.json", "pending-setup.json"} {
		for _, nodes := range []string{`[{"containerId":"old-owned-id"}]`, `{}`, `false`} {
			t.Run(record+nodes, func(t *testing.T) {
				root := t.TempDir()
				state := filepath.Join(root, "private")
				if err := os.Mkdir(state, 0700); err != nil {
					t.Fatal(err)
				}
				data := `{"nodes":` + nodes + `}`
				if record == "pending-setup.json" {
					data = `{"attachment":` + data + `}`
				}
				if err := os.WriteFile(filepath.Join(state, record), []byte(data), 0600); err != nil {
					t.Fatal(err)
				}
				target := filepath.Join(root, "not-created", "autobyteus-nfs")
				store := config.Store{Directory: state, Owner: uint32(os.Getuid())}
				err := installRootBinary(store, target)
				if err == nil || !strings.Contains(err.Error(), "node-management obligation") {
					t.Fatalf("wrong admission: %v", err)
				}
				if _, err := os.Stat(filepath.Dir(target)); !os.IsNotExist(err) {
					t.Fatal("binary parent touched before admission", err)
				}
				// An existing binary is preserved too.
				if err := os.Mkdir(filepath.Dir(target), 0700); err != nil {
					t.Fatal(err)
				}
				if err := os.WriteFile(target, []byte("matching predecessor"), 0700); err != nil {
					t.Fatal(err)
				}
				if err := installRootBinary(store, target); err == nil {
					t.Fatal("accepted obligations")
				}
				got, _ := os.ReadFile(target)
				if string(got) != "matching predecessor" {
					t.Fatal("replaced predecessor")
				}
				got, _ = os.ReadFile(filepath.Join(state, record))
				if string(got) != data {
					t.Fatal("rewrote state")
				}
				lock, err := platform.Lock(state)
				if err != nil {
					t.Fatal("leaked lock", err)
				}
				defer lock.Close()
				if err := installRootBinary(store, target); err == nil || !strings.Contains(err.Error(), "another administrative operation") {
					t.Fatalf("admission did not acquire lock first: %v", err)
				}
			})
		}
	}
}
