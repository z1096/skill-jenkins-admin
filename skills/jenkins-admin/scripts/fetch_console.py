"""Fetch a Jenkins build's console log to a local file.

Read-only. Does NOT trigger any build or modify any job.

Usage:
    python fetch_console.py <job-path> <build-number> [-o <file>]

By default writes to <tempdir>/<safe-job-name>-<n>.txt and prints the path.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

from _client import jenkins_client


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("job")
    p.add_argument("build", type=int)
    p.add_argument("-o", "--output")
    args = p.parse_args()

    j = jenkins_client()
    out = j.get_build_console_output(args.job, args.build)
    if args.output:
        target = Path(args.output)
    else:
        safe = re.sub(r"[^\w.\-]+", "_", args.job)
        target = Path(tempfile.gettempdir()) / f"{safe}-{args.build}.txt"
    target.write_text(out, encoding="utf-8")
    print(f"wrote {target} ({len(out)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
