package dashboard

import (
	"crypto/subtle"
	"encoding/json"
	"errors"
	"io"
	"net/http"
	"strings"

	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
)

func (s *Session) serve(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Security-Policy", "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'none'; form-action 'none'")
	w.Header().Set("Referrer-Policy", "no-referrer")
	w.Header().Set("X-Content-Type-Options", "nosniff")
	w.Header().Set("Cache-Control", "no-store")
	if r.Host != s.host || r.URL.RawQuery != "" {
		http.Error(w, "invalid local address", http.StatusForbidden)
		return
	}
	headerBytes := 0
	for key, values := range r.Header {
		for _, v := range values {
			headerBytes += len(key) + len(v) + 4
		}
	}
	if headerBytes > 8<<10 {
		http.Error(w, "headers exceed bound", http.StatusRequestHeaderFieldsTooLarge)
		return
	}
	if !strings.HasPrefix(r.URL.Path, "/api/") {
		s.asset(w, r)
		return
	}
	if r.Header.Get("Sec-Fetch-Site") == "cross-site" {
		http.Error(w, "cross-site request refused", http.StatusForbidden)
		return
	}
	origin := r.Header.Get("Origin")
	if (r.Method == "POST" && origin != s.origin) || (origin != "" && origin != s.origin) {
		http.Error(w, "origin refused", http.StatusForbidden)
		return
	}
	if r.URL.Path == "/api/session" {
		if r.Method != "POST" {
			http.Error(w, "method refused", http.StatusMethodNotAllowed)
			return
		}
		var input struct {
			Secret string `json:"secret"`
		}
		if err := body(w, r, &input); err != nil {
			http.Error(w, "invalid session request", 400)
			return
		}
		s.mu.Lock()
		valid := s.secret != "" && subtle.ConstantTimeCompare([]byte(input.Secret), []byte(s.secret)) == 1 && !s.closing
		if valid {
			s.secret = ""
			s.token = secret()
		}
		token := s.token
		s.mu.Unlock()
		if !valid {
			http.Error(w, "session refused", 403)
			return
		}
		s.removeBootstrap()
		respond(w, 200, map[string]string{"token": token})
		return
	}
	s.mu.Lock()
	valid := s.token != "" && subtle.ConstantTimeCompare([]byte(r.Header.Get("Authorization")), []byte("Bearer "+s.token)) == 1
	s.mu.Unlock()
	if !valid {
		http.Error(w, "session authorization required", 403)
		return
	}
	switch r.URL.Path {
	case "/api/state":
		if r.Method == "GET" {
			respond(w, 200, s.snapshot())
			return
		}
	case "/api/operations":
		if r.Method == "POST" {
			var input Submission
			if err := body(w, r, &input); err != nil {
				http.Error(w, "invalid bounded operation", 400)
				return
			}
			op, err := s.submit(input)
			if err != nil {
				http.Error(w, err.Error(), 409)
				return
			}
			respond(w, 202, op)
			return
		}
	case "/api/directories":
		if r.Method == "GET" {
			respond(w, 200, s.directorySnapshot())
			return
		}
		if r.Method == "POST" {
			var input struct {
				Path string `json:"path"`
			}
			if err := body(w, r, &input); err != nil {
				http.Error(w, "invalid directory request", 400)
				return
			}
			listing, err := s.listDirectories(input.Path)
			if err != nil {
				http.Error(w, err.Error(), 409)
				return
			}
			respond(w, 202, listing)
			return
		}
	case "/api/stop":
		if r.Method == "POST" {
			var input struct{}
			if err := body(w, r, &input); err != nil {
				http.Error(w, "invalid stop request", 400)
				return
			}
			s.Stop()
			respond(w, 202, map[string]string{"state": "stopping; any active host work will drain; storage is not detached"})
			return
		}
	default:
		http.NotFound(w, r)
		return
	}
	http.Error(w, "method refused", http.StatusMethodNotAllowed)
}
func body(w http.ResponseWriter, r *http.Request, target any) error {
	if r.Header.Get("Content-Type") != "application/json" {
		return errors.New("JSON required")
	}
	b, err := io.ReadAll(http.MaxBytesReader(w, r.Body, adminwire.RequestLimit))
	if err != nil {
		return err
	}
	return adminwire.Decode(b, target)
}
func respond(w http.ResponseWriter, status int, value any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(value)
}
