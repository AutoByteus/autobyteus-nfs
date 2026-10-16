package setup

import (
	"encoding/json"
	"os"
	"strings"
	"testing"

	"github.com/AutoByteus/autobyteus-nfs/internal/config"
)

func TestDeclineNeverChangesResources(t *testing.T) {
	s := Service{} // Any attempted dependency use would panic; denial is first.
	if err := s.Apply(Plan{}, false); err == nil {
		t.Fatal("decline accepted")
	}
	if err := s.Detach(false); err == nil {
		t.Fatal("detach decline accepted")
	}

}
func TestCurrentPendingReceiptHasNoNodeObligations(t *testing.T) {
	p := Plan{}
	b, err := json.Marshal(p)
	if err != nil {
		t.Fatal(err)
	}
	if strings.Contains(strings.ToLower(string(b)), "nodes") {
		t.Fatal("current receipt still carries nodes")
	}
}
func TestBackgroundReconnectDoesNotResumePendingSetup(t *testing.T) {
	dir := t.TempDir()
	_ = os.Chmod(dir, 0700)
	store := config.Store{Directory: dir, Owner: uint32(os.Getuid())}
	if err := store.Write("pending-setup.json", Plan{Attachment: config.Attachment{Connection: config.Connection{StorageID: "5544dadc-86b0-43ba-9799-74728b442227", Endpoint: "192.168.1.2", Export: "/Projects", Protocol: "3", MountRoot: config.DefaultMountRoot}, InstallationID: "5544dadc-86b0-43ba-9799-74728b442227", UserUID: 1000, UserGID: 1000}}); err != nil {
		t.Fatal(err)
	}
	s := Service{Store: store}
	if err := s.Reconnect(); err == nil || !strings.Contains(err.Error(), "interactively") {
		t.Fatal(err)
	}
}
