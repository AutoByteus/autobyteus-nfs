package config

import (
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestStandaloneStateActiveAndPendingObligations(t *testing.T) {
	a := Attachment{Connection: validConnection(), InstallationID: validConnection().StorageID, UserUID: 501, UserGID: 20}
	b, _ := json.Marshal(a)
	base := string(b[:len(b)-1])
	for _, record := range []string{"attachment.json", "pending-setup.json"} {
		for _, tc := range []struct {
			name, suffix string
			refuse       bool
		}{
			{"absent", "}", false}, {"empty", `,"nodes":[]}`, false}, {"null", `,"nodes":null}`, false},
			{"unknown", `,"additive":{"ignored":true}}`, false},
			{"active", `,"nodes":["node-one"]}`, true}, {"malformed", `,"nodes":{}}`, true},
			{"wrong-scalar", `,"nodes":false}`, true}, {"wrong-list", `,"nodes":[null]}`, true},
			{"duplicate", `,"nodes":["node-one"],"Nodes":[]}`, true},
		} {
			t.Run(record+"/"+tc.name, func(t *testing.T) {
				dir := t.TempDir()
				_ = os.Chmod(dir, 0700)
				s := Store{Directory: dir, Owner: uint32(os.Getuid())}
				data := base + tc.suffix
				if record == "pending-setup.json" {
					data = `{"Attachment":` + data + `,"NewSource":false}`
				}
				p := filepath.Join(dir, record)
				if err := os.WriteFile(p, []byte(data), 0600); err != nil {
					t.Fatal(err)
				}
				if err := CheckStandaloneState(s); (err != nil) != tc.refuse {
					t.Fatalf("refusal=%v: %v", tc.refuse, err)
				}
				after, _ := os.ReadFile(p)
				if string(after) != data {
					t.Fatal("admission mutated state")
				}
				if !tc.refuse {
					// Current writers do not perpetuate retired state; no automatic rewrite.
					current, _ := json.Marshal(a)
					if strings.Contains(strings.ToLower(string(current)), "nodes") {
						t.Fatal("retired current field")
					}
				}
			})
		}
	}
}
func TestStandaloneStateMalformedAndTrustedBoundary(t *testing.T) {
	for _, record := range []string{"attachment.json", "pending-setup.json"} {
		for _, data := range []string{`null`, `[]`, `{}`, `{} {}`, `{"Attachment":null}`, `{"Attachment":{}}`, strings.Repeat("x", MaxRecordBytes+1)} {
			dir := t.TempDir()
			_ = os.Chmod(dir, 0700)
			s := Store{Directory: dir, Owner: uint32(os.Getuid())}
			p := filepath.Join(dir, record)
			_ = os.WriteFile(p, []byte(data), 0600)
			if err := CheckStandaloneState(s); err == nil {
				t.Fatalf("accepted %s %s", record, data[:min(40, len(data))])
			}
		}
	}
	dir := t.TempDir()
	_ = os.Chmod(dir, 0700)
	s := Store{Directory: dir, Owner: uint32(os.Getuid())}
	if err := CheckStandaloneState(s); err != nil {
		t.Fatal("new install", err)
	}
	// Historical receipts are inert and never scanned, even malformed.
	_ = os.WriteFile(filepath.Join(dir, "node-old.json"), []byte("malformed"), 0600)
	if err := CheckStandaloneState(s); err != nil {
		t.Fatal("scanned history", err)
	}
	target := filepath.Join(t.TempDir(), "external")
	_ = os.WriteFile(target, []byte(`{}`), 0600)
	_ = os.Symlink(target, filepath.Join(dir, "attachment.json"))
	if err := CheckStandaloneState(s); err == nil {
		t.Fatal("followed state symlink")
	}
}
