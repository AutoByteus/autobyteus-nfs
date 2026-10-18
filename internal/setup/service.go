package setup

import (
	"github.com/AutoByteus/autobyteus-nfs/internal/backend"
	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/docker"
	"github.com/AutoByteus/autobyteus-nfs/internal/platform"
	"os"
)

type User struct {
	UID, GID uint32
	Home     string
}
type Request struct {
	Connection   config.Connection
	Source       string
	Backend      string
	Allowlist    []string
	DockerSocket string
}
type Plan struct {
	Attachment   config.Attachment
	Hosted       *config.HostedFilesystem
	Apple        *backend.ApplePlan
	DockerSocket string
	NewSource    bool
	Summary      []string
}
type FieldValidation struct {
	Filesystem string `json:"filesystem"`
	User       string `json:"user"`
}
type Release struct {
	Schema          int                     `json:"schema"`
	FieldValidation FieldValidation         `json:"fieldValidation"`
	Engine          *backend.EngineManifest `json:"engine,omitempty"`
	SourceHash      string                  `json:"sourceHash"`
	ReleaseTargets  []string                `json:"releaseTargets"`
	Version         string                  `json:"version"`
	Packages        map[string]string       `json:"ubuntuPackages"`
	EngineImage     string                  `json:"engineImage"`
}
type Service struct {
	Lock    *os.File
	Store   config.Store
	Runner  platform.Runner
	Binary  string
	Release Release
	User    User
	Docker  *docker.Client
}
