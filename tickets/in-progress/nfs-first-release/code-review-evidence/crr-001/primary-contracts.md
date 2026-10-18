# Primary contract corroboration — CRR-001

Read-only web checks supplement local source/design review, not actual hosted or publication execution.

- GitHub's artifact record exposes ID, expiry, workflow-run identity and SHA256 digest, supporting the cross-run envelope verification used by candidate.py. [Actions artifacts API](https://docs.github.com/en/rest/actions/artifacts?apiVersion=2022-11-28#get-an-artifact).
- The organization-package endpoint documents GitHub App installation-token support. Its endpoint-specific authentication contract, rather than a general PAT-only introduction, is the relevant basis for workflow-token source review. Actual repository/package permissions and visibility still need hosted verification. [Get an organization package](https://docs.github.com/en/rest/packages/packages?apiVersion=2022-11-28#get-a-package-for-an-organization).
- skopeo documents copying all manifest-list children with --all and refusing digest changes with --preserve-digests; explicit --src-authfile overrides the general auth file. This supports the retained OCI graph and empty-source-auth anonymous read control; it does not prove current GHCR behavior. [skopeo-copy primary documentation](https://raw.githubusercontent.com/podman-container-tools/skopeo/main/docs/skopeo-copy.1.md).

No token-creation, registry-visibility mutation or credential workaround prescribed. No new material scenario/premise introduced.
