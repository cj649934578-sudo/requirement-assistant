# Requirement Assistant Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bootstrap `.planning/` for GSD health and add a minimal Windows-first CLI wrapper for schema bootstrap/validation.

**Architecture:** Write standard GSD planning docs under `.planning/` and add a thin PowerShell wrapper `ra.ps1` that delegates to existing Python scripts.

**Tech Stack:** PowerShell 5+/7, Python 3 stdlib scripts, GSD node tool (already present in environment).

---

### Task 1: Bootstrap GSD planning files

**Files:**
- Create: `.planning/PROJECT.md`
- Create: `.planning/ROADMAP.md`
- Create: `.planning/STATE.md`
- Create: `.planning/config.json`
- Create: `.planning/phases/.keep`

- [ ] Step 1: Create `.planning/PROJECT.md` with required sections
- [ ] Step 2: Create `.planning/ROADMAP.md` with initial phases and success criteria
- [ ] Step 3: Create `.planning/STATE.md` (keep under 100 lines)
- [ ] Step 4: Create `.planning/config.json` based on template, set `planning.commit_docs=false`
- [ ] Step 5: Run GSD health check

Run: `node "C:/Users/findprocess/.codex/get-shit-done/bin/gsd-tools.cjs" validate health`
Expected: no E002/E003/E004; status `healthy` or `degraded` with no missing core files.

### Task 2: Add minimal PowerShell CLI wrapper

**Files:**
- Create: `ra.ps1`

- [ ] Step 1: Implement commands `bootstrap`, `validate`, `check-examples`, `help`
- [ ] Step 2: Run `.\ra.ps1 check-examples`
Expected: `VALID` x3; exit code 0.

