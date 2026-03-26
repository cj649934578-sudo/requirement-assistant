[CmdletBinding(PositionalBinding = $true)]
param(
  [Parameter(Position = 0)]
  [string] $Command,

  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]] $ExtraArgs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Usage {
  @"
Requirement Assistant (minimal CLI)

Usage:
  .\ra.ps1 help
  .\ra.ps1 bootstrap <requirement-package|issue-report|prd-bundle> <output.json>
  .\ra.ps1 validate <requirement-package|issue-report|prd-bundle> <json_file>
  .\ra.ps1 check-examples
  .\ra.ps1 run-evals [case-name]

Notes:
  - Requires: Python 3 available as 'python'
  - Runs scripts from this repo: scripts/bootstrap_output.py, scripts/validate_output.py, scripts/run_evals.py
"@ | Write-Host
}

function Require-RepoRoot([string] $RepoRoot) {
  if (-not (Test-Path (Join-Path $RepoRoot 'scripts\validate_output.py'))) {
    throw "Repo root not detected at '$RepoRoot' (missing scripts\validate_output.py)."
  }
}

function Require-Python {
  $py = Get-Command python -ErrorAction SilentlyContinue
  if (-not $py) {
    throw "Python not found on PATH. Install Python 3 and ensure 'python' is available."
  }
}

$repoRoot = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
Require-RepoRoot -RepoRoot $repoRoot
Require-Python

Push-Location $repoRoot
try {
  $extraArgs = @(@($ExtraArgs) | Where-Object { $_ -ne '' })
  switch ($Command) {
    { $_ -in @($null, '', 'help', '-h', '--help') } {
      Write-Usage
      exit 0
    }

    'bootstrap' {
      if ($extraArgs.Count -ne 2) { Write-Usage; exit 2 }
      $kind = $extraArgs[0]
      $output = $extraArgs[1]
      & python scripts\bootstrap_output.py $kind $output
      exit $LASTEXITCODE
    }

    'validate' {
      if ($extraArgs.Count -ne 2) { Write-Usage; exit 2 }
      $schema = $extraArgs[0]
      $jsonFile = $extraArgs[1]
      & python scripts\validate_output.py $schema $jsonFile
      exit $LASTEXITCODE
    }

    'check-examples' {
      & python scripts\validate_output.py requirement-package examples\requirement-package.min.json
      if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

      & python scripts\validate_output.py issue-report examples\issue-report.min.json
      if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

      & python scripts\validate_output.py prd-bundle examples\prd-bundle.min.json
      exit $LASTEXITCODE
    }

    'run-evals' {
      if ($extraArgs.Count -gt 1) { Write-Usage; exit 2 }
      if ($extraArgs.Count -eq 1) {
        & python scripts\run_evals.py --case $extraArgs[0]
      } else {
        & python scripts\run_evals.py
      }
      exit $LASTEXITCODE
    }

    default {
      Write-Host "Unknown command: $Command"
      Write-Usage
      exit 2
    }
  }
} finally {
  Pop-Location
}
