# Plan Templates

Use these fixed templates for plan-first execution.

`assistant-action` is the recommended workflow entry.
It should first produce `intent-summary.md` and `execution-plan.md`, then report `run-status.md` style state and wait for user confirmation when the run cannot safely continue.

Recommended file locations:
- `docs/requirement-assistant/intent/YYYY-MM-DD-<topic>-intent-summary.md`
- `docs/requirement-assistant/plan/YYYY-MM-DD-<topic>-execution-plan.md`
- `docs/requirement-assistant/status/YYYY-MM-DD-<topic>-run-status.md`

## intent-summary.md

```md
# Intent Summary

## Metadata
- date: [YYYY-MM-DD]
- topic: [stable-topic-slug]
- entry command: [assistant-action / assistant-plan / assistant-check / assistant-analyze / assistant-ask / assistant-confirm / assistant-execute]

## User goal
[one sentence]

## Requested output
[list requested artifacts]

## Scope judgment
[page optimization / logic change / review only / mixed]

## Input inventory
- screenshots:
- notes:
- flow descriptions:
- existing prd:
- template requirements:

## Known facts
- 

## Unclear points
- 

## Recommended mode
[plan / analyze / check / ask / confirm / execute]

## Current phase
[intent]
```

## execution-plan.md

```md
# Execution Plan

## Metadata
- date: [YYYY-MM-DD]
- topic: [stable-topic-slug]
- derived from: [intent-summary file or request summary]

## User goal
[summary]

## Current judgment
- material completeness: [high / medium / low]
- suitable for direct execution: [yes / no]
- recommended mode: [plan / analyze / check / ask / confirm / execute]
- current workflow phase: [plan]

## Input inventory
- screenshots:
- notes:
- flow descriptions:
- existing prd:
- template requirements:

## Recognized content
- pages/modules:
- key fields:
- key actions:
- initial rules:
- initial risks:

## Planned steps
1.
2.
3.
4.

## Blocking questions
1.
2.
3.

## Completed steps
- [intent captured]

## Recommendations
- 
- 

## Next action
[wait for confirmation / ask blocking questions / proceed with assumptions / continue to next phase]
```

## run-status.md

```md
# Run Status

## Metadata
- date: [YYYY-MM-DD]
- topic: [stable-topic-slug]
- status-file: [this file path]

## Current phase
[intent / plan / ask / confirm / execute / verify / finalize]

## Last completed phase
[intent / plan / ask / confirm / execute / verify / none]

## Goal status
[defined / unclear]

## Plan status
[not started / ready / approved]

## Blocking questions
[number]

## Execution status
[not started / in progress / complete / blocked]

## Validation status
[not applicable / pending / passed / failed]

## Resume from
[phase name]

## Can finalize
[yes / no]

## Next action
[one sentence]

## Notes
- [what was completed]
- [what is blocked]
- [what the user needs to confirm]
```
