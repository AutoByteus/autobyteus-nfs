package docker

import (
	"encoding/json"
	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strings"
	"testing"
)

func TestEngineOnlyUsesChosenSourceAndNarrowCapabilities(t *testing.T) {
	h := config.HostedFilesystem{InstallationID: "c87ff813-c2ce-4bd5-9208-7f6e3b7d7cf7", StorageID: "5544dadc-86b0-43ba-9799-74728b442227", Source: "/srv/projects", EngineImage: "registry/engine@sha256:" + strings.Repeat("a", 64)}
	payload := EnginePayload(h, "/var/lib/autobyteus-nfs")
	host := payload["HostConfig"].(map[string]any)
	if host["NetworkMode"] != "host" || host["Privileged"] == true || strings.Contains(capabilities(host["CapAdd"]), "SYS_ADMIN") {
		t.Fatal(host)
	}
	if !strings.Contains(capabilities(host["CapAdd"]), "DAC_READ_SEARCH") {
		t.Fatal("VFS file-handle capability absent")
	}
	mounts := host["Mounts"].([]any)
	if len(mounts) != 3 {
		t.Fatal(mounts)
	}
	for _, m := range mounts {
		source := m.(map[string]any)["Source"]
		if source == "/" || source == "/var/run/docker.sock" || source == "/root" {
			t.Fatal("broad/private export")
		}
	}
	b, _ := json.Marshal(payload)
	var configObj Object
	_ = json.Unmarshal(b, &configObj)
	s := Snapshot{Config: configObj, HostConfig: configObj["HostConfig"].(map[string]any)}
	s.HostConfig["RestartPolicy"].(map[string]any)["MaximumRetryCount"] = float64(0)
	// Build actual inspect mount shape, not the create request shape.
	actual := []Object{}
	for _, raw := range mounts {
		m := raw.(map[string]any)
		actual = append(actual, Object{"Type": "bind", "Source": m["Source"], "Destination": m["Target"], "RW": !boolValue(m, "ReadOnly")})
	}
	bytes, _ := json.Marshal(actual)
	_ = json.Unmarshal(bytes, &s.Mounts)
	if err := validateEngine(s, h, "/var/lib/autobyteus-nfs"); err != nil {
		t.Fatal(err)
	}
	s.HostConfig["Privileged"] = true
	if err := validateEngine(s, h, "/var/lib/autobyteus-nfs"); err == nil {
		t.Fatal("accepted changed privilege")
	}
}

// Complete requests go through the real HTTP client against a local fake engine;
// no actual daemon, containers, app endpoints or volume operations are used.
func TestOwnedEngineLifecycleAndMismatchRefusal(t *testing.T) {
	h := config.HostedFilesystem{InstallationID: "c87ff813-c2ce-4bd5-9208-7f6e3b7d7cf7", StorageID: "5544dadc-86b0-43ba-9799-74728b442227", Source: "/srv/projects", EngineImage: "registry/engine@sha256:" + strings.Repeat("a", 64)}
	root := "/private/fixture"
	payload := EnginePayload(h, root)
	host := payload["HostConfig"].(Object)
	obj := Object{"Id": strings.Repeat("b", 64), "Image": "sha256:" + strings.Repeat("c", 64), "Config": payload, "HostConfig": host, "State": Object{"Running": false}}
	mounts := []Object{}
	for _, raw := range host["Mounts"].([]any) {
		m := raw.(Object)
		mounts = append(mounts, Object{"Type": "bind", "Source": m["Source"], "Destination": m["Target"], "RW": !boolValue(m, "ReadOnly")})
	}
	obj["Mounts"] = mounts
	var calls []string
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		calls = append(calls, r.Method+" "+r.URL.Path)
		if r.URL.Path == apiPrefix+"/info" {
			_ = json.NewEncoder(w).Encode(Object{"OSType": "linux"})
			return
		}
		if strings.HasSuffix(r.URL.Path, "/json") {
			_ = json.NewEncoder(w).Encode(obj)
			return
		}
		if strings.HasSuffix(r.URL.Path, "/start") || strings.HasSuffix(r.URL.Path, "/stop") || r.Method == "DELETE" {
			w.WriteHeader(204)
			return
		}
		t.Errorf("unexpected engine request %s %s", r.Method, r.URL.Path)
		w.WriteHeader(500)
	}))
	defer server.Close()
	c := &Client{http: &http.Client{Transport: engineTransport{base: server.URL}}}
	if err := c.EnsureEngine(h, root, false); err != nil {
		t.Fatal(err)
	}
	if len(calls) != 3 || !strings.HasSuffix(calls[2], "/"+strings.Repeat("b", 64)+"/start") {
		t.Fatal(calls)
	}
	calls = nil
	host["Privileged"] = true
	if err := c.EnsureEngine(h, root, false); err == nil {
		t.Fatal("accepted changed engine")
	}
	if len(calls) != 2 {
		t.Fatal("mutated mismatched engine", calls)
	}
	host["Privileged"] = false
	obj["State"] = Object{"Running": true}
	calls = nil
	if err := c.DetachEngine(h, root); err != nil {
		t.Fatal(err)
	}
	if len(calls) != 3 || !strings.Contains(calls[1], "/stop") || !strings.HasPrefix(calls[2], "DELETE ") {
		t.Fatal(calls)
	}
}

type engineTransport struct{ base string }

func (t engineTransport) RoundTrip(r *http.Request) (*http.Response, error) {
	u, _ := url.Parse(t.base)
	r.URL.Scheme = u.Scheme
	r.URL.Host = u.Host
	return http.DefaultTransport.RoundTrip(r)
}
