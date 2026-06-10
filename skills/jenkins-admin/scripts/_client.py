"""Shared helpers for the jenkins-admin scripts.

Centralises auth, CSRF crumb, proxy bypass, and the python-jenkins client.
Read three env vars:

    JENKINS_URL   e.g. https://jenkins.example.com
    JENKINS_USER  username or account name
    JENKINS_PASS  password or API token

Use:

    from _client import jenkins_client, requests_session
    j = jenkins_client()
    s = requests_session()  # raw HTTP, crumb already attached
"""
from __future__ import annotations

import os
import sys
from urllib.parse import urlsplit

import jenkins  # python-jenkins
import requests


def _require(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        sys.exit(f"missing env var: {name}")
    return val


def _bypass_proxy(host: str) -> None:
    """Make sure HTTP(S)_PROXY isn't fighting with this host's large POSTs."""
    bypass = f"{host},localhost"
    os.environ["NO_PROXY"] = os.environ.get("NO_PROXY", "") + "," + bypass
    os.environ["no_proxy"] = os.environ.get("no_proxy", "") + "," + bypass
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
        os.environ.pop(k, None)


def _ensure_utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # py 3.7+
    except Exception:
        pass


_ensure_utf8_stdout()
JENKINS_URL = _require("JENKINS_URL").rstrip("/")
JENKINS_USER = _require("JENKINS_USER")
JENKINS_PASS = _require("JENKINS_PASS")
_bypass_proxy(urlsplit(JENKINS_URL).hostname or "")


def jenkins_client() -> jenkins.Jenkins:
    return jenkins.Jenkins(JENKINS_URL, username=JENKINS_USER, password=JENKINS_PASS)


def requests_session() -> requests.Session:
    """Raw HTTP session with auth + CSRF crumb attached."""
    s = requests.Session()
    s.auth = (JENKINS_USER, JENKINS_PASS)
    s.trust_env = False
    try:
        cr = s.get(f"{JENKINS_URL}/crumbIssuer/api/json", timeout=10).json()
        s.headers[cr["crumbRequestField"]] = cr["crumb"]
    except Exception:
        # No crumb issuer enabled — that's fine for some setups.
        pass
    return s
