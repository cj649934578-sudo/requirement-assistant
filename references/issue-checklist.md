# Issue Discovery Checklist

Use this checklist during the automatic review phase.

## Completeness
- Is every critical page or flow represented?
- Does every major action have success and failure feedback?
- Do inputs define required/optional status?
- Do fields define validation rules?
- Are empty states, loading states, and failure states covered where relevant?
- Are role or permission differences defined where relevant?

## Consistency
- Do screenshots, notes, and flow descriptions agree?
- Do field rules align with submission rules?
- Do state definitions align with allowed actions?
- Do page descriptions align with scope statements?

## Ambiguity
- Are there fuzzy terms without conditions or audiences?
- Are the actor, object, and trigger all clear?
- Are time constraints specific?
- Are visibility rules explicit?

## Testability
- Can testers derive normal flow tests?
- Can testers derive abnormal flow tests?
- Are boundary conditions present?
- Are state transitions testable?
- Are permission combinations testable?

## Confirmation prompts
When important information is missing, prefer questions like:
- who can perform this action?
- under what condition is this field required?
- what should happen when submission fails?
- what is the expected behavior for empty or invalid input?
- what states can transition into and out of this state?
