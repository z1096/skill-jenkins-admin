# skill-jenkins-admin one-line installer (Windows PowerShell).
#
# Usage:
#   irm https://raw.githubusercontent.com/z1096/skill-jenkins-admin/main/install.ps1 | iex
#
# Or, after cloning the repo manually:
#   pwsh ./install.ps1
#
# What it does:
#   1. Checks Python >= 3.7 and pip-installable libs (python-jenkins, requests).
#   2. Downloads the `skills/jenkins-admin` tree from the GitHub repo into
#      $env:USERPROFILE\.claude\skills\jenkins-admin (overwrites the dir).
#   3. Prints next steps.
#
# Idempotent. Does NOT touch your Jenkins server or any env vars.

$ErrorActionPreference = 'Stop'

$repo = 'z1096/skill-jenkins-admin'
$ref  = if ($env:SKILL_JENKINS_ADMIN_REF) { $env:SKILL_JENKINS_ADMIN_REF } else { 'main' }
$dst  = "$env:USERPROFILE\.claude\skills\jenkins-admin"

Write-Host "==> Checking Python >= 3.7" -ForegroundColor Cyan
$pyver = & python -c "import sys; print(sys.version_info[0]*100+sys.version_info[1])" 2>$null
if (-not $pyver -or [int]$pyver -lt 307) {
    Write-Warning "Python 3.7+ not found. Install from https://www.python.org/downloads/ then re-run."
} else { Write-Host "    Python OK ($pyver / 100 = 3.x)" }

Write-Host "==> Checking Python libs" -ForegroundColor Cyan
foreach ($mod in 'jenkins','requests') {
    & python -c "import $mod" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "  pip install $($(if($mod -eq 'jenkins'){'python-jenkins'}else{$mod}))   # missing"
    } else { Write-Host "    $mod OK" }
}

Write-Host "==> Downloading skill from github.com/$repo @ $ref" -ForegroundColor Cyan
$tmpZip = "$env:TEMP\skill-jenkins-admin-$ref.zip"
$tmpDir = "$env:TEMP\skill-jenkins-admin-$ref"
if (Test-Path $tmpZip) { Remove-Item -Force $tmpZip }
if (Test-Path $tmpDir) { Remove-Item -Recurse -Force $tmpDir }
Invoke-WebRequest -Uri "https://codeload.github.com/$repo/zip/refs/heads/$ref" -OutFile $tmpZip -UseBasicParsing
Expand-Archive -Path $tmpZip -DestinationPath $tmpDir -Force

$srcSkill = Get-ChildItem -Directory $tmpDir | Select-Object -First 1
$srcSkill = Join-Path $srcSkill.FullName "skills\jenkins-admin"
if (-not (Test-Path $srcSkill)) { throw "skill folder not found in downloaded archive: $srcSkill" }

Write-Host "==> Installing into $dst" -ForegroundColor Cyan
if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
Copy-Item -Recurse $srcSkill $dst

Remove-Item -Force $tmpZip
Remove-Item -Recurse -Force $tmpDir

Write-Host ""
Write-Host "==> Done." -ForegroundColor Green
Write-Host "    Skill installed at: $dst"
Write-Host ""
Write-Host "Next:"
Write-Host "  1. Restart Claude Code (the skill is loaded at session start)."
Write-Host "  2. Set the three Jenkins env vars before invoking the skill:"
Write-Host "       `$env:JENKINS_URL='https://your.jenkins/'"
Write-Host "       `$env:JENKINS_USER='your-account'"
Write-Host "       `$env:JENKINS_PASS='your-api-token'"
Write-Host "  3. Mention 'jenkins-admin' or ask Claude to do a Jenkins task."
