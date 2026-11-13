# Shared workflows and composites

Consumer repositories under the Hertzline organization call these from `Hertzline/.github`.

## Rules

- Pin every third-party Action and every reusable workflow reference to a **40-character commit SHA**.
- Keep `permissions:` minimal (`contents: read` unless a job needs more).
- Never expose repository or organization secrets to fork pull requests. Gate secret-using jobs with same-repo checks, or keep `has-secrets: false` and do not pass `secrets: inherit` on fork PRs.
- License audit must stay green before merge when the repo has dependency manifests.

## Action pins used here (verified 2026-11-13)

| Action | Tag | Commit SHA |
|---|---|---|
| `actions/checkout` | v7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` |

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
    uses: Hertzline/.github/.github/workflows/reusable-ci.yml@<sha>
    with:
      meta-ref: <sha>
      pin-check: true
      license-audit: true
      has-secrets: false
```

License-only:

```yaml
jobs:
  licenses:
    uses: Hertzline/.github/.github/workflows/reusable-license-audit.yml@<sha>
    with:
      meta-ref: <sha>
```

## Consumer expectations

- **npm:** ship a lockfile; production licenses must not match the fail list (default includes GPL, AGPL, SSPL, BUSL, Commons Clause).
- **Cargo:** ship `deny.toml` (or `.cargo/deny.toml`) with an explicit license allow-list; `cargo deny check licenses` must pass.
- **No manifests:** a root `LICENSE` containing `MIT License` is enough for this meta-style repository.
