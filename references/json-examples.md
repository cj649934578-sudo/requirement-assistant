# JSON Examples

Use this file when the user requests strict JSON output, machine-readable output, or codex-ready payloads.

## Example 1: Full requirement package

### Example input
- Two prototype screenshots for an order submit page and an order result page
- Page notes:
  - user can enter receiver name, phone number, and address
  - submit button creates an order after validation
  - failed submission should show an inline error and keep entered values
- Flow note:
  - after successful submission, user goes to result page
  - after approval, the order becomes read-only

### Recommended schema
`requirement-package`

### Example output
```json
{
  "schema": "requirement-package",
  "recognition_summary": {
    "pages_detected": 2,
    "modules_detected": 3,
    "fields_detected": 3,
    "actions_detected": 2,
    "rules_detected": 3,
    "states_detected": 3
  },
  "requirement_model": {
    "pages": [
      {
        "name": "Order Submit Page",
        "purpose": "Collect receiver information and submit an order",
        "modules": [
          {
            "name": "Receiver Form",
            "fields": [
              {
                "name": "receiver_name",
                "label": "Receiver Name",
                "type": "text",
                "required": true,
                "validation": ["non-empty"]
              },
              {
                "name": "phone_number",
                "label": "Phone Number",
                "type": "text",
                "required": true,
                "validation": ["phone-format"]
              },
              {
                "name": "address",
                "label": "Address",
                "type": "textarea",
                "required": true,
                "validation": ["non-empty"]
              }
            ]
          }
        ],
        "actions": [
          {
            "name": "submit_order",
            "trigger": "click",
            "target": "Submit Button",
            "outcome": "validate fields and create order"
          }
        ]
      },
      {
        "name": "Order Result Page",
        "purpose": "Show order submission result",
        "modules": [],
        "actions": []
      }
    ],
    "rules": [
      {
        "name": "successful_submit_redirect",
        "condition": "submission succeeds",
        "effect": "navigate to result page"
      },
      {
        "name": "failed_submit_feedback",
        "condition": "submission fails",
        "effect": "show inline error and preserve entered values"
      },
      {
        "name": "approved_order_read_only",
        "condition": "order status is approved",
        "effect": "order becomes read-only"
      }
    ],
    "states": [
      {"name": "draft"},
      {"name": "submitted"},
      {"name": "approved"}
    ],
    "exceptions": [
      {
        "name": "submit_failure",
        "condition": "backend rejects submission",
        "handling": "show inline error and keep current inputs"
      }
    ],
    "test_points": [
      {
        "name": "successful submit",
        "type": "normal"
      },
      {
        "name": "submit with invalid phone number",
        "type": "abnormal"
      }
    ]
  },
  "issues": [],
  "pending_confirmations": [
    "whether approved orders can be reopened",
    "maximum address length"
  ],
  "generated_artifacts": {
    "prd_draft": "...",
    "function_list": [],
    "test_points": []
  },
  "assumptions": [
    "all three fields are visible on the same page"
  ],
  "limitations": []
}
```

## Example 2: Issue report for requirement checking

### Example input
- Existing PRD fragment says the coupon field is optional
- Submission rule says the coupon field must be filled before submission
- No description for invalid coupon handling

### Recommended schema
`issue-report`

### Example output
```json
{
  "schema": "issue-report",
  "scope": "coupon submission rules",
  "summary": {
    "total_issues": 2,
    "high": 1,
    "medium": 1,
    "low": 0
  },
  "issues": [
    {
      "type": "conflict",
      "severity": "high",
      "title": "coupon field optionality conflicts with submission rule",
      "description": "The PRD describes the coupon field as optional, but the submission rule requires it before submission.",
      "impact_scope": ["form validation", "frontend implementation", "test design"],
      "suggestion": "Confirm whether coupon is truly optional or conditionally required."
    },
    {
      "type": "missing",
      "severity": "medium",
      "title": "missing invalid coupon handling",
      "description": "No behavior is defined when the coupon code format is invalid or rejected.",
      "impact_scope": ["error feedback", "test cases"],
      "suggestion": "Add validation and user-visible error handling for invalid coupon input."
    }
  ],
  "pending_confirmations": [
    "is coupon required for all orders or only for campaign orders"
  ],
  "assumptions": [],
  "limitations": []
}
```

## Example 3: PRD bundle output

### Example input
- Requirement note for a refund request page
- User can select reason, upload up to 3 images, submit refund request, and view result
- Testing needs a structured PRD plus test points only

### Recommended schema
`prd-bundle`

### Example output
```json
{
  "schema_version": "1.0.0",
  "artifact_type": "prd_bundle",
  "prd": {
    "title": "退款申请功能 PRD",
    "background": "Allow users to submit refund requests with evidence.",
    "goals": ["Support structured refund submission with evidence upload."],
    "users_and_roles": ["buyer"],
    "scope": {
      "in_scope": ["refund reason selection", "image upload", "refund request submission"],
      "out_of_scope": ["refund approval back-office workflow"]
    },
    "pages_or_flows": ["Refund Request Page", "Refund Result Page"],
    "core_interactions": ["select refund reason", "upload up to 3 images", "submit refund request"],
    "business_rules": ["at least one refund reason is required", "maximum image upload count is 3"],
    "exceptions_and_edge_cases": ["upload failure", "submit failure", "oversized image"],
    "pending_confirmations": ["allowed image formats", "maximum file size"]
  },
  "function_list": [
    {
      "module": "Refund Form",
      "function_point": "Submit refund request",
      "trigger": "click submit",
      "precondition": "reason selected",
      "result": "request submitted successfully",
      "exception_or_note": "show error when submission fails"
    }
  ],
  "test_points": [
    {
      "object": "refund request submission",
      "normal_path": ["submit with valid reason and images"],
      "abnormal_path": ["submit without reason", "upload unsupported image"],
      "boundary_cases": ["upload exactly 3 images", "upload 4 images"],
      "permission_cases": ["buyer only"],
      "state_or_transition_cases": ["draft to submitted"]
    }
  ],
  "draft_test_cases": [
    {
      "case_title": "退款申请模块-提交成功",
      "preconditions": [
        "用户已登录买家账号",
        "当前订单支持发起退款申请",
        "退款申请页面已成功打开"
      ],
      "steps": [
        "在退款原因下拉框中选择任意有效退款原因",
        "上传 1 张格式正确且大小符合限制的凭证图片",
        "点击提交退款申请按钮"
      ],
      "expected_result": "退款申请提交成功，页面展示提交成功反馈，并进入退款结果页或成功状态。",
      "priority": "P1"
    }
  ]
}
```

## Usage notes
- Prefer these examples when schema selection is clear but the user did not provide an exact output skeleton.
- Keep enum values and required top-level keys consistent with the actual JSON schema files.
- If a field is unknown, do not invent it. Use the schema's pending confirmation or limitation fields instead.

## Minimal valid payloads
For bare-minimum schema-compliant outputs, inspect the example files bundled in `examples/`. They are intentionally sparse and useful for bootstrapping or automated tests:

- `examples/requirement-package.min.json`
- `examples/issue-report.min.json`
- `examples/prd-bundle.min.json`
