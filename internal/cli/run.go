package cli

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/AutoByteus/autobyteus-nfs/internal/admin"
	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/platform"
	"github.com/AutoByteus/autobyteus-nfs/internal/service"
	"github.com/AutoByteus/autobyteus-nfs/internal/setup"
)

func Run(args []string, release setup.Release) error {
	if len(args) > 0 {
		switch args[0] {
		case "verify-release":
			if len(args) != 2 {
				return errors.New("verify-release requires manifest path")
			}
			if err := VerifyRelease(args[1], release); err != nil {
				return err
			}
			fmt.Fprintln(os.Stderr, "Shared-filesystem/physical and user testing is deferred; distribution and signature checks are not field qualification.")
			return nil
		case "internal-dashboard-helper":
			return runDashboardHelper(args[1:], release)
		case "internal-install":
			return InstallRoot(args[1:])
		case "internal-probe":
			if os.Geteuid() == 0 || len(args) < 3 || len(args) > 4 {
				return errors.New("invalid nonroot probe")
			}
			return service.Probe(args[1], args[2], len(args) == 4 && args[3] == "initialize")
		case "internal-create-source":
			if os.Geteuid() == 0 || len(args) != 2 || !config.AbsolutePath(args[1]) {
				return errors.New("invalid source creation")
			}
			return os.Mkdir(args[1], 0750)
		case "internal-handles":
			if os.Geteuid() != 0 || len(args) != 2 {
				return errors.New("invalid source qualification")
			}
			return platform.QualifyHandles(args[1])
		}
	}
	o, err := Parse(args)
	if err != nil {
		return err
	}
	if o.Action == "version" {
		fmt.Fprintln(os.Stdout, release.Version)
		return nil
	}
	if err = CheckHost(); err != nil {
		return err
	}
	if o.Action == "server" || o.Action == "client" {
		return runDashboard(o.Action)
	}
	terminal := OpenTerminal()
	defer terminal.Close()
	if os.Geteuid() != 0 {
		if !o.Yes && !terminal.Confirm("Install/use the root-owned AutoByteus NFS control binary and request OS administrator approval? Storage changes get a separate plan") {
			return errors.New("administrator setup declined")
		}
		return Elevate(args)
	}
	session, err := admin.New(release, setup.User{}, "")
	if err != nil {
		return err
	}
	defer session.Close()
	if o.Action == "service" {
		ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
		defer stop()
		return session.Supervise(ctx, os.Stderr)
	}
	if o.Action == "" {
		current, e := session.InspectConfiguration()
		if e != nil {
			return e
		}
		switch current.State {
		case "pending":
			o.Action, err = terminal.Ask("Setup is incomplete: review/retry saved setup (reconnect)", "reconnect")
		case "configured":
			o.Action, err = terminal.Ask("Configured storage: status / reconnect / detach", "status")
		default:
			o.Action, err = terminal.Ask("Create storage or connect to existing storage (create/connect)", "")
		}
		if err != nil {
			return err
		}
	}
	switch o.Action {
	case "status":
		fmt.Fprintln(os.Stderr, "Checking actual host readiness; this may wait for storage.")
		result, e := session.CheckReadiness()
		if result.Status != nil {
			printJSON(result.Status)
		}
		return e
	case "reconnect", "detach":
		var review adminwire.Review
		if o.Action == "reconnect" {
			review, err = session.BeginReconnect()
		} else {
			review, err = session.BeginDetach()
		}
		if err != nil {
			return err
		}
		for _, line := range review.Summary {
			fmt.Fprintln(os.Stderr, " -", line)
		}
		consent := o.Yes
		if o.Action == "detach" {
			consent = o.Yes && o.Drained
		}
		if !consent {
			prompt := "Reconnect saved host storage?"
			if review.Kind == "resume" {
				prompt = "Apply this saved setup plan now?"
			}
			if o.Action == "detach" {
				prompt = "Drain all users of this export/attachment and permit their interruption and safe detach? Source, marker and private data remain"
			}
			consent = terminal.Confirm(prompt)
		}
		if !consent {
			return errors.New(o.Action + " declined; no changes")
		}
		result, e := session.Commit(adminwire.CommitInput{LeaseID: review.LeaseID, Consent: true, Drained: o.Action == "detach"})
		if o.Action == "detach" {
			if e == nil {
				if result.Retained != "" {
					fmt.Fprintln(os.Stderr, result.Retained)
				}
				fmt.Fprintln(os.Stderr, "Detached; source, marker, private receipts preserved.")
			}
			return e
		}
		if result.Status != nil {
			printJSON(result.Status)
		}
		return e
	case "create", "connect":
		return runSetup(o, terminal, session)
	default:
		return errors.New("choose create or connect")
	}
}
func printJSON(v any) {
	b, err := json.MarshalIndent(v, "", "  ")
	if err == nil {
		fmt.Fprintln(os.Stdout, string(b))
	}
}
