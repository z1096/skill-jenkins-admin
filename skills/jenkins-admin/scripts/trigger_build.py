"""Trigger a Jenkins build with parameters and (optionally) wait for it.

Does ONLY what's asked — no other jobs modified.

Usage:
    python trigger_build.py <job-path> [k=v ...] [--wait | --no-wait] [--timeout=600]

Examples:
    python trigger_build.py team-test environment=test gitRef=*/main modes=alpha
    python trigger_build.py team-prod gitRef=v1.2.3 --wait --timeout=1800
"""
from __future__ import annotations

import sys
import time

from _client import jenkins_client


def parse_args(argv):
    job = None
    params = {}
    wait = True
    timeout = 600
    for a in argv:
        if a == "--wait":
            wait = True
        elif a == "--no-wait":
            wait = False
        elif a.startswith("--timeout="):
            timeout = int(a.split("=", 1)[1])
        elif "=" in a:
            k, v = a.split("=", 1)
            params[k] = v
        elif job is None:
            job = a
        else:
            sys.exit(f"unexpected arg: {a}")
    if job is None:
        sys.exit(__doc__)
    return job, params, wait, timeout


def main() -> int:
    job, params, wait, timeout = parse_args(sys.argv[1:])
    j = jenkins_client()
    print(f"job: {job}")
    print(f"params: {params}")
    qid = j.build_job(job, parameters=params) if params else j.build_job(job)
    print(f"queued: {qid}")

    # Wait for it to leave the queue and start executing.
    started = None
    for _ in range(60):
        time.sleep(2)
        qi = j.get_queue_item(qid)
        if qi.get("executable"):
            started = qi["executable"]
            print(f"build #{started['number']} at {started['url']}")
            break
        print(f"  still queued: {qi.get('why')}")
    if started is None:
        print("warning: build did not start within 120 s")
        return 0
    if not wait:
        return 0

    bn = started["number"]
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(10)
        info = j.get_build_info(job, bn)
        if not info.get("building"):
            print(f"FINAL: {info.get('result')}  dur={info.get('duration', 0) / 1000:.1f}s")
            return 0 if info.get("result") == "SUCCESS" else 1
        print(f"  building dur={info.get('duration', 0) / 1000:.1f}s")
    print("warning: timed out waiting for build to finish")
    return 2


if __name__ == "__main__":
    sys.exit(main())
