# Shared workflows and composites

Consumer repositories under the Hertzline organization call these from `Hertzline/.github`.

## Rules

- Pin every third-party Action and every reusable workflow reference to a **40-character commit SHA**.
- Keep `permissions:` minimal (`contents: read` unless a job needs more).
- Never expose repository or organization secrets to fork pull requests (no secrets for fork PRs). Gate secret-using jobs with same-repo checks, or keep `has-secrets: false` and do not pass `secrets: inherit` on fork PRs (HZ-056).
- License audit must stay green before merge when the repo has dependency manifests.

## Action pins used here (re-verified 2026-11-15, HZ-056)

| Action | Tag | Commit SHA |
|---|---|---|
| `actions/checkout` | v7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| `actions/setup-node` | v6.0.0 | `2028fbc5c25fe9cf00d9f06a71cc4710d4507903` |
| `actions/setup-python` | v5.6.0 | `a26af69be951a213d495a4c3e4e4022e16d87065` |
| `actions/setup-dotnet` | v5.0.0 | `d4c94342e560b34958eacfc5d055d21461ed1c5d` |
| `browser-actions/setup-chrome` | v2.2.0 | `48ad923757ca74d66703209fe939badbdf80f2f4` |
| `dtolnay/rust-toolchain` | v1 | `683b588c487a69d01f6c6ddf40f036ff682cc2c8` |

License tools used by the composite (not Actions):

| Tool | Version | License | Source |
|---|---|---|---|
| `license-checker` | 25.0.1 | BSD-3-Clause | npm / https://github.com/davglass/license-checker |
| `cargo-deny` | 0.20.2 | Apache-2.0 (and LICENSE-MIT in repo) | https://github.com/EmbarkStudios/cargo-deny/releases/tag/0.20.2 |

Re-verify versions before bumping.

## Composites

Referenced after checkout of this repository, or via absolute path pinned to a SHA:

| Path | Purpose |
|---|---|
| `actions/pin-actions` | Fail on unpinned `uses:` lines in workflow YAML |
| `actions/fork-guard` | Fail if a fork PR path declares extra secrets |
| `actions/license-audit` | npm `license-checker` and/or `cargo deny check licenses`; MIT-only repos with no manifests pass |

Absolute form for consumers (prefer SHA over `main`):

```yaml
uses: Hertzline/.github/actions/license-audit@<sha>
```

## Reusable workflows

| Workflow | Purpose |
|---|---|
| `.github/workflows/reusable-ci.yml` | Fork guard + optional pin check + optional license audit |
| `.github/workflows/reusable-license-audit.yml` | License audit only |

Meta repository commit used by consumers for HZ-056:

`f4f947f31a5da82d0ca4828917490d2a1d1217b0`

Example caller (pin both the workflow ref and `meta-ref` to the same commit):

```yaml
name: ci

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  shared:
    uses: Hertzline/.github/.github/workflows/reusable-ci.yml@f4f947f31a5da82d0ca4828917490d2a1d1217b0
    with:
      meta-ref: f4f947f31a5da82d0ca4828917490d2a1d1217b0
      pin-check: true
      license-audit: true
      has-secrets: false
```

License-only:

```yaml
jobs:
  licenses:
    uses: Hertzline/.github/.github/workflows/reusable-license-audit.yml@f4f947f31a5da82d0ca4828917490d2a1d1217b0
    with:
      meta-ref: f4f947f31a5da82d0ca4828917490d2a1d1217b0
```

## Consumer expectations (HZ-056)

- Every consumer CI must call `reusable-ci` with `pin-check: true` and `has-secrets: false` unless a documented same-repo secret path exists.
- No `secrets: inherit` on jobs that run for fork pull requests.
- **npm:** ship a lockfile; production licenses must not match the fail list (default includes GPL, AGPL, SSPL, BUSL, Commons Clause).
- **Cargo:** ship `deny.toml` (or `.cargo/deny.toml`) with an explicit license allow-list; `cargo deny check licenses` must pass.
- **Path-dependent Cargo workspaces** (`helper`, `app`): set `license-audit: false` on `reusable-ci`, then run `cargo deny` (and npm `license-checker` when `package.json` exists) after sibling `Hertzline/core` checkout.
- **No manifests:** a root `LICENSE` containing `MIT License` is enough for this meta-style repository and for `packaging`.
