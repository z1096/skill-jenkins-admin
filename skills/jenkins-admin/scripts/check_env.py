"""Preflight: verify the environment supports the jenkins-admin scripts.

Read-only. Does NOT trigger any build or modify any Jenkins resource.

Run this FIRST after loading the skill, before any other script. It reports
each check as pass/fail and exits non-zero on the first hard failure, so
the agent can stop and fix the environment before doing anything risky.

Checks performed (in order):
    1. Python >= 3.7        (sys.stdout.reconfigure, f-strings, dataclasses)
    2. python-jenkins       (the main client library)
    3. requests             (used by upsert_credential.py and shared client)
    4. Env vars JENKINS_URL / JENKINS_USER / JENKINS_PASS are set
    5. Optional: reachability — GET /api/json with auth, report whoami
       (skipped with --offline if user wants pure local check)

Usage:
    python check_env.py              # full check including reachability
    python check_env.py --offline    # skip network check
"""
from __future__ import annotations

import importlib
import os
import sys


GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def ok(msg: str) -> None:
    print(f"{GREEN}[ ok ]{RESET} {msg}")


def fail(msg: str) -> int:
    print(f"{RED}[fail]{RESET} {msg}")
    return 1


def warn(msg: str) -> None:
    print(f"{YELLOW}[warn]{RESET} {msg}")


def check_python() -> int:
    if sys.version_info < (3, 7):
        return fail(
            f"python {sys.version_info.major}.{sys.version_info.minor}; need >= 3.7"
        )
    ok(f"python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return 0


def check_module(name: str, hint: str) -> int:
    try:
        m = importlib.import_module(name)
    except Exception as e:
        return fail(f"import {name}: {e!r}\n       install: {hint}")
    ver = getattr(m, "__version__", "(no __version__)")
    ok(f"{name} {ver}")
    return 0


def check_env_vars() -> int:
    rc = 0
    for name in ("JENKINS_URL", "JENKINS_USER", "JENKINS_PASS"):
        val = os.environ.get(name)
        if not val:
            rc |= fail(f"env var {name} is not set")
            continue
        if name == "JENKINS_URL":
            ok(f"env {name}={val}")
        elif name == "JENKINS_USER":
            ok(f"env {name}={val}")
        else:
            ok(f"env {name}=<set, {len(val)} chars>")
    return rc


def check_reachability() -> int:
    """Make one minimal auth'd call and report the user we authenticated as."""
    try:
        import jenkins  # noqa: F401
    except Exception:
        return fail("cannot check reachability: python-jenkins not importable")
    try:
        import urllib.parse
        # Inline minimal client (do NOT import _client.py — that would also
        # validate env vars and we already did that above).
        host = os.environ["JENKINS_URL"].rstrip("/")
        # Bypass proxy for this single call.
        os.environ.setdefault("NO_PROXY", "")
        os.environ["NO_PROXY"] += "," + (urllib.parse.urlsplit(host).hostname or "")
        for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
            os.environ.pop(k, None)
        import jenkins as _j
        client = _j.Jenkins(host,
                            username=os.environ["JENKINS_USER"],
                            password=os.environ["JENKINS_PASS"])
        whoami = client.get_whoami()
        full = whoami.get("fullName") or whoami.get("id") or "(unknown)"
        ok(f"reachable: authenticated as {full}")
        return 0
    except Exception as e:
        return fail(f"reachability check failed: {e}")


def main(argv: list[str]) -> int:
    offline = "--offline" in argv
    rc = 0
    rc |= check_python()
    rc |= check_module("jenkins", "pip install python-jenkins")
    rc |= check_module("requests", "pip install requests")
    rc |= check_env_vars()

    if offline:
        warn("skipping reachability check (--offline)")
    else:
        if rc == 0:
            rc |= check_reachability()
        else:
            warn("skipping reachability check because earlier checks failed")

    print()
    if rc == 0:
        print(f"{GREEN}all checks passed — scripts are ready to use{RESET}")
    else:
        print(f"{RED}preflight failed — fix the failures above before running other scripts{RESET}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
