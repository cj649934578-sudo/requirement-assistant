#!/usr/bin/env python3
import argparse
import json
import os
import sys
from typing import Any, Dict, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIR = os.path.join(BASE_DIR, "schemas")
SCHEMA_MAP = {
    "requirement-package": "requirement-package.schema.json",
    "issue-report": "issue-report.schema.json",
    "prd-bundle": "prd-bundle.schema.json",
}


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def expect_type(errors: List[str], path: str, value: Any, expected: str):
    type_map = {
        "object": dict,
        "array": list,
        "string": str,
        "number": (int, float),
        "integer": int,
        "boolean": bool,
    }
    py_t = type_map[expected]
    if expected == "integer" and isinstance(value, bool):
        errors.append(f"{path}: expected integer, got boolean")
        return
    if expected == "number" and isinstance(value, bool):
        errors.append(f"{path}: expected number, got boolean")
        return
    if not isinstance(value, py_t):
        errors.append(f"{path}: expected {expected}, got {type(value).__name__}")


def validate(schema: Dict[str, Any], data: Any, path: str = "$", root: Dict[str, Any] = None) -> List[str]:
    root = root or schema
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            return [f"{path}: unsupported ref {ref}"]
        target = root
        for part in ref[2:].split("/"):
            target = target[part]
        return validate(target, data, path, root)
    errors: List[str] = []
    if "type" in schema:
        expect_type(errors, path, data, schema["type"])
        if errors:
            return errors

    if "enum" in schema and data not in schema["enum"]:
        errors.append(f"{path}: expected one of {schema['enum']}, got {data!r}")
        return errors

    if schema.get("type") == "object":
        props = schema.get("properties", {})
        required = schema.get("required", [])
        additional = schema.get("additionalProperties", True)
        for key in required:
            if key not in data:
                errors.append(f"{path}: missing required field '{key}'")
        for key, value in data.items():
            if key in props:
                errors.extend(validate(props[key], value, f"{path}.{key}", root))
            elif not additional:
                errors.append(f"{path}: unexpected field '{key}'")

    elif schema.get("type") == "array":
        items = schema.get("items")
        if "minItems" in schema and len(data) < schema["minItems"]:
            errors.append(f"{path}: expected at least {schema['minItems']} items, got {len(data)}")
        if items:
            for i, item in enumerate(data):
                errors.extend(validate(items, item, f"{path}[{i}]", root))

    elif schema.get("type") == "string":
        if "minLength" in schema and len(data) < schema["minLength"]:
            errors.append(f"{path}: expected min length {schema['minLength']}, got {len(data)}")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate JSON output against requirement-copilot schemas.")
    parser.add_argument("schema", choices=sorted(SCHEMA_MAP.keys()))
    parser.add_argument("json_file")
    args = parser.parse_args()

    schema = load_json(os.path.join(SCHEMA_DIR, SCHEMA_MAP[args.schema]))
    data = load_json(args.json_file)
    errors = validate(schema, data)
    if errors:
        print("VALIDATION FAILED")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)
    print("VALID")


if __name__ == "__main__":
    main()
