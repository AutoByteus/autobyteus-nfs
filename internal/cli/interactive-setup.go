package cli

import (
	"fmt"
	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/docker"
	"github.com/AutoByteus/autobyteus-nfs/internal/setup"
	"os"
)

func runSetup(o Options, terminal *Terminal, s *setup.Service) error {
	u, err := initiatingUser()
	if err != nil {
		return err
	}
	s.User = u
	req, err := collect(o, terminal)
	if err != nil {
		return err
	}
	if req.Backend == "ganesha-docker" {
		req.DockerSocket = socketFor(o, u)
		s.Docker, err = docker.New(req.DockerSocket)
		if err != nil {
			return err
		}
		defer s.Docker.Close()
	}
	p, err := s.Plan(req)
	if err != nil {
		return err
	}
	fmt.Fprintln(os.Stderr, "AutoByteus NFS plan:")
	for _, line := range p.Summary {
		fmt.Fprintln(os.Stderr, " -", line)
	}
	consent := o.Yes || terminal.Confirm("Apply this exact source/network/service plan?")
	if err = s.Apply(p, consent); err != nil {
		return err
	}
	fmt.Fprintln(os.Stderr, "Checking actual host readiness; this may wait for storage.")
	result, err := s.Status()
	if o.JSON {
		printJSON(struct {
			Connection config.Connection `json:"connection"`
			Status     setup.Status      `json:"status"`
		}{p.Attachment.Connection, result})
	} else if err != nil {
		printJSON(result)
	} else {
		fmt.Fprintln(os.Stderr, "Verified host workspace path:", p.Attachment.MountRoot, "\nSelect a project below this path. Keep storage online. Connection JSON for other computers:")
		printJSON(p.Attachment.Connection)

	}
	return err
}
