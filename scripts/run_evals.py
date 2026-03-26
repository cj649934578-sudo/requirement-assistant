#!/usr/bin/env python3
import argparse
import json
import os
import sys
from typing import Any, Dict, Iterable, List

from validate_output import SCHEMA_MAP, load_json, validate

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIR = os.path.join(BASE_DIR, "schemas")


def values_at_path(data: Any, path: str) -> List[Any]:
    if not path.startswith("$."):
        raise ValueError(f"Unsupported path: {path}")
    tokens = path[2:].split(".")
    current = [data]
    for token in tokens:
        next_values: List[Any] = []
        if token.endswith("[*]"):
            key = token[:-3]
            for item in current:
                if not isinstance(item, dict):
                    continue
                value = item.get(key, [])
                if isinstance(value, list):
                    next_values.extend(value)
        else:
            for item in current:
                if isinstance(item, dict) and token in item:
                    next_values.append(item[token])
        current = next_values
    return current


def first_value(data: Any, path: str) -> Any:
    values = values_at_path(data, path)
    if not values:
        raise KeyError(f"No value at path {path}")
    return values[0]


def run_checks(case: Dict[str, Any], data: Any) -> List[str]:
    errors: List[str] = []
    checks = case.get("checks", {})

    for path, expected in checks.get("equals", {}).items():
        actual = first_value(data, path)
        if actual != expected:
            errors.append(f"{path}: expected {expected!r}, got {actual!r}")

    for path, minimum in checks.get("min_lengths", {}).items():
        actual = first_value(data, path)
        if not hasattr(actual, "__len__"):
            errors.append(f"{path}: value has no length")
            continue
        if len(actual) < minimum:
            errors.append(f"{path}: expected length >= {minimum}, got {len(actual)}")

    for path, expected_values in checks.get("contains_any", {}).items():
        actual_values = values_at_path(data, path)
        if not any(value in actual_values for value in expected_values):
            errors.append(f"{path}: expected one of {expected_values!r}, got {actual_values!r}")

    for path, expected_substrings in checks.get("contains_all_substrings", {}).items():
        actual = first_value(data, path)
        if not isinstance(actual, str):
            errors.append(f"{path}: expected string for substring check")
            continue
        for substring in expected_substrings:
            if substring not in actual:
                errors.append(f"{path}: missing substring {substring!r}")

    return errors


def iter_cases(manifest: Dict[str, Any], only: str = "") -> Iterable[Dict[str, Any]]:
    for case in manifest.get("cases", []):
        if only and case.get("name") != only:
            continue
        yield case


def main() -> None:
    parser = argparse.ArgumentParser(description="Run minimal eval checks against saved requirement-assistant outputs.")
    parser.add_argument("--manifest", default=os.path.join("evals", "baseline.json"))
    parser.add_argument("--case", default="")
    args = parser.parse_args()

    manifest_path = os.path.join(BASE_DIR, args.manifest)
    manifest = load_json(manifest_path)
    overall_errors: List[str] = []

    for case in iter_cases(manifest, args.case):
        name = case["name"]
        schema_name = case["schema"]
        output_path = os.path.join(BASE_DIR, case["output"])
        schema = load_json(os.path.join(SCHEMA_DIR, SCHEMA_MAP[schema_name]))
        data = load_json(output_path)

        schema_errors = validate(schema, data)
        if schema_errors:
            overall_errors.append(f"[{name}] schema validation failed")
            overall_errors.extend(f"[{name}] {error}" for error in schema_errors)
            continue

        check_errors = run_checks(case, data)
        if check_errors:
            overall_errors.extend(f"[{name}] {error}" for error in check_errors)
        else:
            print(f"PASS {name}")

    if overall_errors:
        print("EVAL FAILED")
        for error in overall_errors:
            print(f"- {error}")
        sys.exit(1)

    print("EVAL PASS")


if __name__ == "__main__":
    main()
