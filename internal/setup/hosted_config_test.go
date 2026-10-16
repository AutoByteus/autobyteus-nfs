package setup

// Local file/runner fixtures only. Successful preflight stops at mount observation:
// no real mount, job, engine, probe mutation is performed.
import (
	"errors"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/AutoByteus/autobyteus-nfs/internal/backend"
	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/docker"
)

var mountBoundary = errors.New("test stopped at mount observation")

type configBoundaryRunner struct{ calls int }

func (r *configBoundaryRunner) Run(_ string, _ ...string) ([]byte, error) {
	r.calls++
	return nil, mountBoundary
}

func hostedConfigFixture(t *testing.T, engine, content string, pending bool) (Service, *configBoundaryRunner, string) {
	t.Helper()
	root := t.TempDir()
	private := filepath.Join(root, "private")
	for _, p := range []string{private, filepath.Join(private, "ganesha")} {
		if err := os.Mkdir(p, 0700); err != nil {
			t.Fatal(err)
		}
	}
	id := "5544dadc-86b0-43ba-9799-74728b442227"
	a := config.Attachment{Connection: config.Connection{StorageID: id, Endpoint: "192.168.64.7", Export: "/autobyteus/" + id, Protocol: "4.1", MountRoot: config.DefaultMountRoot}, InstallationID: id, UserUID: 1000, UserGID: 1000}
	runner := &configBoundaryRunner{}
	s := Service{Store: config.Store{Directory: private, Owner: uint32(os.Getuid())}, Runner: runner, Docker: &docker.Client{}}
	var h *config.HostedFilesystem
	if engine != "" {
		h = &config.HostedFilesystem{InstallationID: id, StorageID: id, Source: filepath.Join(root, "source"), Identity: config.Identity{Device: 1, Inode: 2}, Backend: engine, DataUID: 1000, DataGID: 1000, Allowlist: []string{"192.168.64.0/24"}}
		if engine == "apple" {
			h.Identity = config.Identity{VolumeUUID: id, Inode: 2}
		}
	}
	records := map[string]any{"attachment.json": a}
	if h != nil {
		records["hosted-filesystem.json"] = h
	}
	if pending {
		records = map[string]any{"pending-setup.json": Plan{Attachment: a, Hosted: h}}
	}
	for name, value := range records {
		if err := s.Store.Write(name, value); err != nil {
			t.Fatal(err)
		}
	}
	p := filepath.Join(private, "ganesha", "ganesha.conf")
	if content != "missing" {
		var want string
		if h != nil {
			var err error
			want, err = backend.GaneshaConfig(*h, private, engine == "ganesha-docker")
			if err != nil {
				t.Fatal(err)
			}
		}
		switch content {
		case "old":
			want = strings.ReplaceAll(want, " Attr_Expiration_Time = 0;\n", "")
		case "different":
			want += "# external change\n"
		case "malformed":
			want = "not a config"
		}
		if err := os.WriteFile(p, []byte(want), 0600); err != nil {
			t.Fatal(err)
		}
	}
	return s, runner, p
}

func TestHostedConfigStatusRefusesBeforeReadiness(t *testing.T) {
	for _, engine := range []string{"ganesha-native", "ganesha-docker"} {
		for _, content := range []string{"missing", "old", "different", "malformed", "current"} {
			t.Run(engine+"/"+content, func(t *testing.T) {
				s, r, p := hostedConfigFixture(t, engine, content, false)
				before, _ := os.ReadFile(p)
				result, err := s.Status()
				if err == nil || result.HostReady {
					t.Fatal("unverified host reported ready", result, err)
				}
				if content == "current" {
					if !errors.Is(err, mountBoundary) || r.calls != 1 {
						t.Fatal("valid config did not reach mount check", err, r.calls)
					}
				} else if errors.Is(err, mountBoundary) || r.calls != 0 {
					t.Fatal("status ignored hosted config", err, r.calls)
				}
				after, _ := os.ReadFile(p)
				if string(before) != string(after) {
					t.Fatal("status rewrote config")
				}
			})
		}
	}
}

func TestHostedConfigDetachPreflightsBeforeEffects(t *testing.T) {
	for _, engine := range []string{"ganesha-native", "ganesha-docker"} {
		for _, pending := range []bool{false, true} {
			for _, content := range []string{"old", "different", "malformed"} {
				t.Run(engine+"/"+content+map[bool]string{true: "/pending", false: "/saved"}[pending], func(t *testing.T) {
					// The unusable Docker client would panic if storage-engine teardown were reached.
					s, r, p := hostedConfigFixture(t, engine, content, pending)
					before, _ := os.ReadFile(p)
					err := s.Detach(true)
					if err == nil || !strings.Contains(err.Error(), "Ganesha configuration changed") || r.calls != 0 {
						t.Fatal("detach touched dependencies before checking config", err, r.calls)
					}
					after, _ := os.ReadFile(p)
					if string(before) != string(after) {
						t.Fatal("detach overwrote config")
					}
					name := "attachment.json"
					if pending {
						name = "pending-setup.json"
					}
					if _, err := os.Stat(filepath.Join(s.Store.Directory, name)); err != nil {
						t.Fatal("lost private receipt", err)
					}

				})
			}
		}
	}
}

func TestHostedConfigDetachCurrentOrPartialRetryReachesExistingChecks(t *testing.T) {
	for _, engine := range []string{"ganesha-native", "ganesha-docker"} {
		for _, content := range []string{"current", "missing"} {
			t.Run(engine+"/"+content, func(t *testing.T) {
				s, r, _ := hostedConfigFixture(t, engine, content, false)
				for i := 0; i < 2; i++ {
					if err := s.Detach(true); !errors.Is(err, mountBoundary) {
						t.Fatal("preflight prevented existing teardown checks", err)
					}
				}
				if r.calls != 2 {
					t.Fatal(r.calls)
				}
			})
		}
	}
}

func TestHostedConfigChecksLeaveAppleAndConnectOnlyUnchanged(t *testing.T) {
	for _, engine := range []string{"apple", ""} {
		s, r, _ := hostedConfigFixture(t, engine, "different", false)
		result, err := s.Status()
		if !errors.Is(err, mountBoundary) || result.HostReady {
			t.Fatal(result, err)
		}
		if err = s.Detach(true); !errors.Is(err, mountBoundary) {
			t.Fatal(err)
		}
		if r.calls != 2 {
			t.Fatal(r.calls)
		}
	}
}
