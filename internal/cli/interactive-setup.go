package cli

import (
	"encoding/json"
	"fmt"
	"github.com/AutoByteus/autobyteus-nfs/internal/admin"
	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/setup"
	"os"
)

func runSetup(o Options, terminal *Terminal, session *admin.Session) error {
	u, err := admin.InitiatingUser()
	if err != nil {
		return err
	}
	req, err := collect(o, terminal)
	if err != nil {
		return err
	}
	var review adminwire.Review
	if o.Action == "create" {
		if req.Backend == "ganesha-docker" {
			req.DockerSocket = socketFor(o, u)
		}
		review, err = session.BeginServer(adminwire.ServerInput{Source: req.Source, Endpoint: req.Connection.Endpoint, Allowlist: req.Allowlist, Backend: req.Backend, MountRoot: req.Connection.MountRoot, DockerSocket: req.DockerSocket})
	} else {
		data, e := json.Marshal(req.Connection)
		if e != nil {
			return e
		}
		review, err = session.BeginClient(adminwire.ClientInput{Connection: string(data)})
	}
	if err != nil {
		return err
	}
	fmt.Fprintln(os.Stderr, "AutoByteus NFS plan:")
	for _, line := range review.Summary {
		fmt.Fprintln(os.Stderr, " -", line)
	}
	consent := o.Yes || terminal.Confirm("Apply this exact source/network/service plan?")
	result, err := session.Commit(adminwire.CommitInput{LeaseID: review.LeaseID, Consent: consent})
	if result.Status == nil {
		return err
	}
	if o.JSON {
		printJSON(struct {
			Connection config.Connection `json:"connection"`
			Status     setup.Status      `json:"status"`
		}{*review.Configuration.Connection, *result.Status})
	} else if err != nil {
		printJSON(result.Status)
	} else {
		fmt.Fprintln(os.Stderr, "Verified host workspace path:", review.Configuration.Connection.MountRoot, "\nSelect a project below this path. Keep storage online. Connection JSON for other computers:")
		printJSON(review.Configuration.Connection)
	}
	return err
}
