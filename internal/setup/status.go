package setup

import (
	"errors"

	"github.com/AutoByteus/autobyteus-nfs/internal/backend"
	"github.com/AutoByteus/autobyteus-nfs/internal/platform"
	"github.com/AutoByteus/autobyteus-nfs/internal/service"
)

type Status struct {
	StorageID  string `json:"storageId"`
	Root       string `json:"mountRoot"`
	HostReady  bool   `json:"hostReady"`
	Limitation string `json:"limitation"`
}

func (s *Service) Status() (Status, error) {
	result := Status{Limitation: "Hard NFS checks may stall; no outage deadline or local substitute"}
	a, h, err := s.CheckConfiguration()
	if err != nil {
		return result, err
	}
	if h != nil && (h.Backend == "ganesha-native" || h.Backend == "ganesha-docker") {
		if err = backend.VerifyGanesha(*h, s.Store.Directory, h.Backend == "ganesha-docker"); err != nil {
			return result, err
		}
	}
	result.StorageID = a.StorageID
	result.Root = a.MountRoot
	m, err := platform.Observe(s.Runner, a.Connection)
	if err != nil {
		return result, err
	}
	if !platform.Matches(m, a.Connection) {
		return result, errors.New("expected host NFS source/protocol is not mounted")
	}
	if err = service.NonrootProbe(s.Binary, a.MountRoot, a.StorageID, a.UserUID, a.UserGID, false, s.Lock); err != nil {
		return result, err
	}
	result.HostReady = true
	return result, nil
}
