---
name: requirement-assistant
version: 0.2.0
description: "analyze product requirement materials and turn them into structured requirement artifacts for gpt or codex. use when the user provides prototype images, page screenshots, page notes, flow descriptions, prd fragments, meeting notes, or mixed requirement materials and wants a staged requirement workflow: first understand intent, then produce an execution plan, ask blocking questions, confirm scope and assumptions, and only then execute generation of prd drafts, function lists, test points, issue reports, or structured json outputs. also use for requirement checking, analysis, clarification, confirmation, and plan-first execution."
---

# Requirement Assistant

## Operator Manual

### Quick Start

Use this skill when the user provides requirement materials and wants structured outputs instead of ad-hoc prose.

Default operating mode:
- default output is `issue-report` for fast requirement scanning
- export to `prd-bundle` when the user wants deliverables such as PRD drafts, function lists, test points, or draft test cases
- export to `requirement-package` when the user wants a full machine-readable package with recognition, issues, confirmations, and generated artifacts

Default inputs remain flexible:
- screenshots or prototype images
- prototype links plus notes
- flow descriptions, PRD fragments, meeting notes
- mixed image and text material

Working rule:
1. understand the goal
2. produce a fixed plan
3. ask only blocking questions
4. wait for confirmation or explicit assumptions approval
5. execute in bounded steps
6. verify before completion

### Role Views

#### For Testers

Prioritize:
- `issue-report`
- abnormal paths
- boundary conditions
- permission coverage
- state transitions
- unresolved items in `pending_confirmations`

#### For Developers

Prioritize:
- business rules
- page and flow decomposition
- dependency assumptions
- state and sync logic
- what is still ambiguous before implementation

#### For Product Managers

Prioritize:
- scope boundaries
- user-visible flows
- conflicts and ambiguities
- pending confirmations
- what can be executed now versus what still needs clarification

### Modes At A Glance

- `assistant-plan`: understand intent, produce an execution plan, stop before generation
- `assistant-check`: scan for missing, conflict, ambiguous, and coverage-gap issues
- `assistant-analyze`: decompose page, flow, rule, or state impact
- `assistant-ask`: turn unclear requirements into explicit questions
- `assistant-confirm`: lock assumptions, rules, or scope for execution
- `assistant-execute`: generate approved deliverables
- `assistant-generate`: execute only if blockers are already closed, otherwise route back to plan

### Gates

Stop at planning if any of the following are true:
- input is mainly screenshots or prototype images
- business context is missing
- scope is ambiguous
- output format is not specified
- the request could mean several deliverables

Execute only when at least one is true:
- the user answered the blocking questions
- the user approved the execution plan
- the user explicitly allowed proceeding with listed assumptions

Fast draft is an exception, not the default:
- only when the user explicitly asks for a rough draft now
- only when the user accepts missing-context risk
- always label draft outputs with assumptions

### Outputs

Choose output by use case:
- `issue-report`: review, scan, ambiguity check, testability gaps
- `prd-bundle`: PRD draft, function list, test points, draft test cases
- `requirement-package`: full-pass structured package for downstream systems

Use these repo resources:
- `references/plan-templates.md` for intent summary, execution plan, and run status
- `references/output-templates.md` for markdown output structure
- `references/issue-checklist.md` for review prompts
- `references/output-schema.md` for schema selection and validation flow
- `schemas/*.schema.json` for exact JSON contracts
- `scripts/bootstrap_output.py` and `scripts/validate_output.py` for runtime JSON workflow

### Command Shortcuts

Explicit commands:
- `/assistant-plan`
- `/assistant-check`
- `/assistant-analyze`
- `/assistant-ask`
- `/assistant-confirm`
- `/assistant-execute`
- `/assistant-generate`

Natural language should map to the same modes even without slash commands.

### Maintenance Rules

Keep this file lean:
- keep behavioral rules here
- keep long templates in `references/`
- keep exact contracts in `schemas/`
- keep examples in `examples/`

When behavior changes:
- update `version`
- prefer editing templates or schema before adding more prose here
- validate changes against the bundled examples and at least one real sample

## Full Spec

Use this skill as a **plan-first requirement workflow**, not as a direct long-document generator.

Adopt a superpowers-style execution pattern:
1. understand the user's real goal
2. produce a fixed execution plan
3. ask only blocking questions
4. wait for confirmation or explicit permission to proceed with assumptions
5. execute in bounded steps
6. verify outputs before declaring completion

Do not jump straight from screenshots to a full PRD unless the user explicitly asks for fast draft mode and accepts the risk.

## Core workflow

Follow this state machine unless the user explicitly narrows the task to a single phase.

### Phase 1: intent
Determine what the user actually wants.

Clarify:
- target artifact: prd, issue report, function list, test points, draft test cases, or structured json
- scope: page optimization, business logic change, flow redesign, review only, or test preparation
- material completeness: screenshots only, screenshots plus notes, prd fragments, or full mixed materials
- delivery quality level: rough draft, review draft, formal prd, or strict json

Produce `intent-summary.md` style output using the template in `references/plan-templates.md`.

### Phase 2: plan
Before executing, produce a fixed `execution-plan.md` style output.

Always include:
- user goal
- current judgment
- input inventory
- recognized content
- planned steps
- blocking questions
- recommendations
- next action

If the task is image-first, vague, or underspecified, stop here and ask for confirmation before generating long outputs.

### Phase 3: ask
Ask only the questions that materially change scope, structure, or correctness.

Good blocking questions include:
- is this page-only optimization or does it include business logic changes?
- should the output follow a formal company prd template or a compact analysis draft?
- should test points and acceptance criteria be included now?
- which assumptions are safe to proceed with if no answer is available?

