package cli

import (
	"errors"
	"flag"
	"fmt"
	"net"
	"os"
	"path/filepath"
	"runtime"
	"strings"

	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/setup"
)

type Options struct {
	Action, Source, Endpoint, Allow, Root, Backend, Connection, Socket string
	Yes, Drained, JSON                                                 bool
}

func Parse(args []string) (Options, error) {
	var o Options
	if len(args) > 0 && !strings.HasPrefix(args[0], "-") {
		o.Action = args[0]
		args = args[1:]
	}
	if o.Action == "server" || o.Action == "client" {
		if len(args) != 0 {
			return o, errors.New("server/client dashboard launches accept no flags or additional arguments")
		}
		return o, nil
	}
	f := flag.NewFlagSet("autobyteus-nfs", flag.ContinueOnError)
	f.StringVar(&o.Source, "source", "", "chosen source folder (existing files stay in place)")
	f.StringVar(&o.Endpoint, "endpoint", "", "private IPv4 reachable by all clients")
	f.StringVar(&o.Allow, "allow", "", "comma-separated trusted private hosts/subnets")
	f.StringVar(&o.Root, "mount-root", "", "actual client root")
	f.StringVar(&o.Backend, "backend", "", "apple, ganesha-native, ganesha-docker")
	f.StringVar(&o.Connection, "connection", "", "nonsecret printed connection JSON")
	f.StringVar(&o.Socket, "docker-socket", "", "selected local Unix daemon socket")
	f.BoolVar(&o.Yes, "yes", false, "explicit setup administration consent")
	f.BoolVar(&o.Drained, "drained", false, "export/mount users are drained and interruption approved")
	f.BoolVar(&o.JSON, "json", false, "structured result")
	if err := f.Parse(args); err != nil {
		return o, err
	}
	if f.NArg() != 0 {
		return o, errors.New("unexpected arguments")
	}
	switch o.Action {
	case "", "create", "connect", "status", "reconnect", "detach", "version", "service":
	default:
		return o, errors.New("unknown action")
	}
	return o, nil
}
func parseOSRelease(data string) map[string]string {
	m := map[string]string{}
	for _, line := range strings.Split(data, "\n") {
		parts := strings.SplitN(line, "=", 2)
		if len(parts) == 2 {
			m[parts[0]] = strings.Trim(parts[1], `"`)
		}
	}
	return m
}
func privateAddresses() []string {
	result := []string{}
	addresses, err := net.InterfaceAddrs()
	if err != nil {
		return result
	}
	for _, a := range addresses {
		ip, _, err := net.ParseCIDR(a.String())
		if err == nil && ip.To4() != nil && ip.IsPrivate() {
			result = append(result, ip.String())
		}
	}
	return result
}
func socketFor(o Options, u setup.User) string {
	if o.Socket != "" {
		return o.Socket
	}
	paths := []string{"/var/run/docker.sock"}
	if runtime.GOOS == "darwin" {
		paths = append(paths, filepath.Join(u.Home, ".docker", "run", "docker.sock"))
	}
	for _, p := range paths {
		if info, err := os.Stat(p); err == nil && info.Mode()&os.ModeSocket != 0 {
			return p
		}
	}
	return ""
}
func collect(o Options, t *Terminal) (setup.Request, error) {
	var req setup.Request
	var err error
	ask := func(value *string, label, def string) {
		if err == nil && *value == "" {
			if !t.Available() && def != "" {
				*value = def
				return
			}
			*value, err = t.Ask(label, def)
		}
	}
	if o.Action == "create" {
		ask(&o.Source, "Source folder to share (NOT your home/private app folder)", "")
		defaults := "ganesha-native"
		if runtime.GOOS == "darwin" {
			defaults = "apple"
		}
		ask(&o.Backend, "Storage mode", defaults)
		addresses := privateAddresses()
		fmt.Fprintln(os.Stderr, "Detected private addresses:", strings.Join(addresses, ", "))
		endpointDefault := ""
		if len(addresses) == 1 {
			endpointDefault = addresses[0]
		}
		ask(&o.Endpoint, "Private IPv4 reachable from every computer and Docker daemon", endpointDefault)
		ask(&o.Allow, "Trusted private hosts/subnets (plaintext; comma-separated)", "")
		req.Source = o.Source
		req.Backend = o.Backend
		req.Allowlist = strings.Split(o.Allow, ",")
		req.Connection.Endpoint = o.Endpoint
	} else {
		ask(&o.Connection, "Paste storage connection JSON", "")
		if err == nil {
			req.Connection, err = config.ParseConnection([]byte(o.Connection))
		}
	}
	rootDefault := req.Connection.MountRoot
	if rootDefault == "" {
		rootDefault = config.DefaultMountRoot
	}
	ask(&o.Root, "Mount root (occupied contents are never hidden)", rootDefault)
	req.Connection.MountRoot = o.Root
	if err != nil {
		return req, err
	}
	return req, nil
}
