package dashboard

import (
	"errors"
	"io"
	"os"
	"path/filepath"
	"sync"
)

type DirectoryListing struct {
	State   string   `json:"state"`
	Path    string   `json:"path"`
	Parent  string   `json:"parent,omitempty"`
	Names   []string `json:"names,omitempty"`
	TooMany bool     `json:"tooMany"`
	Error   string   `json:"error,omitempty"`
}
type directorySlot struct {
	mu      sync.Mutex
	listing DirectoryListing
}

func (s *Session) listDirectories(path string) (DirectoryListing, error) {
	if !filepath.IsAbs(path) || filepath.Clean(path) != path {
		return DirectoryListing{}, errors.New("enter a clean absolute directory path")
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.closing {
		return DirectoryListing{}, errors.New("dashboard is stopping")
	}
	s.directories.mu.Lock()
	defer s.directories.mu.Unlock()
	if s.directories.listing.State == "running" {
		return s.directories.listing, errors.New("directory listing still waiting; enter a path manually")
	}
	s.directories.listing = DirectoryListing{State: "running", Path: path}
	s.workers.Add(1)
	go func() {
		defer s.workers.Done()
		listing := readDirectories(path)
		s.directories.mu.Lock()
		s.directories.listing = listing
		s.directories.mu.Unlock()
	}()
	return s.directories.listing, nil
}
func (s *Session) directorySnapshot() DirectoryListing {
	s.directories.mu.Lock()
	defer s.directories.mu.Unlock()
	return s.directories.listing
}
func readDirectories(path string) DirectoryListing {
	result := DirectoryListing{State: "complete", Path: path, Parent: filepath.Dir(path)}
	canonical, err := filepath.EvalSymlinks(path)
	if err != nil {
		result.Error = err.Error()
		return result
	}
	if canonical != path {
		result.Error = "Use the canonical directory path: " + canonical
		return result
	}
	f, err := os.Open(path)
	if err != nil {
		result.Error = err.Error()
		return result
	}
	defer f.Close()
	entries, err := f.ReadDir(201)
	if err != nil && !errors.Is(err, io.EOF) {
		result.Error = err.Error()
		return result
	}
	if len(entries) > 200 {
		result.TooMany = true
		entries = entries[:200]
	}
	for _, entry := range entries {
		if entry.IsDir() && entry.Type()&os.ModeSymlink == 0 {
			result.Names = append(result.Names, entry.Name())
		}
	}
	return result
}
