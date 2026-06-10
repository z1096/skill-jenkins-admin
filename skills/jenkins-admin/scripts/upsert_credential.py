"""Create or update a global secret-text credential.

Stored under the system store, domain "_". Use --description to override.

Usage:
    python upsert_credential.py <cred-id> <secret-value> [--description "..."]
"""
from __future__ import annotations

import argparse
import sys

from _client import JENKINS_URL, requests_session


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("cred_id")
    p.add_argument("secret")
    p.add_argument("--description", default="")
    args = p.parse_args()

    base = f"{JENKINS_URL}/credentials/store/system/domain/_"
    xml = (
        '<org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl plugin="plain-credentials">\n'
        f"  <scope>GLOBAL</scope>\n"
        f"  <id>{args.cred_id}</id>\n"
        f"  <description>{args.description}</description>\n"
        f"  <secret>{args.secret}</secret>\n"
        "</org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl>"
    )
    s = requests_session()
    cfg_url = f"{base}/credential/{args.cred_id}/config.xml"
    r = s.get(cfg_url, timeout=10)
    if r.status_code == 200:
        s.post(cfg_url, data=xml,
               headers={"Content-Type": "application/xml"}, timeout=10)
        print(f"[update] {args.cred_id}")
    else:
        s.post(f"{base}/createCredentials", data=xml,
               headers={"Content-Type": "application/xml"}, timeout=10)
        print(f"[create] {args.cred_id}")

    exists = s.get(cfg_url, timeout=10).status_code == 200
    print(f"verify exists={exists}")
    return 0 if exists else 1


if __name__ == "__main__":
    sys.exit(main())
