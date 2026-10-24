package cli

import (
	"os"
	"strings"
	"testing"
)

func TestServiceEntryHasOneOwnerAndNoInteractiveIdentity(t *testing.T) {
	data, err := os.ReadFile("run.go")
	if err != nil {
		t.Fatal(err)
	}
	s := string(data)
	if !strings.Contains(s, "return session.Supervise(ctx, os.Stderr)") || strings.Contains(s, "service.Supervise") || strings.Contains(s, "platform.Lock(") || strings.Contains(s, "openSavedDocker") {
		t.Fatal("service/terminal orchestration escaped admin")
	}
	start := strings.Index(s, `if o.Action == "service"`)
	end := strings.Index(s[start:], `if o.Action == ""`)
	if start < 0 || end < 0 {
		t.Fatal("missing entry")
	}
	if strings.Contains(s[start:start+end], "InitiatingUser") || strings.Contains(s[start:start+end], "Confirm") {
		t.Fatal("service requires interactive identity")
	}
	if _, err = os.Stat("../service/supervisor.go"); !os.IsNotExist(err) {
		t.Fatal("obsolete callback supervisor retained", err)
	}
}

func TestDashboardLaunchOnlyArguments(t *testing.T) {
	for _, role := range []string{"server", "client"} {
		o, err := Parse([]string{role})
		if err != nil || o.Action != role {
			t.Fatal(o, err)
		}
		for _, extra := range [][]string{{"--yes"}, {"--source", "/unsafe"}, {"--json"}, {"--"}, {"create"}} {
			if _, err := Parse(append([]string{role}, extra...)); err == nil {
				t.Fatal("dashboard accepted hidden setup input", role, extra)
			}
		}
	}
}
