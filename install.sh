#!/usr/bin/env bash
# skill-jenkins-admin one-line installer (Linux / macOS / Git Bash).
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/z1096/skill-jenkins-admin/main/install.sh | bash
#
# Or, after cloning the repo manually:
#   bash ./install.sh
#
# What it does:
#   1. Checks Python >= 3.7 and pip-installable libs (python-jenkins, requests).
#   2. Downloads the `skills/jenkins-admin` tree from the GitHub repo into
#      ~/.claude/skills/jenkins-admin (overwrites the dir).
#   3. Prints next steps.
#
# Idempotent. Does NOT touch your Jenkins server or any env vars.

set -euo pipefail

REPO="z1096/skill-jenkins-admin"
REF="${SKILL_JENKINS_ADMIN_REF:-main}"
DST="${HOME}/.claude/skills/jenkins-admin"

GREEN="\033[32m"; CYAN="\033[36m"; YELLOW="\033[33m"; RESET="\033[0m"

echo -e "${CYAN}==> Checking Python >= 3.7${RESET}"
if ! command -v python3 >/dev/null 2>&1; then
    echo -e "${YELLOW}    python3 not found. Install Python 3.7+ first.${RESET}"
else
    PYVER=$(python3 -c "import sys; print(sys.version_info[0]*100+sys.version_info[1])")
    if [ "$PYVER" -lt 307 ]; then
        echo -e "${YELLOW}    Python too old ($PYVER). Need 3.7+.${RESET}"
    else
        echo "    Python OK"
    fi
fi

echo -e "${CYAN}==> Checking Python libs${RESET}"
for mod in jenkins requests; do
    if ! python3 -c "import ${mod}" >/dev/null 2>&1; then
        pip_name=$([ "$mod" = "jenkins" ] && echo "python-jenkins" || echo "$mod")
        echo -e "${YELLOW}    pip install ${pip_name}   # missing${RESET}"
    else
        echo "    ${mod} OK"
    fi
done

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

echo -e "${CYAN}==> Downloading skill from github.com/${REPO} @ ${REF}${RESET}"
curl -fsSL "https://codeload.github.com/${REPO}/zip/refs/heads/${REF}" -o "${TMPDIR}/src.zip"
unzip -q "${TMPDIR}/src.zip" -d "${TMPDIR}/"

# Locate the skill folder inside the extracted archive.
SRC_ROOT=$(find "${TMPDIR}" -maxdepth 1 -type d -name "skill-jenkins-admin-*" | head -1)
SRC_SKILL="${SRC_ROOT}/skills/jenkins-admin"
[ -d "${SRC_SKILL}" ] || { echo "skill folder not found at ${SRC_SKILL}"; exit 1; }

echo -e "${CYAN}==> Installing into ${DST}${RESET}"
rm -rf "${DST}"
mkdir -p "$(dirname "${DST}")"
cp -R "${SRC_SKILL}" "${DST}"

echo
echo -e "${GREEN}==> Done.${RESET}"
echo "    Skill installed at: ${DST}"
echo
echo "Next:"
echo "  1. Restart Claude Code (the skill is loaded at session start)."
echo "  2. Set the three Jenkins env vars before invoking the skill:"
echo "       export JENKINS_URL=https://your.jenkins/"
echo "       export JENKINS_USER=your-account"
echo "       export JENKINS_PASS=your-api-token"
echo "  3. Mention 'jenkins-admin' or ask Claude to do a Jenkins task."
