# Output Templates

Use these templates when the user asks for formal outputs or when consistency matters.

## 1. Recognition summary

```markdown
## Recognition summary
- Pages identified:
- Modules identified:
- Fields identified:
- Actions identified:
- Rules identified:
- States identified:
- Key assumptions:
```

## 2. Structured requirement model

```markdown
## Structured requirement model
### Pages
- Page name:
  - Goal:
  - Entry:
  - Key modules:

### Fields
- Field name:
  - Type:
  - Required:
  - Validation:
  - Visibility:
  - Default:

### Actions
- Action name:
  - Trigger:
  - Preconditions:
  - Success result:
  - Failure result:

### Rules
- Rule:
  - Condition:
  - Effect:

### States
- State:
  - Enter condition:
  - Exit condition:
  - Available actions:
```

## 3. Issue list

```markdown
## Issue list
### High priority
- [type] title
  - Why it matters:
  - Evidence:
  - Suggestion:

### Medium priority
...

### Low priority
...
```

## 4. Pending confirmations

```markdown
## Pending confirmations
1. Question:
   - Why this must be confirmed:
   - Suggested options:
```

## 5. PRD draft

```markdown
# PRD draft

## Background and goal

## Users and roles

## Scope

## Pages / flow description

## Core interactions

## Business rules

## Exceptions and edge cases

## Pending confirmations
```

## 6. Function list

```markdown
## Function list
| Module | Function point | Trigger | Precondition | Result | Exception/Note |
|---|---|---|---|---|---|
```

## 7. Test points

```markdown
## Test points
### Object
- Normal path:
- Abnormal path:
- Boundary cases:
- Permission cases:
- State/transition cases:
```

## 8. Draft test cases

```markdown
## Draft test cases
### Case 1: [title]
- Preconditions:
- Steps:
- Expected result:
- Priority:
```


## Plan-first note

For image-first or underspecified tasks, prefer producing `intent-summary.md`, `execution-plan.md`, and `run-status.md` before a full PRD.
