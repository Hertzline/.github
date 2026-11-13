# Security Policy

## Supported versions

Security fixes apply to the latest published release of each Hertzline repository. Pre-release and unreleased code may receive fixes at maintainer discretion.

## Reporting a vulnerability

Do **not** open a public issue for security reports.

Prefer [GitHub private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability) on the affected repository when enabled.

If private reporting is unavailable, open a draft [GitHub Security Advisory](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/creating-a-repository-security-advisory) request by contacting an organization owner through a private channel.

Include:

- Affected repository and version (or commit)
- Description of the issue and impact
- Steps to reproduce
- Whether a fix or workaround is known

## Response

Maintainers aim to acknowledge reports within 7 days and keep reporters informed of status. Disclosure timing is coordinated with the reporter when a fix is prepared.

## Scope notes

Hertzline does not ship kernel drivers authored by the project. Privilege elevation is limited to a small, allow-listed helper. Reports about injection into games, anti-cheat bypass, or remote code execution in the helper are high priority.
