package docker

type Object = map[string]any

// Config and HostConfig remain opaque Docker-owned shapes, preserving fields we do not change.
type Snapshot struct {
	ID         string `json:"Id"`
	Name       string `json:"Name"`
	Image      string `json:"Image"`
	Config     Object `json:"Config"`
	HostConfig Object `json:"HostConfig"`
	Mounts     []struct {
		Type, Name, Source, Destination string
		RW                              bool
	} `json:"Mounts"`
	State struct{ Running bool } `json:"State"`
}

func stringValue(m Object, k string) string { s, _ := m[k].(string); return s }
func boolValue(m Object, k string) bool     { v, _ := m[k].(bool); return v }
func labels(s Snapshot) Object              { m, _ := s.Config["Labels"].(map[string]any); return m }
