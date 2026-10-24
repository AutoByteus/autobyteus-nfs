package dashboard

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"sync/atomic"
	"testing"
	"time"
)

func testDashboard(t *testing.T) (*Session, *atomic.Int32) {
	t.Helper()
	calls := &atomic.Int32{}
	launch := func() (*exec.Cmd, string, error) {
		calls.Add(1)
		cmd := exec.Command(os.Args[0], "-test.run=^TestPrivateClientHandshakeAndCorrelation$")
		cmd.Env = append(os.Environ(), "NFS_TEST_HELPER=current")
		return cmd, "measured-test-binary", nil
	}
	s, err := New("client", launch)
	if err != nil {
		t.Fatal(err)
	}
	go s.http.Serve(s.listener)
	t.Cleanup(func() { s.http.Close(); s.Drain() })
	return s, calls
}
func fetch(t *testing.T, s *Session, method, path, body, token, origin, host, site string) (int, []byte, http.Header) {
	t.Helper()
	r, err := http.NewRequest(method, s.origin+path, strings.NewReader(body))
	if err != nil {
		t.Fatal(err)
	}
	r.Header.Set("Content-Type", "application/json")
	if token != "" {
		r.Header.Set("Authorization", "Bearer "+token)
	}
	if origin != "" {
		r.Header.Set("Origin", origin)
	}
	if host != "" {
		r.Host = host
	}
	if site != "" {
		r.Header.Set("Sec-Fetch-Site", site)
	}
	res, err := http.DefaultClient.Do(r)
	if err != nil {
		t.Fatal(err)
	}
	defer res.Body.Close()
	data, _ := io.ReadAll(res.Body)
	return res.StatusCode, data, res.Header
}
func authenticate(t *testing.T, s *Session) string {
	t.Helper()
	b, _ := json.Marshal(map[string]string{"secret": s.secret})
	code, data, _ := fetch(t, s, "POST", "/api/session", string(b), "", s.origin, "", "same-origin")
	if code != 200 {
		t.Fatal(code, string(data))
	}
	var out struct {
		Token string `json:"token"`
	}
	json.Unmarshal(data, &out)
	return out.Token
}
func TestRealHTTPAuthorizationOriginAndBounds(t *testing.T) {
	s, calls := testDashboard(t)
	code, _, h := fetch(t, s, "GET", "/", "", "", "", "", "none")
	if code != 200 || !strings.Contains(h.Get("Content-Security-Policy"), "frame-ancestors 'none'") {
		t.Fatal(code, h)
	}
	for _, test := range []struct{ method, path, body, token, origin, host, site string }{
		{"GET", "/api/state", "", "", "", "", ""},
		{"POST", "/api/session", `{"secret":"guess"}`, "", s.origin, "", "same-origin"},
		{"POST", "/api/session", `{}`, "", "null", "", ""},
		{"POST", "/api/operations", `{}`, "", "https://foreign.example", "", "cross-site"},
		{"GET", "/", "", "", "", "foreign.example", ""},
		{"GET", "/api/state?token=bad", "", "", "", "", ""},
	} {
		code, _, _ = fetch(t, s, test.method, test.path, test.body, test.token, test.origin, test.host, test.site)
		if code != 403 {
			t.Fatal(test, code)
		}
	}
	token := authenticate(t, s)
	for _, body := range []string{`{"id":1,"id":2,"kind":"authorize","payload":{}}`, `{"id":1,"kind":"authorize","payload":{},"uid":0}`, strings.Repeat("x", 32<<10+1), `{} {}`} {
		code, _, _ = fetch(t, s, "POST", "/api/operations", body, token, s.origin, "", "same-origin")
		if code != 400 {
			t.Fatal(code)
		}
	}
	for _, origin := range []string{"", "null", "http://localhost"} {
		code, _, _ = fetch(t, s, "POST", "/api/operations", `{"id":1,"kind":"authorize","payload":{}}`, token, origin, "", "same-origin")
		if code != 403 {
			t.Fatal("missing/foreign origin", origin, code)
		}
	}
	code, _, _ = fetch(t, s, "GET", "/api/state", "", token, s.origin, "", "cross-site")
	if code != 403 {
		t.Fatal(code)
	}
	code, _, _ = fetch(t, s, "OPTIONS", "/api/operations", "", token, s.origin, "", "same-origin")
	if code != 405 {
		t.Fatal(code)
	}
	code, _, _ = fetch(t, s, "POST", "/api/session", `{"secret":"guess"}`, "", s.origin, "", "same-origin")
	if code != 403 {
		t.Fatal("exchange reused")
	}
	code, _, _ = fetch(t, s, "GET", "/api/state", "", token, "", "", "same-origin")
	if code != 200 {
		t.Fatal(code)
	}
	if calls.Load() != 0 {
		t.Fatal("unauthorized path started privilege")
	}
}
func TestSubmissionDeduplicatesAndNoAutomaticStorageWork(t *testing.T) {
	s, calls := testDashboard(t)
	token := authenticate(t, s)
	body := `{"id":1,"kind":"authorize","payload":{}}`
	code, a, _ := fetch(t, s, "POST", "/api/operations", body, token, s.origin, "", "same-origin")
	if code != 202 {
		t.Fatal(code, string(a))
	}
	code, b, _ := fetch(t, s, "POST", "/api/operations", body, token, s.origin, "", "same-origin")
	if code != 202 {
		t.Fatal(code, string(b))
	}
	var first, second Operation
	json.Unmarshal(a, &first)
	json.Unmarshal(b, &second)
	if first.ID != second.ID {
		t.Fatal("repeat created new operation")
	}
	deadline := time.Now().Add(5 * time.Second)
	for time.Now().Before(deadline) {
		if s.snapshot().Operation.State != "running" {
			break
		}
		time.Sleep(time.Millisecond)
	}
	snapshot := s.snapshot()
	if snapshot.Operation.State != "succeeded" || !snapshot.Authorized || calls.Load() != 1 {
		t.Fatal(snapshot, calls.Load())
	}
	code, _, _ = fetch(t, s, "POST", "/api/operations", `{"id":1,"kind":"checkReadiness","payload":{}}`, token, s.origin, "", "same-origin")
	if code != 409 {
		t.Fatal("conflicting id accepted")
	}
	code, _, _ = fetch(t, s, "POST", "/api/operations", `{"id":2,"kind":"authorize","payload":{}}`, token, s.origin, "", "same-origin")
	if code != 409 || calls.Load() != 1 {
		t.Fatal("duplicate auth")
	}
	s.Stop()
	code, _, _ = fetch(t, s, "POST", "/api/operations", `{"id":3,"kind":"checkReadiness","payload":{}}`, token, s.origin, "", "same-origin")
	if code != 409 {
		t.Fatal("stop admitted work")
	}
}
func TestPrivateBootstrapAndDirectoryOnlyChooser(t *testing.T) {
	s, _ := testDashboard(t)
	path, err := s.bootstrapFile()
	if err != nil {
		t.Fatal(err)
	}
	f, _ := os.Stat(path)
	dir, _ := os.Stat(filepath.Dir(path))
	if f.Mode().Perm() != 0600 || dir.Mode().Perm() != 0700 {
		t.Fatal("bootstrap permissions")
	}
	data, _ := os.ReadFile(path)
	if !bytes.Contains(data, []byte(s.secret)) {
		t.Fatal("no launch fragment")
	}
	authenticate(t, s)
	if _, err = os.Stat(path); !os.IsNotExist(err) {
		t.Fatal("bootstrap retained after exchange")
	}
	root := t.TempDir()
	root, err = filepath.EvalSymlinks(root)
	if err != nil {
		t.Fatal(err)
	}
	os.Mkdir(filepath.Join(root, "visible"), 0700)
	os.WriteFile(filepath.Join(root, "private-file"), []byte("never-read"), 0600)
	os.Symlink(filepath.Join(root, "visible"), filepath.Join(root, "alias"))
	listing := readDirectories(root)
	if listing.Error != "" || len(listing.Names) != 1 || listing.Names[0] != "visible" {
		t.Fatal(listing)
	}
	if listing = readDirectories(filepath.Join(root, "alias")); listing.Error == "" {
		t.Fatal("silently resolved symlink")
	}
	if listing = readDirectories(filepath.Join(root, "visible")); listing.Error != "" || len(listing.Names) != 0 {
		t.Fatal("empty directory refused", listing)
	}
}
