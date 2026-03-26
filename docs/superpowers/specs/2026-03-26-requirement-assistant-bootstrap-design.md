# Requirement Assistant Bootstrap (GSD + Minimal CLI) — Design

Date: 2026-03-26

## Context

This repository is a “skill package” (workflow + templates + JSON Schemas + local validators), not an executable application.
Current contents:
- `SKILL.md` (plan-first workflow)
- `references/` (templates and notes)
- `schemas/` (strict JSON schemas)
- `scripts/` (bootstrap + validate utilities)
- `.planning/codebase/` (local codebase map)

The repo is not currently a git repository (`.git` missing), so workflows that assume commits must be disabled.

## Goals

1. Make GSD health check pass by bootstrapping required planning files:
   - `.planning/PROJECT.md`
   - `.planning/ROADMAP.md`
   - `.planning/STATE.md`
   - `.planning/config.json`
2. Provide a minimal Windows-first CLI entrypoint to run the existing schema utilities consistently:
   - bootstrap outputs
   - validate outputs
   - validate bundled examples

## Non-goals

- Build a hosted service or full application UI.
- Add model-calling logic (OpenAI API, etc.) inside this repo.
- Add packaging (`pip install`, etc.) or non-standard dependencies.

## Proposed Changes

### 1) GSD bootstrap

- Add missing `.planning/*` files from GSD templates, filled with content reflecting the “skill package” reality.
- Set `.planning/config.json` to avoid git assumptions:
  - `planning.commit_docs = false`

### 2) Minimal CLI (Windows)

Add `ra.ps1` at repo root that provides:
- `bootstrap <kind> <output>` → calls `python scripts/bootstrap_output.py`
- `validate <schema> <json>` → calls `python scripts/validate_output.py`
- `check-examples` → validates `examples/*.min.json` for all schemas

CLI is intentionally a thin wrapper over existing scripts; no new Python code is required.

## Verification

- `node "C:/Users/findprocess/.codex/get-shit-done/bin/gsd-tools.cjs" validate health` shows no E002/E003/E004/W003.
- `.\ra.ps1 check-examples` prints `VALID` for all bundled example files.

