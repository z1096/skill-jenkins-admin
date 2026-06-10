# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `CHANGELOG.md` (this file).
- GitHub Actions CI: Python compile + ruff lint + shellcheck + plugin.json
  validation + a dry-run of `init_pipeline.py`.
- README badges (CI status, license, latest release, PRs welcome).

## [0.1.0] — 2026-06-10

### Added

- Initial public release.
- `SKILL.md` defining the agent-facing protocol:
  - Preflight: probe `JENKINS_URL` / `JENKINS_USER` / `JENKINS_PASS`,
    collect missing values via `AskUserQuestion`, then run a reachability
    check before any other action.
  - Inline-Python pattern for one-off operations and a fallback table to
    `python-jenkins` methods when no script wraps the operation.
  - Guided creation flow for new pipelines via `init_pipeline.py`.
- Ten CLI scripts sharing `_client.py` (auth + CSRF crumb + proxy bypass):
  - `check_env.py` — preflight.
  - `init_pipeline.py` — scaffold a starter Jenkinsfile + job XML.
  - `list_jobs.py` — list jobs, optional regex filter.
  - `show_config.py` — print or save a job's `config.xml`.
  - `upsert_job.py` — create or update a job.
  - `deprecate_job.py` — disable + prefix description `[DEPRECATED]`.
  - `delete_job.py` — destructive job delete (requires `--yes`).
  - `trigger_build.py` — trigger a build, poll to completion.
  - `fetch_console.py` — save a build's console log.
  - `upsert_view.py` — create or update a `ListView`.
  - `upsert_credential.py` — global secret-text credential.
- Starter templates under `scripts/templates/` for the scaffolding flow.
- One-line installers (`install.ps1` for PowerShell, `install.sh` for
  Bash) that pull the skill subtree from GitHub and drop it into
  `~/.claude/skills/jenkins-admin/`.
- `.claude-plugin/plugin.json` so Claude Code's plugin marketplace can
  pick this up as a third-party plugin in the future.
- MIT license.

[Unreleased]: https://github.com/z1096/skill-jenkins-admin/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/z1096/skill-jenkins-admin/releases/tag/v0.1.0
