package adminwire

import (
	"bytes"
	"strings"
	"testing"
)

func TestStrictFrameAndTypedPayload(t *testing.T) {
	for _, raw := range []string{`null`, `{"version":1,"id":1,"id":2}`, `{"version":1,"id":1} {}`, `{"version":1,"userUid":0}`, strings.Repeat("[", 34) + strings.Repeat("]", 34)} {
		var r Request
		if err := Decode([]byte(raw), &r); err == nil {
			t.Fatal("accepted", raw)
		}
	}
	for _, r := range []Request{{Kind: "shell", Payload: []byte(`{}`)}, {Kind: "inspect", Payload: []byte(`{"store":"/"}`)}, {Kind: "commit", Payload: []byte(`{"leaseId":"x","plan":{}}`)}, {Kind: "beginClient", Payload: []byte(`{"connection":"{}","uid":0}`)}, {Kind: "beginServer", Payload: []byte(`{"source":"/a","source":"/b"}`)}} {
		if _, err := Input(r); err == nil {
			t.Fatal("accepted", r)
		}
	}
	if _, err := Input(Request{Kind: "inspect", Payload: []byte(`{}`)}); err != nil {
		t.Fatal(err)
	}
}
func TestTransportBoundedBeforeDecodeAndWrite(t *testing.T) {
	r := NewReader(strings.NewReader(strings.Repeat("x", RequestLimit+1)+"\n"), RequestLimit)
	if r.Scan() || r.Err() == nil {
		t.Fatal("oversize frame accepted")
	}
	var out bytes.Buffer
	if err := Write(&out, strings.Repeat("x", ReplyLimit), ReplyLimit); err == nil || out.Len() != 0 {
		t.Fatal("oversize reply wrote bytes")
	}
}
