package adminwire

import (
	"bufio"
	"bytes"
	"encoding/json"
	"errors"
	"io"
)

const Version = 1
const RequestLimit = 32 << 10
const ReplyLimit = 64 << 10

type Request struct {
	Version int             `json:"version"`
	ID      uint64          `json:"id"`
	Kind    string          `json:"kind"`
	Payload json.RawMessage `json:"payload"`
}
type Reply struct {
	Version int             `json:"version"`
	ID      uint64          `json:"id"`
	Kind    string          `json:"kind"`
	Data    json.RawMessage `json:"data,omitempty"`
	Error   *Failure        `json:"error,omitempty"`
}
type Failure struct {
	Code                  string `json:"code"`
	Detail                string `json:"detail"`
	Truncated             bool   `json:"truncated"`
	EffectsMayHaveStarted bool   `json:"effectsMayHaveStarted"`
}
type Hello struct {
	Role   string `json:"role"`
	Digest string `json:"digest"`
}
type LeaseInput struct {
	LeaseID string `json:"leaseId"`
}

// Decode is deliberately strict only at the new transport boundary. Installed
// config.Decode continues to tolerate irrelevant additive fields.
func Decode(data []byte, target any) error {
	if len(data) == 0 || bytes.Equal(bytes.TrimSpace(data), []byte("null")) {
		return errors.New("JSON object required")
	}
	d := json.NewDecoder(bytes.NewReader(data))
	if err := value(d, 0); err != nil {
		return err
	}
	if _, err := d.Token(); err != io.EOF {
		return errors.New("trailing JSON")
	}
	d = json.NewDecoder(bytes.NewReader(data))
	d.DisallowUnknownFields()
	return d.Decode(target)
}
func value(d *json.Decoder, depth int) error {
	if depth > 32 {
		return errors.New("JSON nesting exceeds bound")
	}
	tok, err := d.Token()
	if err != nil {
		return err
	}
	delimiter, ok := tok.(json.Delim)
	if !ok {
		return nil
	}
	switch delimiter {
	case '{':
		seen := map[string]bool{}
		for d.More() {
			key, err := d.Token()
			if err != nil {
				return err
			}
			name, ok := key.(string)
			if !ok || seen[name] {
				return errors.New("duplicate or invalid JSON key")
			}
			seen[name] = true
			if err = value(d, depth+1); err != nil {
				return err
			}
		}
	case '[':
		for d.More() {
			if err = value(d, depth+1); err != nil {
				return err
			}
		}
	default:
		return errors.New("unexpected JSON delimiter")
	}
	_, err = d.Token()
	return err
}

// NewReader limits memory before parsing, not after an unbounded ReadString.
func NewReader(r io.Reader, limit int) *bufio.Scanner {
	scanner := bufio.NewScanner(r)
	scanner.Buffer(make([]byte, 4096), limit+1)
	return scanner
}
func Write(w io.Writer, v any, limit int) error {
	b, err := json.Marshal(v)
	if err != nil {
		return err
	}
	if len(b) > limit {
		return errors.New("transport response exceeds bound")
	}
	b = append(b, '\n')
	n, err := w.Write(b)
	if err == nil && n != len(b) {
		err = io.ErrShortWrite
	}
	return err
}

// Input selects one typed payload; no mostly-optional command object exists.
func Input(request Request) (any, error) {
	var input any
	switch request.Kind {
	case "beginServer":
		input = &ServerInput{}
	case "beginClient":
		input = &ClientInput{}
	case "commit":
		input = &CommitInput{}
	case "cancelReview":
		input = &LeaseInput{}
	case "inspect", "checkReadiness", "beginReconnect", "beginDetach", "close":
		input = &struct{}{}
	default:
		return nil, errors.New("unknown administrative operation")
	}
	if err := Decode(request.Payload, input); err != nil {
		return nil, err
	}
	return input, nil
}
