# Strict JSON Output and Validation

Use this reference when the user wants machine-readable output for GPT, Codex, downstream APIs, or automated pipelines.

## Supported schemas

### 1. requirement-package
Use for full-pass outputs that include recognition, requirement modeling, issue discovery, confirmations, and optional generated artifacts.

Schema file:
- `schemas/requirement-package.schema.json`

Bootstrap command:
```bash
scripts/bootstrap_output.py requirement-package /tmp/requirement-package.json
```

Validate command:
```bash
scripts/validate_output.py requirement-package /tmp/requirement-package.json
```

### 2. issue-report
Use for review-focused outputs when the user asks mainly for checking, scanning, or risk identification.

Schema file:
- `schemas/issue-report.schema.json`

Bootstrap command:
```bash
scripts/bootstrap_output.py issue-report /tmp/issue-report.json
```

Validate command:
```bash
scripts/validate_output.py issue-report /tmp/issue-report.json
```

### 3. prd-bundle
Use when the user wants generated requirement deliverables in machine-readable form.

Schema file:
- `schemas/prd-bundle.schema.json`

Bootstrap command:
```bash
scripts/bootstrap_output.py prd-bundle /tmp/prd-bundle.json
```

Validate command:
```bash
scripts/validate_output.py prd-bundle /tmp/prd-bundle.json
```

## Schema selection rules

- Choose `requirement-package` for full analysis or mixed requests.
- Choose `issue-report` for check / review / scan requests.
- Choose `prd-bundle` for generate / draft requests.
- If the user explicitly asks for JSON schema output, prefer one of these schemas over free-form markdown.

## Output discipline

When producing strict JSON:
- Do not add commentary inside the JSON object.
- Keep keys exactly as defined in the schema.
- Use empty arrays instead of omitting optional list fields when feasible.
- Put uncertain content into `assumptions`, `limitations`, or `pending_confirmations` instead of fabricating facts.
- Validate with `scripts/validate_output.py` whenever you are working in a filesystem context.

## Minimal valid example files
Use these files when GPT or Codex needs the smallest legal payload for each schema, or when testing the bundled validator:

- `examples/requirement-package.min.json`
- `examples/issue-report.min.json`
- `examples/prd-bundle.min.json`

Recommended check commands:

```bash
python scripts/validate_output.py requirement-package examples/requirement-package.min.json
python scripts/validate_output.py issue-report examples/issue-report.min.json
python scripts/validate_output.py prd-bundle examples/prd-bundle.min.json
```
