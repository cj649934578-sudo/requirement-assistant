#!/usr/bin/env python3
import argparse
import json
from copy import deepcopy

REQUIREMENT_PACKAGE = {
    "schema_version": "1.0.0",
    "input_summary": {
        "materials": [],
        "language": "zh-CN",
        "assumptions": [],
        "limitations": []
    },
    "recognition_summary": {
        "pages_identified": 0,
        "modules_identified": 0,
        "fields_identified": 0,
        "actions_identified": 0,
        "rules_identified": 0,
        "states_identified": 0
    },
    "requirement_model": {
        "pages": [],
        "fields": [],
        "actions": [],
        "rules": [],
        "states": [],
        "exceptions": [],
        "test_points": []
    },
    "issues": [],
    "pending_confirmations": [],
    "generated_artifacts": {}
}

ISSUE_REPORT = {
    "schema_version": "1.0.0",
    "scope": {"task": "unspecified task", "objects": []},
    "summary": {"high": 0, "medium": 0, "low": 0},
    "issues": [],
    "pending_confirmations": []
}

PRD_BUNDLE = {
    "schema_version": "1.0.0",
    "artifact_type": "prd_bundle",
    "prd": {
        "title": "untitled prd",
        "background": "",
        "goals": [],
        "users_and_roles": [],
        "scope": {"in_scope": [], "out_of_scope": []},
        "pages_or_flows": [],
        "core_interactions": [],
        "business_rules": [],
        "exceptions_and_edge_cases": [],
        "pending_confirmations": []
    },
    "function_list": [],
    "test_points": [],
    "draft_test_cases": []
}

TEMPLATES = {
    "requirement-package": REQUIREMENT_PACKAGE,
    "issue-report": ISSUE_REPORT,
    "prd-bundle": PRD_BUNDLE,
}


def main():
    parser = argparse.ArgumentParser(description="Create a starter JSON file for requirement-copilot schemas.")
    parser.add_argument("kind", choices=sorted(TEMPLATES.keys()))
    parser.add_argument("output")
    args = parser.parse_args()

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(deepcopy(TEMPLATES[args.kind]), f, ensure_ascii=False, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
