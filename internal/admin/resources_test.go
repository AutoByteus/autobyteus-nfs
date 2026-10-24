package admin

import (
	"errors"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
	"github.com/AutoByteus/autobyteus-nfs/internal/docker"
)

func TestOwnedDockerScopeClosesOnReviewAndFailure(t *testing.T) {
	for _, mode := range []string{"cancel-review", "prepare-failure", "supervisor-failure", "daemon-open-failure"} {
		t.Run(mode, func(t *testing.T) {
			s := testSession(t)
			dir, err := os.MkdirTemp("", "nfs-dock-")
			if err != nil {
				t.Fatal(err)
			}
			defer os.RemoveAll(dir)
			// Keep AF_UNIX name within the OS bound, independent of long test names.
			socket := filepath.Join(dir, "d.sock")
			listener, err := net.Listen("unix", socket)
			if err != nil {
				t.Fatal(err)
			}
			closed := make(chan struct{}, 4)
			server := &http.Server{Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) { w.Write([]byte(`{}`)) }), ConnState: func(_ net.Conn, state http.ConnState) {
				if state == http.StateClosed {
					closed <- struct{}{}
				}
			}}
			go server.Serve(listener)
			defer server.Close()
			opens := 0
			s.openDocker = func(path string) (*docker.Client, error) {
				opens++
				if path != socket {
					t.Fatal("changed socket", path)
				}
				if mode == "daemon-open-failure" {
					return nil, errors.New("controlled unavailable daemon")
				}
				c, err := docker.New(path)
				if err != nil {
					return nil, err
				}
				// Establish a real idle Unix HTTP connection; Close must actually release it.
				if err = c.Call("GET", "/_ping", nil, nil); err != nil {
					c.Close()
					return nil, err
				}
				return c, nil
			}
			save(t, s, "docker-endpoint.json", struct {
				Socket string `json:"socket"`
			}{socket})
			if mode == "prepare-failure" || mode == "daemon-open-failure" {
				if _, err = s.BeginServer(adminwire.ServerInput{Source: "/", Backend: "ganesha-docker", DockerSocket: socket}); err == nil {
					t.Fatal("invalid source unexpectedly planned")
				}
			} else {
				save(t, s, "attachment.json", attachment())
				if mode == "cancel-review" {
					r, err := s.BeginDetach()
					if err != nil {
						t.Fatal(err)
					}
					if err = s.CancelReview(r.LeaseID); err != nil {
						t.Fatal(err)
					}
				} else if err = s.reconcileOnce(); err == nil {
					t.Fatal("controlled observation failure ignored")
				}
			}
			if opens != 1 {
				t.Fatal("saved daemon not scoped exactly once", opens)
			}
			if mode != "daemon-open-failure" {
				select {
				case <-closed:
				case <-time.After(time.Second):
					t.Fatal("idle daemon connection leaked")
				}
			}
			unlocked(t, s)
			s.Close()
			select {
			case <-closed:
				t.Fatal("duplicate close/extra connection")
			default:
			}
		})
	}
}
