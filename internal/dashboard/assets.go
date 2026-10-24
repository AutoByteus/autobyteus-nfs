package dashboard

import (
	"embed"
	"net/http"
)

//go:embed web/*
var assets embed.FS

func (s *Session) asset(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		http.Error(w, "method refused", 405)
		return
	}
	names := map[string]string{"/": "index.html", "/styles.css": "styles.css", "/app.js": "app.js", "/api.js": "api.js", "/forms.js": "forms.js"}
	name, ok := names[r.URL.Path]
	if !ok {
		http.NotFound(w, r)
		return
	}
	data, err := assets.ReadFile("web/" + name)
	if err != nil {
		http.NotFound(w, r)
		return
	}
	types := map[string]string{"index.html": "text/html; charset=utf-8", "styles.css": "text/css; charset=utf-8", "app.js": "text/javascript; charset=utf-8", "api.js": "text/javascript; charset=utf-8", "forms.js": "text/javascript; charset=utf-8"}
	w.Header().Set("Content-Type", types[name])
	w.Write(data)
}
