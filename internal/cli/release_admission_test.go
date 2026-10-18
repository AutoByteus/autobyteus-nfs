package cli

import (
	"encoding/json"
	"io"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"testing"

	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/setup"
)

func releaseFixture() setup.Release {
	return setup.Release{Schema: 2, Version: "v0.1.0", SourceHash: strings.Repeat("a", 64),
		ReleaseTargets:  []string{"darwin-amd64", "darwin-arm64", "linux-amd64", "linux-arm64"},
		FieldValidation: setup.FieldValidation{Filesystem: "deferred", User: "deferred"}}
}

func TestReleaseAdmissionCurrentSchemaAndClaims(t *testing.T) {
	base := releaseFixture()
	data, _ := json.Marshal(base)
	path := filepath.Join(t.TempDir(), "release.json")
	variants := map[string]string{
		"legacy-only":      strings.Replace(string(data), "releaseTargets", "qualifiedTargets", 1),
		"legacy-extra":     strings.Replace(string(data), `"schema":2`, `"schema":2,"qualifiedTargets":[]`, 1),
		"missing-schema":   strings.Replace(string(data), `"schema":2,`, "", 1),
		"old-schema":       strings.Replace(string(data), `"schema":2`, `"schema":1`, 1),
		"missing-status":   strings.Replace(string(data), `"filesystem":"deferred",`, "", 1),
		"false-user":       strings.Replace(string(data), `"user":"deferred"`, `"user":"passed"`, 1),
		"false-filesystem": strings.Replace(string(data), `"filesystem":"deferred"`, `"filesystem":"passed"`, 1),
		"unknown-status":   strings.Replace(string(data), `"user":"deferred"`, `"user":"unknown"`, 1),
		"extra-claim":      strings.Replace(string(data), `"user":"deferred"`, `"user":"deferred","physical":"passed"`, 1),
		"duplicate":        strings.Replace(string(data), `"schema":2`, `"schema":1,"schema":2`, 1),
		"duplicate-status": strings.Replace(string(data), `"user":"deferred"`, `"user":"passed","user":"deferred"`, 1),
		"trailing":         string(data) + "{}", "null": "null", "empty": "",
	}
	for name, raw := range variants {
		t.Run(name, func(t *testing.T) {
			if err := os.WriteFile(path, []byte(raw), 0600); err != nil {
				t.Fatal(err)
			}
			// Even a binary with the same malformed typed values must refuse.
			var embedded setup.Release
			_ = json.Unmarshal([]byte(raw), &embedded)
			if err := VerifyRelease(path, embedded); err == nil {
				t.Fatal("admitted invalid claim")
			}
		})
	}
	for name, targets := range map[string][]string{
		"candidate": {}, "unsupported": {"windows-amd64"},
		"duplicate":    {runtime.GOOS + "-" + runtime.GOARCH, runtime.GOOS + "-" + runtime.GOARCH},
		"wrong-target": {"darwin-amd64"},
	} {
		if name == "wrong-target" && runtime.GOOS+"-"+runtime.GOARCH == "darwin-amd64" {
			targets = []string{"linux-amd64"}
		}
		t.Run(name, func(t *testing.T) {
			changed := base
			changed.ReleaseTargets = targets
			raw, _ := json.Marshal(changed)
			os.WriteFile(path, raw, 0600)
			if err := VerifyRelease(path, changed); err == nil {
				t.Fatal("admitted target")
			}
		})
	}
	os.WriteFile(path, data, 0600)
	if err := VerifyRelease(path, base); err != nil {
		t.Fatal(err)
	}
	changed := base
	changed.SourceHash = strings.Repeat("b", 64)
	if err := VerifyRelease(path, changed); err == nil {
		t.Fatal("source mismatch admitted")
	}
	link := path + ".link"
	if err := os.Symlink(path, link); err != nil {
		t.Fatal(err)
	}
	if err := VerifyRelease(link, base); err == nil {
		t.Fatal("linked manifest admitted")
	}
	if err := VerifyRelease(filepath.Dir(path), base); err == nil {
		t.Fatal("directory admitted")
	}
	os.WriteFile(path, make([]byte, config.MaxRecordBytes+1), 0600)
	if err := VerifyRelease(path, base); err == nil {
		t.Fatal("oversize admitted")
	}
}

func captureReleaseOutput(t *testing.T, args []string, release setup.Release) (string, string, error) {
	t.Helper()
	out, err := os.CreateTemp(t.TempDir(), "out")
	if err != nil {
		t.Fatal(err)
	}
	defer out.Close()
	stderr, err := os.CreateTemp(t.TempDir(), "err")
	if err != nil {
		t.Fatal(err)
	}
	defer stderr.Close()
	oldOut, oldErr := os.Stdout, os.Stderr
	os.Stdout, os.Stderr = out, stderr
	defer func() { os.Stdout, os.Stderr = oldOut, oldErr }()
	result := Run(args, release)
	out.Seek(0, 0)
	stderr.Seek(0, 0)
	stdoutBytes, _ := io.ReadAll(out)
	stderrBytes, _ := io.ReadAll(stderr)
	return string(stdoutBytes), string(stderrBytes), result
}

func TestReleaseNoticeOnlyAfterAdmissionAndExactVersionStdout(t *testing.T) {
	release := releaseFixture()
	path := filepath.Join(t.TempDir(), "release.json")
	data, _ := json.Marshal(release)
	os.WriteFile(path, data, 0600)
	stdout, stderr, err := captureReleaseOutput(t, []string{"verify-release", path}, release)
	if err != nil || stdout != "" || stderr != "Shared-filesystem/physical and user testing is deferred; distribution and signature checks are not field qualification.\n" {
		t.Fatal(stdout, stderr, err)
	}
	stdout, stderr, err = captureReleaseOutput(t, []string{"version"}, release)
	if err != nil || stdout != "v0.1.0\n" || stderr != "" {
		t.Fatal(stdout, stderr, err)
	}
	release.ReleaseTargets = nil
	stdout, stderr, err = captureReleaseOutput(t, []string{"verify-release", path}, release)
	if err == nil || stdout != "" || stderr != "" {
		t.Fatal("notice before admission", stdout, stderr, err)
	}
	// The new release-only strict reader must not tighten installed-state decode.
	var host struct {
		Version int `json:"version"`
	}
	if err := config.Decode([]byte(`{"version":1,"additive":true}`), &host); err != nil || host.Version != 1 {
		t.Fatal(host, err)
	}
}
