"""Create or update a Jenkins ListView from a local XML file.

Usage:
    python upsert_view.py <view-name> <xml-file>
"""
from __future__ import annotations

import sys
from pathlib import Path

from _client import jenkins_client


def main() -> int:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    name, xml_path = sys.argv[1], Path(sys.argv[2])
    if not xml_path.is_file():
        sys.exit(f"file not found: {xml_path}")
    xml = xml_path.read_text(encoding="utf-8")
    j = jenkins_client()
    if j.view_exists(name):
        print(f"[update] {name}")
        j.reconfig_view(name, xml)
    else:
        print(f"[create] {name}")
        j.create_view(name, xml)
    print(f"verify exists={j.view_exists(name)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
