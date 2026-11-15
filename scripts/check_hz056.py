#!/usr/bin/env python3
"""HZ-056 local check: meta repo pin/license/fork-secret hardening."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / ".github" / "workflows" / "ci.yml"
WORKFLOWS = ROOT / "WORKFLOWS.md"
SHA40 = re.compile(r"@[0-9a-fA-F]{40}\b")

REQUIRED_FILES = [
    CI,
    WORKFLOWS,
    ROOT / ".github" / "workflows" / "reusable-ci.yml",
    ROOT / ".github" / "workflows" / "reusable-license-audit.yml",
    ROOT / "actions" / "pin-actions" / "action.yml",
    ROOT / "actions" / "fork-guard" / "action.yml",
    ROOT / "actions" / "license-audit" / "action.yml",
    ROOT / "LICENSE",
]


def main() -> int:
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED_FILES if not p.is_file()]
    if missing:
        print("FAIL missing files:", ", ".join(missing))
        return 1

    text = CI.read_text(encoding="utf-8")
    for marker in (
        "permissions:",
        "contents: read",
        'has-secrets: "false"',
        "fork-guard",
        "pin-actions",
        "license-audit",
        "check_hz056.py",
    ):
        if marker not in text:
            print("FAIL ci.yml missing:", marker)
            return 1

    if "secrets: inherit" in text:
        print("FAIL ci.yml must not use secrets: inherit")
        return 1

    for m in re.finditer(r"(?m)^\s*uses:\s*(\S+)", text):
        value = m.group(1).strip().strip("\"'")
        if value.startswith("./") or value.startswith("$/"):
            continue
        if not SHA40.search(value):
            print("FAIL unpinned uses:", value)
            return 1

    docs = WORKFLOWS.read_text(encoding="utf-8")
    for marker in (
        "HZ-056",
        "3d3c42e5aac5ba805825da76410c181273ba90b1",
        "has-secrets: false",
        "no secrets for fork",
        "license-checker",
        "cargo-deny",
    ):
        if marker not in docs:
            print(f"FAIL WORKFLOWS.md missing: {marker}")
            return 1

    print("check_hz056: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
