"""Create or update a Jenkins job from a local XML file.

Idempotent. Does NOT trigger any build. Mutates the job's config only.

Usage:
    python upsert_job.py <job-path> <xml-file>

Examples:
    python upsert_job.py team-deploy ./jobs/team-deploy.xml
    python upsert_job.py "正式/release-prod" ./jobs/release-prod.xml
"""
from __future__ import annotations

import sys
from pathlib import Path

from _client import jenkins_client


def main() -> int:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    job, xml_path = sys.argv[1], Path(sys.argv[2])
    if not xml_path.is_file():
        sys.exit(f"file not found: {xml_path}")
    xml = xml_path.read_text(encoding="utf-8")
    j = jenkins_client()
    if j.job_exists(job):
        print(f"[update] {job}")
        j.reconfig_job(job, xml)
    else:
        print(f"[create] {job}")
        j.create_job(job, xml)
    print(f"verify exists={j.job_exists(job)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
