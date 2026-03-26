# Requirement Assistant Skill Operator Manual Design

Date: 2026-03-26

## Goal

Improve `SKILL.md` usability without changing the underlying workflow contract.

The current skill file is accurate but reads like a full policy document. It is harder than necessary to quickly answer:
- what the skill is for
- what the default output is
- when to stop at planning versus execute
- which schema to choose
- what each role should focus on

## Chosen Structure

Adopt a dual-layer structure:

1. `Operator Manual` at the top
   - Quick Start
   - Role Views
   - Modes at a glance
   - Gates
   - Outputs and schema selection
   - Command shortcuts
2. `Full Spec` below
   - Preserve the existing detailed workflow, taxonomy, strict JSON rules, and command mapping

## Constraints

- Do not change the meaning of the 7-phase workflow.
- Do not change schema-selection rules.
- Do not weaken confirmation or validation gates.
- Keep the full current spec in the same file for backward compatibility.

## Expected Outcome

After refactor, a reader should be able to understand the skill from the top section in under 2 minutes and still access the full normative spec below.
