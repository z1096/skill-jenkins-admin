"""Disable a Jenkins job AND prefix its description with [DEPRECATED].

Idempotent. Mutates the job's config only — does NOT trigger or delete builds.

Usage:
    python deprecate_job.py <job-path> [<job-path> ...]
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET

from _client import jenkins_client


def deprecate(j, full: str) -> None:
    if not j.job_exists(full):
        print(f"[skip] {full} not found")
        return
    root = ET.fromstring(j.get_job_config(full))

    d = root.find("disabled")
    if d is None:
        d = ET.SubElement(root, "disabled")
    d.text = "true"

    desc = root.find("description")
    if desc is None:
        desc = ET.SubElement(root, "description")
        desc.text = ""
    if desc.text is None:
        desc.text = ""
    if "[DEPRECATED]" not in desc.text:
        desc.text = f"[DEPRECATED] {desc.text}".strip()

    new_xml = '<?xml version="1.1" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode")
    j.reconfig_job(full, new_xml)
    print(f"[deprecated+disabled] {full}")


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    j = jenkins_client()
    for full in sys.argv[1:]:
        deprecate(j, full)
    return 0


if __name__ == "__main__":
    sys.exit(main())
