package config

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"strings"
)

// CheckStandaloneState is read-only admission, not migration. The caller holds
// the administrative lock. Only active host state and pending setup can carry
// outstanding predecessor node obligations; receipts/history are not scanned.
func CheckStandaloneState(s Store) error {
	for _, name := range []string{"attachment.json", "pending-setup.json"} {
		var envelope stateEnvelope
		if err := s.Read(name, &envelope); os.IsNotExist(err) {
			continue
		} else if err != nil {
			return fmt.Errorf("%s: %w", name, err)
		}
		if name == "pending-setup.json" {
			raw, ok := envelope["attachment"]
			if !ok {
				return errors.New("pending setup is missing attachment")
			}
			if err := json.Unmarshal(raw, &envelope); err != nil {
				return err
			}
		}
		if raw, ok := envelope["nodes"]; ok && !bytes.Equal(bytes.TrimSpace(raw), []byte("null")) {
			var nodes []json.RawMessage
			if err := json.Unmarshal(raw, &nodes); err != nil || len(nodes) != 0 {
				return errors.New("active node-management obligation is unsupported; drain/detach using its matching predecessor tool before installing standalone NFS")
			}
		}
		raw, err := json.Marshal(envelope)
		if err != nil {
			return err
		}
		var a Attachment
		if err := json.Unmarshal(raw, &a); err != nil {
			return err
		}
		if err := a.Validate(); err != nil {
			return err
		}
	}
	return nil
}

// Reject ambiguous/case-duplicate envelope keys rather than silently accepting
// the last node list. Unknown fields remain tolerated by current host readers.
type stateEnvelope map[string]json.RawMessage

func (s *stateEnvelope) UnmarshalJSON(data []byte) error {
	d := json.NewDecoder(bytes.NewReader(data))
	first, err := d.Token()
	if err != nil || first != json.Delim('{') {
		return errors.New("installation state must be an object")
	}
	fields := stateEnvelope{}
	for d.More() {
		token, err := d.Token()
		if err != nil {
			return err
		}
		key, ok := token.(string)
		if !ok {
			return errors.New("invalid installation state key")
		}
		key = strings.ToLower(key)
		if _, exists := fields[key]; exists {
			return errors.New("ambiguous installation state key")
		}
		var raw json.RawMessage
		if err := d.Decode(&raw); err != nil {
			return err
		}
		fields[key] = raw
	}
	if _, err := d.Token(); err != nil {
		return err
	}
	*s = fields
	return nil
}
