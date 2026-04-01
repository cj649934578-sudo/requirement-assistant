# requirement-assistant

[中文](README.md) | [English](README_EN.md)

[![npm version](https://img.shields.io/npm/v/@chaidd/requirement-assistant-skill)](https://www.npmjs.com/package/@chaidd/requirement-assistant-skill)
![schema-driven](https://img.shields.io/badge/schema-driven-0f766e)
![plan-first workflow](https://img.shields.io/badge/workflow-plan--first-2563eb)
![eval-ready](https://img.shields.io/badge/evals-ready-7c3aed)
![windows powershell](https://img.shields.io/badge/platform-Windows%20PowerShell-1d4ed8)

![requirement-assistant cover](docs/requirement-assistant/readme-cover-plan-first-workflow.svg)

Turn messy requirement materials such as screenshots, prototypes, meeting notes, and PRD fragments into structured, validation-ready outputs.

This is not just another prompt bundle that jumps straight to a PRD. It is a **plan-first requirement workflow** designed for more reliable team use:

- clarify the goal and scope first
- produce an execution plan first
- inspect gaps, ambiguity, conflicts, and coverage holes first
- surface items that must be confirmed
- generate PRDs, test points, or strict JSON only after that

It works well both as a Codex/GPT skill and as input to downstream automation because the repo includes:

- a defined requirement workflow
- three strict JSON Schemas
- minimal valid examples
- local bootstrap / validate tools
- eval baselines

> If you are tired of AI confidently inventing details from a few screenshots, this project is built for you.

Installation details: [INSTALL.md](INSTALL.md)

---

## Input -> Output

Here is a realistic example.

### Input materials

Assume all you have is:

- 2 screenshots of a member center page
- a meeting note: `show a reminder 7 days before membership expiration; benefits expire after expiration, but historical orders remain valid`
- a product note: `the page should show current level, expiration time, renewal entry, and benefit description`
- one extra note: `enterprise members do not support renewal entry for now`

If you ask a model to write a PRD directly from that input, common problems usually appear:

- it invents rules that were never confirmed
- it hides the personal vs enterprise member difference inside prose
- it misses key states such as pre-expiration, post-expiration, and renewal failure
- it does not make the unanswered questions explicit

### Output

`requirement-assistant` prefers generating an `issue-report` or execution plan first. The result looks more like this:

```yaml
intent_summary:
  target_artifact: issue-report
  scope: membership module in member center
  current_goal: identify requirement gaps before drafting the PRD

recognized_items:
  - display current membership level
  - display expiration time
  - provide a renewal entry
  - display benefit descriptions
  - 7-day pre-expiration reminder
  - benefits become invalid after expiration
  - historical orders remain unaffected
  - enterprise members do not support renewal entry

findings:
  missing:
    - reminder delivery channel is not defined
    - renewal failure handling is not defined
    - post-expiration page state is not fully defined
  ambiguous:
    - should enterprise members see no renewal entry at all, or a disabled button with an explanation
    - can expired members renew directly from the same page
  coverage_gap:
    - reminder frequency rule is missing
    - benefit display rule after expiration is missing

must_confirm:
  - Should enterprise members see no renewal button, or a disabled button with an explanation?
  - After expiration, should the page prioritize renewal guidance or benefit expiration notice?

recommended_next_step:
  - confirm the 2 blocking questions above
  - then generate prd-bundle and test points
```

### Why this output matters

Instead of rushing into a polished-looking PRD, it does the important work first:

- separates recognized facts from unresolved questions
- exposes the issues that directly affect implementation and testing
- makes the next step explicit before generation starts

For teams, this is usually much more reliable than a long document generated too early.

---

## Why This Project Matters

Most AI requirement workflows share three problems:

- they generate long documents too early
- they blur facts and assumptions
- they are hard to validate or plug into team processes

`requirement-assistant` is designed in the opposite direction.

### 1) Plan first, generate later

Instead of jumping straight into a PRD, it follows:

`intent -> plan -> check -> ask -> confirm -> execute -> verify`

This reduces two common failure modes:

- AI fills in missing business logic on its own
- output drifts because scope was never locked

### 2) It finds problems before it writes documents

Before generation, it explicitly looks for:

- missing information
- conflicts
- ambiguity
- coverage gaps

That makes it a requirement analysis assistant, not just a document writer.

### 3) It is built for teams and automation

The repo includes strict Schemas, examples, validation scripts, and eval baselines, so results can be:

- reviewed by product, engineering, and QA
- passed into GPT / Codex follow-up workflows
- consumed by automation pipelines

### 4) It handles messy real-world inputs

Real requirement inputs are usually incomplete and mixed:

- screenshots and prototypes
- notes and field descriptions
- PRD fragments
- meeting summaries
- mixed Chinese and English materials

This project is built to turn that mess into structured outputs a team can actually move forward with.

---

## Good Fit For

This project is especially useful when:

- product managers want to scan screenshots and notes for gaps or ambiguity
- engineers want clearer rules, states, and edge cases before implementation
- QA wants test points and coverage holes surfaced earlier
- teams want requirement analysis results in structured form instead of scattered chat history
- you want requirement understanding to plug into automation instead of staying manual

---

## What It Produces

### 1) `issue-report`

Best when requirements are still unclear and you want to scan for problems first.

You get:

- missing information
- conflict points
- ambiguity points
- coverage gaps
- pending confirmations

Typical use cases:

- pre-review checks
- PRD quality scanning
- screenshot / prototype gap analysis

### 2) `prd-bundle`

Best when scope is mostly confirmed and you want delivery-oriented artifacts.

You get:

- PRD draft
- feature list
- test points
- draft test cases

Typical use cases:

- turning raw requirement material into execution-ready docs
- creating a shared alignment draft for product, engineering, and QA

### 3) `requirement-package`

Best when you want a full structured package for archiving or downstream systems.

You get:

- recognition summary
- structured model
- issue list
- pending confirmations
- optional generated artifacts

Typical use cases:

- feeding downstream AI / automation workflows
- requirement asset archiving

---

## Repository Layout

```text
SKILL.md                 # skill entry and behavior rules
schemas/                 # strict JSON Schemas
examples/                # minimal valid examples
references/              # templates, checklists, and output references
scripts/                 # bootstrap / validate / eval tools
evals/                   # eval baselines
ra.ps1                   # Windows PowerShell entry point
```

---

## Quick Start

### Requirements

- PowerShell
- Python 3 available as `python`

### Option 1: Use the repo directly

From the repo root:

```powershell
.\ra.ps1 check-examples
.\ra.ps1 run-evals
```

If both commands succeed, the bundled examples and eval baseline are working.

### Option 2: Install via npm / npx

```powershell
npx @chaidd/requirement-assistant-skill@latest install
```

Default install location:

```text
%USERPROFILE%\.codex\skills\requirement-assistant
```

Install into the current project:

```powershell
npx @chaidd/requirement-assistant-skill@latest install --target project
```

Install into a custom directory:

```powershell
npx @chaidd/requirement-assistant-skill@latest install --dir C:\Users\you\.codex\skills
```

More installation details: [INSTALL.md](INSTALL.md)

---

## Common Commands

### Validate bundled examples

```powershell
.\ra.ps1 check-examples
```

Expected result:

- `VALID` x3

### Generate an empty JSON skeleton

```powershell
.\ra.ps1 bootstrap issue-report out.issue-report.json
```

### Validate a JSON output

```powershell
.\ra.ps1 validate issue-report out.issue-report.json
```

### Run eval baselines

```powershell
.\ra.ps1 run-evals
```

Run a single case:

```powershell
.\ra.ps1 run-evals issue-report-gdyd-202603
```

Run the negative baseline:

```powershell
python scripts/run_evals.py --manifest evals/negative.json
```

---

## Schema Guide

Choose a schema based on what you want:

- “I want to find problems, fill gaps, and scan risk first” -> `issue-report`
- “I want PRD drafts, feature lists, test points, and draft cases” -> `prd-bundle`
- “I want recognition, issues, confirmations, and artifacts in one package” -> `requirement-package`

---

## How To Use It As A Skill

This is a **plan-first** requirement workflow skill. In normal use, you do not need to type every stage manually. You can describe the goal in natural language and let the assistant drive the internal phase order.

Recommended prompts:

- `assistant-action, generate the plan first and wait for my confirmation before continuing`
- `analyze this batch of screenshots first and give me the execution plan`
- `check this PRD for ambiguity, conflicts, and missing information`
- `break down this page into features, states, and flows`
- `the scope is confirmed, output the feature list and test points directly`
- `ask me the must-confirm questions before generating the PRD`

Default internal flow:

`intent -> plan -> check -> ask -> confirm -> execute -> verify -> finalize`

Recommended unified entry:

- `assistant-action`

It typically outputs:

- intent summary
- execution plan
- current judgment
- input inventory
- recognized content
- layered pending confirmations
- recommended next step

Full behavior details: [SKILL.md](SKILL.md)

---

## Current Support

### Input materials

- page screenshots / prototype screenshots / interaction screenshots
- page notes / field descriptions / flow descriptions
- PRD fragments / meeting notes / fragmented requirement text
- mixed image and text materials
- mixed Chinese and English input

### Output artifacts

- `issue-report`
- `prd-bundle`
- `requirement-package`

### Validation support

- local validation for the three JSON output types above

---

## Limitations

This repo is intentionally focused on requirement workflow and structured outputs. It is not a full product.

It does not include:

- OpenAI API calls
- Web UI / backend service
- screenshot parsing
- requirement knowledge base or persistent storage

Also:

- `scripts/validate_output.py` implements a **subset JSON Schema validator**
- it covers common capabilities such as `type / enum / required / items / $ref`
- it is not a full Draft 2020-12 implementation

---

## Who This Is For

This project is likely useful if you are:

- a product manager trying to make AI requirement analysis more reliable
- an engineer who wants clearer rules, boundaries, and state flows before implementation
- a QA engineer who wants earlier visibility into test points and edge cases
- a team lead trying to turn requirement analysis into reusable structured assets
- an AI engineer connecting requirement understanding into downstream automation

If that sounds like your workflow, a Star is appreciated.

---

## License

See [LICENSE](LICENSE).
