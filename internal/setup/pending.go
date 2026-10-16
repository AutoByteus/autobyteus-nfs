package setup

import (
	"errors"
	"os"

	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/platform"
)

// Pending setup is an intended-resource receipt, not persisted readiness. Resume
// needs a fresh displayed plan and consent; the supervisor never resumes setup.
func (s *Service) PendingPlan() (Plan, error) {
	if err := config.CheckStandaloneState(s.Store); err != nil {
		return Plan{}, err
	}
	var p Plan
	if err := s.Store.Read("pending-setup.json", &p); err != nil {
		return p, err
	}
	if err := p.Attachment.Validate(); err != nil {
		return p, err
	}
	if err := validateSourceIntent(p); err != nil {
		return p, err
	}
	if p.Hosted != nil {
		if p.Hosted.Identity != (config.Identity{}) {
			if err := platform.CheckSource(s.Runner, *p.Hosted); err != nil {
				return p, err
			}
			p.NewSource = false
		} else {
			// Zero is an unbound intent, never permission to rebind hosted state.
			if err := platform.ValidateSourcePath(p.Hosted.Source, p.Attachment.MountRoot, s.User.Home); err != nil {
				return p, err
			}
			if err := s.checkUnboundSource(); err != nil {
				return p, err
			}
			id, err := platform.SourceIdentity(s.Runner, p.Hosted.Source)
			if err == nil {
				p.Hosted.Identity = id
				p.NewSource = false
				if err := p.Hosted.ValidateBound(); err != nil {
					return p, err
				}
			} else if !os.IsNotExist(err) {
				return p, err
			}
		}
	}
	return p, nil
}

func (s *Service) SaveIntent(p Plan) error {
	if err := s.Store.Write("pending-setup.json", p); err != nil {
		return err
	}
	if err := s.Store.Write("docker-endpoint.json", struct {
		Socket string `json:"socket"`
	}{p.DockerSocket}); err != nil {
		return err
	}
	return nil
}

// Only a genuinely new, completely zero binding may await source creation.
func validateSourceIntent(p Plan) error {
	if p.Hosted == nil {
		return nil
	}
	if err := p.Hosted.Validate(); err != nil {
		return err
	}
	if p.NewSource && p.Hosted.Identity == (config.Identity{}) {
		return nil
	}
	return p.Hosted.ValidateBound()
}

func (s *Service) checkUnboundSource() error {
	var hosted config.HostedFilesystem
	if err := s.Store.Read("hosted-filesystem.json", &hosted); err == nil {
		return errors.New("unbound pending source conflicts with hosted state")
	} else if !os.IsNotExist(err) {
		return err
	}
	return nil
}
