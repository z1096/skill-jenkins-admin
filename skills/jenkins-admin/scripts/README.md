# jenkins-admin scripts

Companion CLI scripts for the `jenkins-admin` skill. All scripts read three
env vars before doing anything:

```
JENKINS_URL    e.g. https://jenkins.example.com
JENKINS_USER   username or account name
JENKINS_PASS   password or API token
```

`_client.py` centralises auth, CSRF crumb, and proxy bypass. Other scripts
import it. No host, no user, no secret is committed to the repo.

| Script | Mutates? | What it does |
|---|---|---|
| `check_env.py [--offline]` | no | **preflight** — Python, libs, env vars, reachability |
| `init_pipeline.py <name> [--source scm\|inline] ...` | no | scaffold a starter Jenkinsfile + job XML (writes locally, doesn't touch Jenkins) |
| `list_jobs.py [pattern]` | no | list jobs (regex filter optional) |
| `show_config.py <job> [-o file]` | no | print or save a job's config.xml |
| `upsert_job.py <job> <xml-file>` | yes | create or update job from XML |
| `deprecate_job.py <job> ...` | yes | disable + prefix description with [DEPRECATED] |
| `delete_job.py <job> [--yes]` | DESTRUCTIVE | delete a job (--yes required) |
| `trigger_build.py <job> [k=v ...] [--no-wait]` | triggers build | trigger and poll |
| `fetch_console.py <job> <#> [-o file]` | no | save console log to a file |
| `upsert_view.py <name> <xml-file>` | yes | create or update a ListView |
| `upsert_credential.py <id> <secret> [--description ...]` | yes | global secret-text |

## Examples

```powershell
# Setup once per shell
$env:JENKINS_URL='https://jenkins.example.com'
$env:JENKINS_USER='your-user'
$env:JENKINS_PASS='your-token'

# Always run preflight first — checks Python, libs, env vars, reachability
python .claude/skills/jenkins-admin/scripts/check_env.py

# Survey
python .claude/skills/jenkins-admin/scripts/list_jobs.py
python .claude/skills/jenkins-admin/scripts/list_jobs.py '^team-'

# Read
python .claude/skills/jenkins-admin/scripts/show_config.py team-test-job -o /tmp/cfg.xml

# Mutate
python .claude/skills/jenkins-admin/scripts/upsert_job.py team-test-job /tmp/cfg.xml
python .claude/skills/jenkins-admin/scripts/deprecate_job.py legacy-job-a legacy-job-b
python .claude/skills/jenkins-admin/scripts/upsert_view.py team-view /tmp/view.xml
python .claude/skills/jenkins-admin/scripts/upsert_credential.py my-token-id "$env:MY_TOKEN" --description 'My API token'

# Build
python .claude/skills/jenkins-admin/scripts/trigger_build.py team-test-job environment=test gitRef='*/main'
python .claude/skills/jenkins-admin/scripts/fetch_console.py team-test-job 42

# Destructive (deletion requires explicit --yes)
python .claude/skills/jenkins-admin/scripts/delete_job.py legacy-job-a               # dry-run
python .claude/skills/jenkins-admin/scripts/delete_job.py legacy-job-a --yes         # actually delete
```

## Classifier-safe usage notes

The scripts here are stable, human-readable Python files. Reading them is
safe for the auto-mode classifier. When using them via `python script.py
args...`, the action is unambiguous because the script's first line is a
docstring that states what it does.

Prefer these scripts over ad-hoc inline Python for repeated operations.
Use inline Python (per SKILL.md) only for one-off explorations or when
combining several operations into a single transaction.
