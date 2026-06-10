"""Print a Jenkins job's config.xml to stdout (or save to file).

Read-only. Does NOT trigger any build or modify any job.

Usage:
    python show_config.py <job-path>            # to stdout
    python show_config.py <job-path> -o <file>  # save to file
"""
from __future__ import annotations

import argparse
import sys

from _client import jenkins_client


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("job")
    p.add_argument("-o", "--output", help="write XML to this file instead of stdout")
    args = p.parse_args()

    j = jenkins_client()
    if not j.job_exists(args.job):
        sys.exit(f"job not found: {args.job}")
    xml = j.get_job_config(args.job)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(xml)
        print(f"wrote {args.output} ({len(xml)} bytes)")
    else:
        sys.stdout.write(xml)
    return 0


if __name__ == "__main__":
    sys.exit(main())
