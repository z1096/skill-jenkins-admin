"""Delete a Jenkins job. Destructive — requires --yes to actually run.

Usage:
    python delete_job.py <job-path>          # dry-run: prints what it would do
    python delete_job.py <job-path> --yes    # actually delete
"""
from __future__ import annotations

import sys

from _client import jenkins_client


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    args = sys.argv[1:]
    confirm = "--yes" in args
    args = [a for a in args if a != "--yes"]
    if len(args) != 1:
        sys.exit(__doc__)
    job = args[0]
    j = jenkins_client()
    if not j.job_exists(job):
        print(f"[skip] {job} not found")
        return 0
    if not confirm:
        print(f"[dry-run] would delete {job}; re-run with --yes to confirm")
        return 0
    j.delete_job(job)
    print(f"[deleted] {job}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
