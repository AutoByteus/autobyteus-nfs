package setup

// Local file/runner fixtures only. Darwin stops at the doubled mount command;
// Linux observes its existing unrelated /proc mount and refuses to unmount it.
// No real mount, job, engine or probe mutation is performed.
import (
	"errors"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"testing"

	"github.com/AutoByteus/autobyteus-nfs/internal/backend"
	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/docker"
	"github.com/AutoByteus/autobyteus-nfs/internal/platform"
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
	if runtime.GOOS == "linux" {
		// Mounts reads /proc directly on Linux, not Runner. Use a known unrelated
		// mount so valid preflight stops before teardown even for nonroot tests.
		a.MountRoot = "/proc"
		m, err := platform.Observe(runner, a.Connection)
		if err != nil || m == nil || m.Filesystem != "proc" || platform.Matches(m, a.Connection) {
			t.Fatalf("fixture requires the existing unrelated proc mount: %+v, %v", m, err)
		}
	}
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

// Linux reaches the ordinary read-only mismatch/refusal path without a command.
// Other supported hosts reach the deliberately failed mount command instead.
func assertConfigMountBoundary(t *testing.T, r *configBoundaryRunner, err error, linuxError string) {
	t.Helper()
	if runtime.GOOS == "linux" {
		if err == nil || err.Error() != linuxError || r.calls != 0 {
			t.Fatal("did not stop at Linux mount boundary", err, r.calls)
		}
	} else if !errors.Is(err, mountBoundary) || r.calls != 1 {
		t.Fatal("did not stop at command mount boundary", err, r.calls)
	}
}

func retainHostedFixture(t *testing.T, s Service, configPath string) func() {
	t.Helper()
	before := map[string]string{}
	missing := map[string]bool{}
	for _, p := range []string{configPath, filepath.Join(s.Store.Directory, "attachment.json"), filepath.Join(s.Store.Directory, "hosted-filesystem.json"), filepath.Join(s.Store.Directory, "pending-setup.json")} {
		b, err := os.ReadFile(p)
		if err != nil && !os.IsNotExist(err) {
			t.Fatal(err)
		}
		before[p], missing[p] = string(b), os.IsNotExist(err)
	}
	return func() {
		t.Helper()
		for p, b := range before {
			after, err := os.ReadFile(p)
			if (err != nil && !os.IsNotExist(err)) || os.IsNotExist(err) != missing[p] || string(after) != b {
				t.Fatalf("mount-boundary refusal changed fixture %s: %v", p, err)
			}
		}
	}
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
					assertConfigMountBoundary(t, r, err, "expected host NFS source/protocol is not mounted")
				} else {
					if content == "missing" && !os.IsNotExist(err) {
						t.Fatal("missing config did not refuse before readiness", err)
					}
					if content != "missing" && !strings.Contains(err.Error(), "Ganesha configuration changed") {
						t.Fatal("status ignored hosted config", err)
					}
					if r.calls != 0 {
						t.Fatal("status checked mounts before config", r.calls)
					}
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
				s, r, p := hostedConfigFixture(t, engine, content, false)
				defer retainHostedFixture(t, s, p)()
				for i := 0; i < 2; i++ {
					r.calls = 0
					assertConfigMountBoundary(t, r, s.Detach(true), "refusing to unmount an unrelated source")
				}
			})
		}
	}
}

func TestHostedConfigChecksLeaveAppleAndConnectOnlyUnchanged(t *testing.T) {
	for _, engine := range []string{"apple", ""} {
		s, r, p := hostedConfigFixture(t, engine, "different", false)
		defer retainHostedFixture(t, s, p)()
		result, err := s.Status()
		if result.HostReady {
			t.Fatal("unverified host reported ready", result)
		}
		assertConfigMountBoundary(t, r, err, "expected host NFS source/protocol is not mounted")
		r.calls = 0
		assertConfigMountBoundary(t, r, s.Detach(true), "refusing to unmount an unrelated source")
	}
}
