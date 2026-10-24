package admin

import (
	"errors"
	"os"
	"os/user"
	"strconv"

	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/setup"
)

func InitiatingUser() (setup.User, error) {
	id := os.Getenv("SUDO_UID")
	if id == "" && os.Getuid() != 0 {
		id = strconv.Itoa(os.Getuid())
	}
	if id == "" {
		return setup.User{}, errors.New("run as an ordinary user; setup requests sudo itself")
	}
	u, err := user.LookupId(id)
	if err != nil {
		return setup.User{}, err
	}
	uid, e1 := strconv.ParseUint(u.Uid, 10, 32)
	gid, e2 := strconv.ParseUint(u.Gid, 10, 32)
	if e1 != nil || e2 != nil || uid == 0 || gid == 0 || !config.AbsolutePath(u.HomeDir) {
		return setup.User{}, errors.New("invalid nonroot data owner")
	}
	return setup.User{UID: uint32(uid), GID: uint32(gid), Home: u.HomeDir}, nil
}
func savedUser(a config.Attachment) (setup.User, error) {
	u, err := user.LookupId(strconv.FormatUint(uint64(a.UserUID), 10))
	if err != nil {
		return setup.User{}, err
	}
	gid, err := strconv.ParseUint(u.Gid, 10, 32)
	if err != nil || a.UserUID == 0 || a.UserGID == 0 || uint32(gid) != a.UserGID || !config.AbsolutePath(u.HomeDir) {
		return setup.User{}, errors.New("saved nonroot owner is unavailable or changed")
	}
	return setup.User{UID: a.UserUID, GID: a.UserGID, Home: u.HomeDir}, nil
}
func configuration(a config.Attachment, h *config.HostedFilesystem, pending bool) adminwire.Configuration {
	c := adminwire.Configuration{State: "configured", Role: "client", Connection: &a.Connection}
	if h != nil {
		c.Role = "server"
		c.Source = h.Source
		c.Backend = h.Backend
	}
	if pending {
		c.State = "pending"
	}
	return c
}

// Inspect reads private metadata only: never probes/traverses source/mount.
func inspect(service *setup.Service) (adminwire.Configuration, error) {
	var p setup.Plan
	if err := service.Store.Read("pending-setup.json", &p); err == nil {
		if err = p.Attachment.Validate(); err != nil {
			return adminwire.Configuration{}, err
		}
		if p.Hosted != nil {
			if err = p.Hosted.Validate(); err != nil {
				return adminwire.Configuration{}, err
			}
		}
		return configuration(p.Attachment, p.Hosted, true), nil
	} else if !os.IsNotExist(err) {
		return adminwire.Configuration{}, err
	}
	var a config.Attachment
	if err := service.Store.Read("attachment.json", &a); err != nil {
		if os.IsNotExist(err) {
			var h config.HostedFilesystem
			if err = service.Store.Read("hosted-filesystem.json", &h); !os.IsNotExist(err) {
				return adminwire.Configuration{}, errors.New("hosted state lacks its attachment; retain evidence and recover with the matching tool")
			}
			return adminwire.Configuration{State: "empty"}, nil
		}
		return adminwire.Configuration{}, err
	}
	if err := a.Validate(); err != nil {
		return adminwire.Configuration{}, err
	}
	var h config.HostedFilesystem
	if err := service.Store.Read("hosted-filesystem.json", &h); err == nil {
		if err = h.Validate(); err != nil {
			return adminwire.Configuration{}, err
		}
		if h.InstallationID != a.InstallationID || h.StorageID != a.StorageID {
			return adminwire.Configuration{}, errors.New("hosted and attachment identities differ")
		}
		return configuration(a, &h, false), nil
	} else if !os.IsNotExist(err) {
		return adminwire.Configuration{}, err
	}
	return configuration(a, nil, false), nil
}
func (s *Session) matchRole(c adminwire.Configuration) error {
	if s.role != "" && c.State != "empty" && c.Role != s.role {
		return errors.New("configured role differs; open autobyteus-nfs " + c.Role)
	}
	return nil
}
func (s *Session) InspectConfiguration() (adminwire.Configuration, error) {
	if err := s.enter(); err != nil {
		return adminwire.Configuration{}, err
	}
	defer s.mu.Unlock()
	service, err := s.acquire()
	if err != nil {
		return adminwire.Configuration{}, err
	}
	defer closeScope(service)
	return inspect(service)
}
