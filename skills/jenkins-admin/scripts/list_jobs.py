"""List Jenkins jobs, optionally filtered by a regex pattern.

Read-only. Does NOT trigger any build or modify any job.

Usage:
    python list_jobs.py                 # all jobs
    python list_jobs.py pattern         # case-insensitive regex on the full job path
"""
from __future__ import annotations

import re
import sys
import urllib.parse

from _client import jenkins_client


def walk(j, base: str = ""):
    if base:
        try:
            info = j.get_job_info(base)
        except Exception:
            return
        items = info.get("jobs", [])
    else:
        items = j.get_info()["jobs"]
    for it in items:
        full = (base + "/" + it["name"]) if base else it["name"]
        cls = it["_class"].split(".")[-1]
        if cls == "Folder":
            yield from walk(j, full)
        else:
            decoded = urllib.parse.unquote(it["url"].rstrip("/").split("/")[-1])
            yield full, cls, decoded


def main() -> int:
    pat = re.compile(sys.argv[1], re.I) if len(sys.argv) > 1 else None
    j = jenkins_client()
    n = 0
    for full, cls, decoded in walk(j):
        if pat and not pat.search(full) and not pat.search(decoded):
            continue
        print(f"[{cls}] {full}" + (f" | {decoded}" if decoded != full.split('/')[-1] else ""))
        n += 1
    print(f"\n{n} job(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