Do not ask more than 3 to 5 blocking questions in one turn.
Always pair questions with practical recommendations.

### Phase 4: confirm
The task becomes executable only when one of the following is true:
- the user answered the blocking questions
- the user explicitly approved the execution plan
- the user explicitly allowed proceeding with listed assumptions

When confirming, restate:
- confirmed scope
- confirmed output set
- accepted assumptions
- remaining non-blocking uncertainties

### Phase 5: execute
Only execute after the confirmation gate is passed.

Execution should be bounded and minimal:
- generate only the requested artifacts
- prefer summary-first outputs before full prose
- preserve unresolved points as pending confirmations
- do not silently resolve conflicts

### Phase 6: verify
Before declaring completion, verify:
- requested outputs were produced
- blocking questions count is zero
- assumptions are listed
- issue taxonomy is respected
- json outputs pass schema validation when strict mode is requested

### Phase 7: finalize
Declare execution complete only when:
- goal is defined
- plan exists
- blocking questions are closed or explicitly waived
- required outputs are generated
- validation is complete
- the user has signed off or explicitly allowed auto-finalization

If any of the above is false, return a `run-status.md` style summary instead of saying the task is complete.

## Input handling rules

Acceptable inputs:
- prototype images or screenshots
- page descriptions
- flow descriptions or process notes
- prd fragments
- meeting notes
- existing requirement drafts
- mixed chinese and english requirement text

### Input interpretation
- For screenshots and prototypes, infer visible pages, modules, fields, actions, states, and feedback messages.
- For text notes, extract conditions, constraints, business intent, and edge cases.
- For mixed materials, merge evidence instead of treating one source as authoritative by default.
- When sources disagree, record the disagreement as a conflict instead of silently resolving it.

## Mode contracts

- `assistant-plan`: return `intent summary`, `execution plan`, `blocking questions`, `recommendations`, `next action`
- `assistant-check`: return scope checked, issue summary, concrete findings, revision suggestions
- `assistant-analyze`: return object analyzed, key entities/relationships, risk points, downstream impact
- `assistant-ask`: return questions with why each matters and suggested options when possible
- `assistant-confirm`: return confirmed item, accepted assumptions, affected sections, execution readiness
- `assistant-execute`: generate only the approved artifacts
- `assistant-generate`: alias to execute if blockers are closed, otherwise route to plan

## Completion gate

Only report `execution complete` when all fields below are true.

- `goal_defined = true`
- `plan_generated = true`
- `blocking_questions_count = 0`
- `required_steps_completed = true`
- `validation_passed = true` when validation applies
- `user_signoff = true` or `user_allowed_auto_finalize = true`

If one or more are false, output a run status summary and say what is still needed.

## Mandatory issue taxonomy

Always classify discovered issues using this taxonomy.

### missing
A required element is absent.

### conflict
Two or more materials disagree.

### ambiguous
The wording is not executable.

### coverage-gap
The requirement may be buildable but is not sufficiently testable or reviewable.

## Strict JSON mode

Use strict JSON output when the user mentions any of these needs:
- json
- schema
- structured output
- machine-readable result
- codex ingestion
- api payload
- downstream automation

### JSON schema selection
- Use `requirement-package` for full-pass outputs.
- Use `issue-report` for checking and risk scanning outputs.
- Use `prd-bundle` for generated requirement deliverables.
- Use `run-status` style fields from `references/plan-templates.md` when the task is not yet complete.

### Script-assisted workflow
When you can work with files in a runtime environment, prefer this sequence:
1. Run `scripts/bootstrap_output.py <schema-name> <output.json>` to create a valid starter object.
2. Fill the JSON content.
3. Run `scripts/validate_output.py <schema-name> <output.json>`.
4. Return the validated JSON or embed it in the final response.

### Minimal valid examples
Use the example files in `examples/` as the canonical minimum valid payloads for each schema:
- `examples/requirement-package.min.json`
- `examples/issue-report.min.json`
- `examples/prd-bundle.min.json`

When a result is sparse, stay schema-valid by following these examples instead of inventing placeholder fields.

If file execution is not available, still conform to the same schema manually.

### Validation policy
- Never invent extra top-level keys outside the schema.
- Preserve enum values exactly as specified in the schema files.
- Put unresolved details into `pending_confirmations`, `assumptions`, or `limitations`.
- Prefer strict arrays and objects over prose paragraphs when JSON mode is requested.

## Command mapping

Map natural language internally to one of these modes.

- “计划 / plan / understand first / not yet generate / first figure out” -> plan
- “检查 / check / review / scan” -> check
- “分析 / analyze / impact / decompose” -> analyze
- “疑问 / ask / clarify / question” -> ask
- “确认 / confirm / lock / finalize / proceed with assumptions” -> confirm
- “执行 / execute / approved generate / proceed now” -> execute
- “生成 / generate / draft / output” -> if blocked then plan first, else execute

The user does not need to remember commands. Natural language is enough.

## Resources

Use these files when needed:
- `references/output-templates.md` for canonical output structures
- `references/issue-checklist.md` for issue discovery checklist
- `references/output-schema.md` for strict JSON selection and validation flow
- `references/json-examples.md` for example input to example JSON output patterns
- `references/plan-templates.md` for `intent-summary.md`, `execution-plan.md`, and `run-status.md` templates
- `references/workflow-notes.md` for staged execution and completion rules
- `schemas/*.schema.json` for exact machine-readable output contracts
- `scripts/bootstrap_output.py` to create starter JSON payloads
- `scripts/validate_output.py` to validate JSON outputs before returning them
