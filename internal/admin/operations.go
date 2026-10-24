package admin

import (
	"encoding/json"
	"errors"
	"fmt"
	"time"

	"github.com/AutoByteus/autobyteus-nfs/internal/adminwire"
	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/platform"
	"github.com/AutoByteus/autobyteus-nfs/internal/setup"
)

func (s *Session) BeginServer(in adminwire.ServerInput) (adminwire.Review, error) {
	if s.role == "client" {
		return adminwire.Review{}, errors.New("client dashboard cannot create storage")
	}
	if in.Source == "" {
		return adminwire.Review{}, errors.New("source folder required")
	}
	return s.beginSetup(setup.Request{Source: in.Source, Backend: in.Backend, Allowlist: in.Allowlist, DockerSocket: in.DockerSocket, Connection: config.Connection{Endpoint: in.Endpoint, MountRoot: in.MountRoot}})
}
func (s *Session) BeginClient(in adminwire.ClientInput) (adminwire.Review, error) {
	if s.role == "server" {
		return adminwire.Review{}, errors.New("server dashboard cannot connect as client")
	}
	c, err := config.ParseConnection([]byte(in.Connection))
	if err != nil {
		return adminwire.Review{}, err
	}
	if in.MountRoot != "" {
		c.MountRoot = in.MountRoot
	}
	return s.beginSetup(setup.Request{Connection: c})
}
func (s *Session) beginSetup(req setup.Request) (adminwire.Review, error) {
	if err := s.enter(); err != nil {
		return adminwire.Review{}, err
	}
	defer s.mu.Unlock()
	service, err := s.acquire()
	if err != nil {
		return adminwire.Review{}, err
	}
	defer func() {
		if s.lease == nil {
			closeScope(service)
		}
	}()
	if service.User.UID == 0 {
		service.User, err = InitiatingUser()
		if err != nil {
			return adminwire.Review{}, err
		}
	}
	if req.Backend == "ganesha-docker" {
		service.Docker, err = s.openDocker(req.DockerSocket)
		if err != nil {
			return adminwire.Review{}, err
		}
	}
	plan, err := service.Plan(req)
	if err != nil {
		return adminwire.Review{}, err
	}
	return s.retain(service, "setup", plan, plan.Summary, configuration(plan.Attachment, plan.Hosted, false))
}
func (s *Session) retain(service *setup.Service, kind string, plan setup.Plan, summary []string, c adminwire.Configuration) (adminwire.Review, error) {
	id, err := config.NewID()
	if err != nil {
		return adminwire.Review{}, err
	}
	review := adminwire.Review{LeaseID: id, Kind: kind, ExpiresAt: time.Now().Add(reviewLifetime), Summary: summary, Configuration: c}
	b, err := json.Marshal(review)
	if err != nil {
		return adminwire.Review{}, err
	}
	if len(b) > 32<<10 {
		return adminwire.Review{}, errors.New("review exceeds display bound; no truncated plan may be approved")
	}
	l := &lease{id: id, kind: kind, expires: review.ExpiresAt, plan: plan, service: service}
	s.lease = l
	l.timer = time.AfterFunc(reviewLifetime, func() {
		s.mu.Lock()
		defer s.mu.Unlock()
		if s.lease == l {
			s.releaseReview()
		}
	})
	return review, nil
}
func (s *Session) BeginReconnect() (adminwire.Review, error) { return s.beginExisting("reconnect") }
func (s *Session) BeginDetach() (adminwire.Review, error)    { return s.beginExisting("detach") }
func (s *Session) beginExisting(kind string) (adminwire.Review, error) {
	if err := s.enter(); err != nil {
		return adminwire.Review{}, err
	}
	defer s.mu.Unlock()
	service, err := s.acquire()
	if err != nil {
		return adminwire.Review{}, err
	}
	defer func() {
		if s.lease == nil {
			closeScope(service)
		}
	}()
	c, err := inspect(service)
	if err != nil {
		return adminwire.Review{}, err
	}
	if c.State == "empty" {
		return adminwire.Review{}, errors.New("storage is not configured")
	}
	if err = s.matchRole(c); err != nil {
		return adminwire.Review{}, err
	}
	s.savedDocker(service)
	var plan setup.Plan
	summary := []string{fmt.Sprintf("%s saved host attachment %s:%s at %s", kind, c.Connection.Endpoint, c.Connection.Export, c.Connection.MountRoot), "Hard NFS may wait for storage; this is not data recovery"}
	if kind == "reconnect" && c.State == "pending" {
		if err = service.Store.Read("pending-setup.json", &plan); err != nil {
			return adminwire.Review{}, err
		}
		service.User, err = savedUser(plan.Attachment)
		if err != nil {
			return adminwire.Review{}, err
		}
		plan, err = service.PendingPlan()
		if err != nil {
			return adminwire.Review{}, err
		}
		kind = "resume"
		summary = plan.Summary
	} else if kind == "detach" {
		summary = append(summary, "Drain all users and permit interruption; no forced unmount. Source, marker and private recovery data remain.")
		if c.Role == "server" {
			summary = append(summary, "Stop ALL remote users of export "+c.Source+" first; this program cannot discover or prove their drain.")
		}
	}
	return s.retain(service, kind, plan, summary, c)
}
func (s *Session) CancelReview(id string) error {
	if err := s.enter(); err != nil {
		return err
	}
	defer s.mu.Unlock()
	if s.lease == nil || s.lease.id != id {
		return errors.New("review expired, cancelled or consumed")
	}
	s.releaseReview()
	return nil
}
func (s *Session) Commit(in adminwire.CommitInput) (adminwire.Result, error) {
	var result adminwire.Result
	if err := s.enter(); err != nil {
		return result, err
	}
	defer s.mu.Unlock()
	l := s.lease
	if l == nil || l.id != in.LeaseID {
		return result, errors.New("review expired, cancelled or consumed")
	}
	if !time.Now().Before(l.expires) {
		s.releaseReview()
		return result, errors.New("review expired; request a fresh plan")
	}
	if !in.Consent || (l.kind == "detach" && !in.Drained) {
		return result, errors.New("explicit plan consent and required drain acknowledgment are missing")
	}
	l.timer.Stop()
	s.lease = nil // consume before any effect; no replay, including errors
	defer closeScope(l.service)
	if err := s.admit(l.service.Binary, s.digest); err != nil {
		return result, err
	}
	result.EffectsMayHaveStarted = true
	var err error
	switch l.kind {
	case "setup", "resume":
		err = l.service.Apply(l.plan, true)
	case "reconnect":
		err = s.reconnectActiveLocked(l.service)
		if err == nil {
			err = platform.InstallJob(l.service.Runner)
		}
	case "detach":
		err = l.service.Detach(true)
		if err == nil {
			var receipt struct {
				Retained string `json:"retained"`
			}
			_ = l.service.Store.Read("apple-detach-receipt.json", &receipt)
			result.Retained = receipt.Retained
			result.Configuration = &adminwire.Configuration{State: "empty"}
			return result, nil
		}
	}
	// Read metadata even after effects fail; never imply an apply was rolled back.
	if c, e := inspect(l.service); e == nil {
		result.Configuration = &c
	}
	if err != nil {
		return result, err
	}
	result.Status, result.CheckedAt, err = checkReadiness(l.service)
	return result, err
}
func checkReadiness(service *setup.Service) (*setup.Status, *time.Time, error) {
	status, err := service.Status()
	now := time.Now()
	return &status, &now, err
}
func (s *Session) CheckReadiness() (adminwire.Result, error) {
	var r adminwire.Result
	if err := s.enter(); err != nil {
		return r, err
	}
	defer s.mu.Unlock()
	service, err := s.acquire()
	if err != nil {
		return r, err
	}
	defer closeScope(service)
	c, err := inspect(service)
	if err != nil {
		return r, err
	}
	r.Configuration = &c
	if err = s.matchRole(c); err != nil {
		return r, err
	}
	s.savedDocker(service)
	r.Status, r.CheckedAt, err = checkReadiness(service)
	return r, err
}

// Called only with the caller's single operation scope already held.
func (s *Session) reconnectActiveLocked(service *setup.Service) error { return service.Reconnect() }
