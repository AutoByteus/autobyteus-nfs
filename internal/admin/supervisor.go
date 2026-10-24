package admin

import (
	"context"
	"fmt"
	"io"
)

// Supervise owns the entire serial attempt and completion-relative retry. Stop
// drains the current attempt; no context cancels administrative children.
func (s *Session) Supervise(ctx context.Context, log io.Writer) error {
	for {
		if ctx.Err() != nil {
			return nil
		}
		err := s.reconcileOnce()
		if err != nil {
			fmt.Fprintf(log, "AutoByteus NFS checking/incomplete: %v\n", err)
		}
		if ctx.Err() != nil {
			return nil
		}
		select {
		case <-ctx.Done():
			return nil
		case <-s.wait():
		}
	}
}
func (s *Session) reconcileOnce() error {
	if err := s.enter(); err != nil {
		return err
	}
	defer s.mu.Unlock()
	service, err := s.acquire()
	if err != nil {
		return err
	}
	defer closeScope(service)
	s.savedDocker(service)
	return s.reconnectActiveLocked(service)
}
