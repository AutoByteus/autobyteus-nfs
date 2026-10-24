package cli

import (
	"context"
	"errors"
	"os"
	"os/exec"
	"os/signal"
	"path/filepath"
	"syscall"

	"github.com/AutoByteus/autobyteus-nfs/internal/admin"
	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/dashboard"
	"github.com/AutoByteus/autobyteus-nfs/internal/setup"
)

func runDashboardHelper(args []string, release setup.Release) error {
	if os.Geteuid() != 0 || len(args) != 1 || (args[0] != "server" && args[0] != "client") {
		return errors.New("invalid private dashboard helper invocation")
	}
	if err := CheckHost(); err != nil {
		return err
	}
	executable, err := os.Executable()
	if err != nil {
		return err
	}
	executable, err = filepath.EvalSymlinks(executable)
	if err != nil {
		return err
	}
	installed, err := filepath.EvalSymlinks(config.BinaryPath())
	if err != nil {
		return err
	}
	if executable != installed {
		return errors.New("private helper requires the root-installed control executable")
	}
	for _, f := range []*os.File{os.Stdin, os.Stdout} {
		info, err := f.Stat()
		if err != nil {
			return err
		}
		if info.Mode()&os.ModeNamedPipe == 0 {
			return errors.New("private helper requires inherited anonymous pipes")
		}
	}
	user, err := admin.InitiatingUser()
	if err != nil {
		return err
	}
	session, err := admin.New(release, user, args[0])
	if err != nil {
		return err
	}
	// Scope SIGPIPE handling to this process entry only. Go's default handling of
	// broken stdout can exit immediately; EPIPE must instead drain admitted work.
	broken := make(chan os.Signal, 1)
	signal.Notify(broken, syscall.SIGPIPE)
	defer signal.Stop(broken)
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()
	defer os.Stdin.Close()
	return session.ServePipe(ctx, os.Stdin, os.Stdout)
}

func dashboardLauncher(role string) (*exec.Cmd, string, error) {
	terminal := OpenTerminal()
	defer terminal.Close()
	if os.Geteuid() == 0 || !terminal.Available() {
		return nil, "", errors.New("launch dashboard as an ordinary user in a terminal; administrator approval stays in that terminal")
	}
	executable, err := os.Executable()
	if err != nil {
		return nil, "", err
	}
	executable, err = filepath.EvalSymlinks(executable)
	if err != nil {
		return nil, "", err
	}
	digest, err := admin.Digest(executable)
	if err != nil {
		return nil, "", err
	}
	// Only the exact parsed role is appended; no browser-controlled process argv.
	cmd := exec.Command("/usr/bin/sudo", "--", executable, "internal-install", "internal-dashboard-helper", role)
	cmd.Stderr = os.Stderr
	return cmd, digest, nil
}

func runDashboard(role string) error {
	terminal := OpenTerminal()
	defer terminal.Close()
	if os.Geteuid() == 0 || !terminal.Available() {
		return errors.New("launch server/client as an ordinary user in a terminal, not under sudo")
	}
	session, err := dashboard.New(role, func() (*exec.Cmd, string, error) { return dashboardLauncher(role) })
	if err != nil {
		return err
	}
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()
	return session.Run(ctx, os.Stderr)
}
