# Contributing to Hertzline

Thank you for considering a contribution. Hertzline is MIT-licensed and organized as separate repositories under the [Hertzline](https://github.com/Hertzline) organization.

## Before you start

1. Read the product principles: measure first; every change must be explained and reversible; never invent measurements.
2. Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
3. Check existing issues and pull requests in the target repository.

## Repositories

| Repository | Contribute when you are changing |
|---|---|
| `core` | Measurement, benchmarks, actions, snapshots, profiles, export |
| `helper` | Privileged per-OS helpers |
| `app` | Desktop UI |
| `packaging` | Installers and manifests |
| `website` | Product site and docs |
| `.github` | Org templates and shared workflows |

Do not introduce a dependency from `core` to `app`, or from `helper` to UI code.

## Development expectations

- English for code, comments, docs, and commit messages.
- No emoji in commits or required project docs.
- Unit tests for every action path: apply, restore, and verify. Label mocks clearly.
- Prefer documented OS APIs. Do not add injection, memory reading, or game file modification.
- Do not claim "+X FPS" without a local measured result.
- Pin GitHub Actions to commit SHAs. Keep workflow permissions minimal.
- Prefer shared workflows documented in [WORKFLOWS.md](WORKFLOWS.md). Do not pass repository secrets to fork pull requests.
- Never commit secrets, `CLAUDE.md`, or `AGENTS.md`.

## Pull requests

1. Fork or branch from `main`.
2. Keep the change focused on one concern.
3. Fill in the pull request template.
4. Ensure CI on the repository is green.
5. Link related issues.

## License

By contributing, you agree that your contributions are licensed under the MIT License of the repository you contribute to.
