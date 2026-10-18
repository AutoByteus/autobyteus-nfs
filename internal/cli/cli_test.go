package cli

import (
	"encoding/json"
	"os"
	"path/filepath"
	"runtime"
	"testing"

	"github.com/AutoByteus/autobyteus-nfs/internal/setup"
)

func TestExplicitNoTTYInputsAndNoShellEvaluation(t *testing.T) {
	o, err := Parse([]string{"create", "--source", "/srv/projects", "--endpoint", "192.168.1.5", "--allow", "192.168.1.0/24", "--backend", "ganesha-native", "--yes"})
	if err != nil {
		t.Fatal(err)
	}
	req, err := collect(o, &Terminal{})
	if err != nil || req.Source != "/srv/projects" || req.Connection.MountRoot != "/Volumes/autobyteus-shared" {
		t.Fatal(req, err)
	}
	if _, err = collect(Options{Action: "connect", Connection: "$(touch /tmp/nope)"}, &Terminal{}); err == nil {
		t.Fatal("accepted shell input")
	}
	if _, err = collect(Options{Action: "create"}, &Terminal{}); err == nil {
		t.Fatal("missing required source did not fail")
	}
}
func TestReleaseManifestMustMatchAndAdmitActualArchitecture(t *testing.T) {
	metadata := setup.Release{Schema: 2, FieldValidation: setup.FieldValidation{Filesystem: "deferred", User: "deferred"}, Version: "v1.2.3", ReleaseTargets: []string{runtime.GOOS + "-" + runtime.GOARCH}, SourceHash: "fixture"}
	p := filepath.Join(t.TempDir(), "release.json")
	write := func(v setup.Release) {
		b, _ := json.Marshal(v)
		if err := os.WriteFile(p, b, 0600); err != nil {
			t.Fatal(err)
		}
	}
	write(metadata)
	if err := VerifyRelease(p, metadata); err != nil {
		t.Fatal(err)
	}
	unavailable := metadata
	unavailable.ReleaseTargets = nil
	write(unavailable)
	if err := VerifyRelease(p, unavailable); err == nil {
		t.Fatal("candidate release accepted")
	}
	write(metadata)
	metadata.Version = "v2.0.0"
	if err := VerifyRelease(p, metadata); err == nil {
		t.Fatal("manifest/binary mismatch accepted")
	}
}

func TestRemovedNodeInterfaceRefuses(t *testing.T) {
	for _, args := range [][]string{{"create", "--nodes", "none"}, {"launcher-attachment"}, {"reconnect", "--nodes", "node-one"}} {
		if _, err := Parse(args); err == nil {
			t.Fatal("accepted removed interface", args)
		}
	}
}
