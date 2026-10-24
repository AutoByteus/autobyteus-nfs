// Package adminwire defines the private, same-binary management transport.
// These projections are never persisted or accepted as setup authority.
package adminwire

import (
	"time"

	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/setup"
)

type ServerInput struct {
	Source       string   `json:"source"`
	Endpoint     string   `json:"endpoint"`
	Allowlist    []string `json:"allowlist"`
	Backend      string   `json:"backend"`
	MountRoot    string   `json:"mountRoot"`
	DockerSocket string   `json:"dockerSocket"`
}
type ClientInput struct {
	Connection string `json:"connection"`
	MountRoot  string `json:"mountRoot"`
}
type Configuration struct {
	State      string             `json:"state"`
	Role       string             `json:"role,omitempty"`
	Connection *config.Connection `json:"connection,omitempty"`
	Source     string             `json:"source,omitempty"`
	Backend    string             `json:"backend,omitempty"`
}
type Review struct {
	LeaseID       string        `json:"leaseId"`
	Kind          string        `json:"kind"`
	ExpiresAt     time.Time     `json:"expiresAt"`
	Summary       []string      `json:"summary"`
	Configuration Configuration `json:"configuration"`
}
type CommitInput struct {
	LeaseID string `json:"leaseId"`
	Consent bool   `json:"consent"`
	Drained bool   `json:"drained"`
}
type Result struct {
	Configuration         *Configuration `json:"configuration,omitempty"`
	Status                *setup.Status  `json:"status,omitempty"`
	CheckedAt             *time.Time     `json:"checkedAt,omitempty"`
	Retained              string         `json:"retained,omitempty"`
	EffectsMayHaveStarted bool           `json:"effectsMayHaveStarted"`
}
