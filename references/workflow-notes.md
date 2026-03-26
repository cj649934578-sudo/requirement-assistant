# Workflow Notes

## Plan-first policy

Use plan-first execution whenever the user provides screenshots, vague requests, partial requirement materials, or multiple possible deliverables.

Do not generate a full PRD immediately in these cases.

`assistant-action` is the preferred entry command for this workflow.
It should drive the internal phase order:
- `intent -> plan -> ask -> confirm -> execute -> verify -> finalize`

The assistant should report the current phase whenever the workflow pauses.
The user does not need to manually invoke every phase command.

When the workflow is paused:
- return `run-status.md` style state
- state the current phase, last completed phase, and next action
- make it clear whether the run can continue immediately or is waiting on user confirmation

When the user comes back later:
- resume from the latest unfinished phase by default
- restart from an earlier phase only if new inputs materially change scope, assumptions, or outputs

## Completion policy

A task is complete only when:
- the goal is defined
- an execution plan exists
- blocking questions are closed or explicitly waived
- required outputs are generated
- validation has passed when required
- the user signed off or allowed auto-finalization

If any item above is false, return `run-status.md` instead of declaring success.

## Recommendation policy

When asking questions, always add a recommendation. Do not ask passive questions without guidance.

## Fast draft exception

Fast draft mode is allowed only when the user explicitly asks for a rough draft now and accepts missing-context risk.
In that case:
- label the result as draft
- list assumptions clearly
- preserve pending confirmations
