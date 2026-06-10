# skill-jenkins-admin

Claude Code skill for administering a Jenkins server through the
`python-jenkins` library — host-agnostic, classifier-safe, and bundled
with CLI scripts for the most common operations.

> Manage jobs, views, credentials, and builds without leaving the Claude
> Code conversation.

## What's included

- **`SKILL.md`** — the skill body Claude reads on activation. Defines the
  preflight protocol (env probe → collect missing → reachability check),
  the safe inline-Python pattern, and a fallback table for operations
  that don't have a script yet.
- **`scripts/`** — ten standalone CLI tools sharing one `_client.py`
  (auth + CSRF crumb + proxy bypass). All read `JENKINS_URL` /
  `JENKINS_USER` / `JENKINS_PASS` from env; nothing hard-coded.
- **`scripts/templates/`** — declarative Jenkinsfile + job XML starters
  used by `init_pipeline.py` when guiding a user through creating a new
  pipeline from scratch.

## Install

### One-liner (recommended)

**PowerShell (Windows):**

```powershell
irm https://raw.githubusercontent.com/z1096/skill-jenkins-admin/main/install.ps1 | iex
```

**Bash (Linux / macOS / Git Bash):**

```bash
curl -fsSL https://raw.githubusercontent.com/z1096/skill-jenkins-admin/main/install.sh | bash
```

Both installers:

1. Check Python >= 3.7 and warn (without forcing) about missing
   `python-jenkins` / `requests` libs.
2. Download the current `main` tree from GitHub (no full clone, just
   the zip archive — fast and no `.git/` dump in your home).
3. Copy `skills/jenkins-admin/` into `~/.claude/skills/jenkins-admin/`,
   overwriting any existing install. Idempotent.
4. Print the next steps (env vars to set, how to invoke).

**Pin a release:** set `SKILL_JENKINS_ADMIN_REF=v0.1.0` (or any tag /
branch / commit) before running the installer to fetch that ref instead
of `main`.

### Manual install (git clone)

```bash
git clone https://github.com/z1096/skill-jenkins-admin /tmp/sja
cp -r /tmp/sja/skills/jenkins-admin ~/.claude/skills/
```

PowerShell equivalent:

```powershell
git clone https://github.com/z1096/skill-jenkins-admin "$env:TEMP\sja"
Copy-Item -Recurse "$env:TEMP\sja\skills\jenkins-admin" "$env:USERPROFILE\.claude\skills\jenkins-admin"
```

### Plugin install (future)

The repo ships a `plugin.json` under `.claude-plugin/`. When Claude
Code's plugin marketplace opens to third-party sources, the install will
become:

```text
/plugin install https://github.com/z1096/skill-jenkins-admin
```

Until then the installer scripts above are the supported path.

### Verifying the install

Restart Claude Code. The skill is loaded at session start and shows up
in the available-skills list. You can also confirm by ls'ing the dir:

```bash
ls ~/.claude/skills/jenkins-admin
# Expect: SKILL.md and scripts/
```

## Set up your Jenkins credentials

The skill reads three env vars on activation. Set them once per shell
(or persist them in your profile):

```powershell
$env:JENKINS_URL='https://jenkins.example.com'
$env:JENKINS_USER='your-account'
$env:JENKINS_PASS='your-api-token'   # not your password — generate one in Jenkins
```

The skill runs `scripts/check_env.py --offline` on first invocation, asks
you for any values that aren't set (via `AskUserQuestion`), then runs the
full reachability check.

## Scripts at a glance

| Script | Mutates? | What it does |
|---|---|---|
| `check_env.py` | no | preflight: Python, libs, env vars, reachability |
| `init_pipeline.py` | no | scaffold a starter Jenkinsfile + job XML for a new pipeline |
| `list_jobs.py` | no | list jobs, optional regex filter |
| `show_config.py` | no | print or save a job's `config.xml` |
| `upsert_job.py` | yes | create or update a job from an XML file |
| `deprecate_job.py` | yes | disable + prefix description `[DEPRECATED]` |
| `delete_job.py` | DESTRUCTIVE | delete a job (requires `--yes`) |
| `trigger_build.py` | triggers a build | trigger and poll to completion |
| `fetch_console.py` | no | save build console log to a local file |
| `upsert_view.py` | yes | create or update a ListView |
| `upsert_credential.py` | yes | global secret-text credential |

See `skills/jenkins-admin/scripts/README.md` for a fuller cheat-sheet
and `skills/jenkins-admin/SKILL.md` for the agent-facing protocol.

## Design notes

- **Classifier-safe by default.** Every script's first lines are a docstring
  that declares what it does and what it does NOT do, so Claude Code's
  auto-mode classifier reads the intent before allowing execution.
- **Host-agnostic.** No host, account, or project name is committed to the
  repo. The three env vars are the only configuration surface.
- **Inline-Python pattern documented.** When the user needs an operation
  not yet wrapped as a script, the skill instructs the agent to fall
  back to `python-jenkins` directly (with a method cheat-sheet) and to
  promote that snippet to a script once the same operation is needed
  more than twice.
- **No notifications baked in.** Build notifications belong in the
  pipelines themselves, not in the management skill. The
  `init_pipeline.py` template leaves `post {}` blocks open for the team
  to wire up whatever notifier they use.

## Contributing

PRs welcome. Two non-negotiable conventions for new scripts:

1. Read `JENKINS_URL`, `JENKINS_USER`, `JENKINS_PASS` from env via
   `_client.py`. Never hard-code a host.
2. Start with a docstring header that names what the script does and what
   it does NOT do (especially "does NOT trigger any build" for non-build
   operations).

## License

MIT. See [LICENSE](LICENSE).
