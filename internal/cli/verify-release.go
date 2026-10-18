package cli

import (
	"bytes"
	"encoding/json"
	"errors"
	"io"
	"os"
	"reflect"
	"runtime"

	"github.com/AutoByteus/autobyteus-nfs/internal/config"
	"github.com/AutoByteus/autobyteus-nfs/internal/setup"
)

func VerifyRelease(path string, embedded setup.Release) error {
	info, err := os.Lstat(path)
	if err != nil {
		return err
	}
	if !info.Mode().IsRegular() || info.Size() > config.MaxRecordBytes {
		return errors.New("invalid release manifest")
	}
	b, err := os.ReadFile(path)
	if err != nil {
		return err
	}
	if err := uniqueReleaseValue(json.NewDecoder(bytes.NewReader(b)), 0); err != nil {
		return err
	}
	// Distribution metadata is a strict current contract, unlike additive host
	// records. Do not change config.Decode's installed-state policy.
	var manifest setup.Release
	decoder := json.NewDecoder(bytes.NewReader(b))
	decoder.DisallowUnknownFields()
	if err = decoder.Decode(&manifest); err != nil {
		return err
	}
	var trailing any
	if err = decoder.Decode(&trailing); err != io.EOF {
		return errors.New("trailing release data")
	}
	if manifest.Schema != 2 || manifest.FieldValidation != (setup.FieldValidation{Filesystem: "deferred", User: "deferred"}) {
		return errors.New("unsupported release schema or field-validation claim")
	}
	if !reflect.DeepEqual(manifest, embedded) {
		return errors.New("downloaded manifest differs from this binary's pinned release")
	}
	target := runtime.GOOS + "-" + runtime.GOARCH
	seen := map[string]bool{}
	for _, released := range manifest.ReleaseTargets {
		switch released {
		case "darwin-amd64", "darwin-arm64", "linux-amd64", "linux-arm64":
		default:
			return errors.New("unsupported release target")
		}
		if seen[released] {
			return errors.New("duplicate release target")
		}
		seen[released] = true
	}
	if !seen[target] {
		return errors.New("this release does not admit the current computer/CPU; no installation performed")
	}
	return nil
}

// Reject ambiguous duplicate claims before typed decoding. This is local to
// distribution admission; it does not alter the persisted host-state reader.
func uniqueReleaseValue(decoder *json.Decoder, depth int) error {
	if depth > 64 {
		return errors.New("release metadata nesting exceeds bound")
	}
	token, err := decoder.Token()
	if err != nil {
		return err
	}
	delim, compound := token.(json.Delim)
	if !compound {
		return nil
	}
	seen := map[string]bool{}
	for decoder.More() {
		if delim == '{' {
			key, err := decoder.Token()
			if err != nil {
				return err
			}
			name, ok := key.(string)
			if !ok || seen[name] {
				return errors.New("duplicate or invalid release key")
			}
			seen[name] = true
		}
		if err := uniqueReleaseValue(decoder, depth+1); err != nil {
			return err
		}
	}
	_, err = decoder.Token()
	return err
}
