#!/usr/bin/env python3
"""Validate LLM-generated modules against a target vSphere API spec version."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULES_DIR = REPO_ROOT / "plugins" / "modules"
SPECS_DIR = REPO_ROOT / "config" / "api_specifications"

DEFAULT_TARGET_VERSION = "8.0.2"


@dataclass
class Operation:
    method: str
    path: str
    body_fields: set[str] = field(default_factory=set)
    query_fields: set[str] = field(default_factory=set)


@dataclass
class BreakingChange:
    category: str
    method: str
    path: str
    detail: str


def strip_query(path: str) -> str:
    return path.split("?", 1)[0]


def normalize_path_template(path: str) -> str:
    """Normalize path for comparison: strip query, unify param placeholder names."""
    base = strip_query(path)
    return re.sub(r"\{[^}]+\}", "{}", base)


def path_variants(path: str) -> list[str]:
    base = strip_query(path)
    variants = [base]
    if not base.startswith("/api"):
        variants.append("/api" + base)
    else:
        variants.append(base[4:] if base.startswith("/api") else base)

    parts = base.rstrip("/").split("/")
    if len(parts) > 1:
        last = parts[-1]
        if "{" not in last and "-" not in last:
            for suffix in ("pool", "policy", "profile", "filesystem"):
                if last.endswith(suffix) and len(last) > len(suffix):
                    hyphenated = last[: -len(suffix)] + "-" + suffix
                    hyp_parts = parts[:-1] + [hyphenated]
                    for prefix in ("", "/api"):
                        variants.append(prefix + "/".join(hyp_parts))

    if "{library}" in base:
        variants.append(base.replace("{library}", "{library_id}"))
        variants.append("/api" + base.replace("{library}", "{library_id}"))

    return list(dict.fromkeys(variants))


def action_path_candidates(path: str) -> list[str]:
    """Return path variants including /api prefix for action (query) endpoints."""
    candidates = [path]
    if not path.startswith("/api"):
        candidates.append("/api" + path)
    return list(dict.fromkeys(candidates))


def build_action_path(path: str, query_fields: dict[str, str]) -> str:
    action = query_fields.get("action")
    if action:
        return f"{strip_query(path)}?action={action}"
    return strip_query(path)


def parse_query_dict(tail: str) -> dict[str, str]:
    query: dict[str, str] = {}
    query_match = re.search(r"query\s*=\s*\{([^}]*)\}", tail, re.DOTALL)
    if not query_match:
        return query
    for qm in re.finditer(r'"([^"]+)"\s*:\s*"([^"]+)"', query_match.group(1)):
        query[qm.group(1)] = qm.group(2)
    return query


def load_all_specs(version: str) -> tuple[dict, dict]:
    version_dir = SPECS_DIR / version
    merged_paths: dict = {}
    merged_data: dict = {"components": {"schemas": {}}, "definitions": {}}
    for spec_path in sorted(version_dir.rglob("*.json")):
        with spec_path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        merged_paths.update(data.get("paths", {}))
        merged_data["components"]["schemas"].update(
            data.get("components", {}).get("schemas", {})
        )
        merged_data["definitions"].update(data.get("definitions", {}))
    return merged_paths, merged_data


def find_path_ops(spec_paths: dict, path: str) -> tuple[str | None, dict | None]:
    # Action endpoints: match full path including ?action= before stripping query.
    if "?" in path:
        for candidate in action_path_candidates(path):
            if candidate in spec_paths:
                return candidate, spec_paths[candidate]

    for variant in path_variants(path):
        if variant in spec_paths:
            return variant, spec_paths[variant]

    target_norm = normalize_path_template(path)
    for spec_path, ops in spec_paths.items():
        if normalize_path_template(spec_path) == target_norm:
            return spec_path, ops

    return None, None


def resolve_ref(spec: dict, ref: str) -> dict:
    if ref.startswith("#/components/schemas/"):
        return spec.get("components", {}).get("schemas", {}).get(ref.split("/")[-1], {})
    if ref.startswith("#/definitions/"):
        return spec.get("definitions", {}).get(ref.split("/")[-1], {})
    return {}


def get_request_schema(spec_data: dict, operation: dict) -> dict:
    if "requestBody" in operation:
        content = operation["requestBody"].get("content", {})
        for media in content.values():
            schema = media.get("schema", {})
            if "$ref" in schema:
                return resolve_ref(spec_data, schema["$ref"])
            return schema
    for param in operation.get("parameters", []):
        if param.get("in") == "body":
            schema = param.get("schema", {})
            if "$ref" in schema:
                return resolve_ref(spec_data, schema["$ref"])
            return schema
    return {}


def schema_properties(schema: dict, spec_data: dict) -> dict:
    if not schema:
        return {}
    if "$ref" in schema:
        schema = resolve_ref(spec_data, schema["$ref"])
    props = dict(schema.get("properties", {}))
    for key, value in list(props.items()):
        if "$ref" in value:
            props[key] = resolve_ref(spec_data, value["$ref"])
    return props


def schema_required(schema: dict, spec_data: dict) -> set[str]:
    if not schema:
        return set()
    if "$ref" in schema:
        schema = resolve_ref(spec_data, schema["$ref"])
    return set(schema.get("required", []))


def parse_llm_module(path: Path) -> dict | None:
    content = path.read_text(encoding="utf-8")
    if "This module is generated using LLM agents" not in content:
        return None
    gen_match = re.search(
        r"Generated from vSphere API spec ([0-9]+\.[0-9]+\.[0-9]+)\.",
        content,
    )
    if not gen_match:
        return None
    return {
        "content": content,
        "source_version": gen_match.group(1),
    }


def has_support_note(content: str, target_version: str) -> bool:
    return f"Has support for vSphere API {target_version}." in content


def same_major_version(source: str, target: str) -> bool:
    return source.split(".", 1)[0] == target.split(".", 1)[0]


def extract_path_constants(content: str) -> dict[str, str]:
    constants = {}
    for match in re.finditer(
        r"^([A-Z][A-Z0-9_]*)\s*=\s*[\"']([^\"']+)[\"']",
        content,
        re.MULTILINE,
    ):
        name, value = match.groups()
        if "PATH" in name or name == "PATH":
            constants[name] = value
    return constants


def extract_body_constants(content: str) -> dict[str, set[str]]:
    bodies: dict[str, set[str]] = {}
    for match in re.finditer(
        r"^(_[A-Z_]+)\s*=\s*\{([^}]+)\}",
        content,
        re.MULTILINE | re.DOTALL,
    ):
        name = match.group(1)
        fields = {m.group(1) for m in re.finditer(r"\"([^\"]+)\"\s*:", match.group(2))}
        bodies[name] = fields
    return bodies


def extract_payload_format(content: str) -> dict[str, dict]:
    payload_format: dict[str, dict] = {}
    pf_match = re.search(r"(?:_)?PAYLOAD_FORMAT\s*=\s*\{", content)
    if not pf_match:
        return payload_format

    start = pf_match.end() - 1
    depth = 0
    end = start
    while end < len(content):
        if content[end] == "{":
            depth += 1
        elif content[end] == "}":
            depth -= 1
            if depth == 0:
                end += 1
                break
        end += 1
    block = content[start:end]
    body_constants = extract_body_constants(content)

    for op_match in re.finditer(
        r"\"([a-z_]+)\"\s*:\s*\{(.*?)\n\s*\}",
        block,
        re.DOTALL,
    ):
        op_name = op_match.group(1)
        op_block = op_match.group(2)
        body_fields: set[str] = set()
        body_match = re.search(r"\"body\"\s*:\s*(\{[^}]*\}|_[A-Z_]+)", op_block)
        if body_match:
            body_ref = body_match.group(1).strip()
            if body_ref.startswith("{"):
                body_fields = {
                    m.group(1) for m in re.finditer(r"\"([^\"]+)\"\s*:", body_ref)
                }
            elif body_ref in body_constants:
                body_fields = body_constants[body_ref]

        query_fields: dict[str, str] = {}
        query_match = re.search(r"\"query\"\s*:\s*\{([^}]*)\}", op_block)
        if query_match:
            for qm in re.finditer(
                r"\"([^\"]+)\"\s*:\s*(?:\"([^\"]+)\"|([a-z_]+))",
                query_match.group(1),
            ):
                api_field = qm.group(1)
                literal = qm.group(2) or qm.group(3)
                query_fields[api_field] = literal

        payload_format[op_name] = {
            "body_fields": body_fields,
            "query_fields": query_fields,
        }

    return payload_format


def extract_client_operations(
    content: str,
    path_constants: dict[str, str],
    payload_format: dict[str, dict],
) -> list[tuple[str, str, str | None, dict[str, str]]]:
    operations: list[tuple[str, str, str | None, dict[str, str]]] = []

    def add(method: str, path: str, op: str | None = None, query: dict | None = None):
        query_fields = dict(query or {})
        if not query_fields and op and op in payload_format:
            query_fields = dict(payload_format[op].get("query_fields", {}))
        if "?" in path:
            full_path = path
        else:
            full_path = build_action_path(path, query_fields)
        operations.append((method.lower(), full_path, op, query_fields))

    for match in re.finditer(
        r"self\.client\.(get|post|put|patch|delete)\(\s*([A-Z][A-Z0-9_]*)\b([^)]*)\)",
        content,
        re.DOTALL,
    ):
        method, const, tail = match.groups()
        if const in path_constants:
            add(method, path_constants[const], None, parse_query_dict(tail))

    for match in re.finditer(
        r"self\.client\.(get|post|put|patch|delete)\(\s*[\"']([^\"']+)[\"']",
        content,
    ):
        method, literal = match.groups()
        add(method, literal)

    for match in re.finditer(
        r"self\.client\.request\(\s*[\"'](GET|POST|PUT|PATCH|DELETE)[\"']\s*,\s*([A-Z][A-Z0-9_]*)\b([^)]*)\)",
        content,
        re.DOTALL,
    ):
        method, const, tail = match.groups()
        if const in path_constants:
            add(method, path_constants[const], None, parse_query_dict(tail))

    for match in re.finditer(
        r"fetch_list\(\s*([A-Z][A-Z0-9_]*)\s*,\s*(?:self\.)?(?:_)?PAYLOAD_FORMAT\[\"([a-z_]+)\"\]",
        content,
    ):
        const, op = match.groups()
        if const in path_constants:
            add("get", path_constants[const], op)

    for match in re.finditer(
        r"path\s*=\s*self\.build_path\(\s*([A-Z][A-Z0-9_]*)\b[^)]*\)\s*\n\s*return self\.fetch_list\(path",
        content,
    ):
        const = match.group(1)
        if const in path_constants:
            add("get", path_constants[const])

    for match in re.finditer(
        r"self\.client\.(get|post|put|patch|delete)\(\s*path\b([^)]*)\)",
        content,
        re.DOTALL,
    ):
        method = match.group(1)
        call_tail = match.group(2)
        query = parse_query_dict(call_tail)
        if not query and "query=query" in call_tail:
            preceding = content[max(0, match.start() - 500) : match.start()]
            qm = re.search(
                r'query\s*=\s*self\.build_query\(self\.PAYLOAD_FORMAT\["([a-z_]+)"\]\)',
                preceding,
            )
            if qm and qm.group(1) in payload_format:
                query = dict(payload_format[qm.group(1)].get("query_fields", {}))
        pos = match.start()
        bp_matches = re.findall(r"build_path\(\s*([A-Z][A-Z0-9_]*)\b", content[:pos])
        if bp_matches and bp_matches[-1] in path_constants:
            add(method, path_constants[bp_matches[-1]], None, query)

    for match in re.finditer(
        r"build_payload\((?:self\.)?(?:_)?PAYLOAD_FORMAT\[\"([a-z_]+)\"\]\)",
        content,
    ):
        op = match.group(1)
        after = content[match.end() : match.end() + 500]
        client_match = re.search(
            r"self\.client\.(get|post|put|patch|delete)\(\s*([A-Z][A-Z0-9_]*|path)\b([^)]*)\)",
            after,
            re.DOTALL,
        )
        if not client_match:
            continue
        method, target, call_tail = client_match.groups()
        query = dict(payload_format.get(op, {}).get("query_fields", {}))
        query.update(parse_query_dict(call_tail))
        if target in path_constants:
            add(method, path_constants[target], op, query)
        elif target == "path":
            bp_matches = re.findall(
                r"build_path\(\s*([A-Z][A-Z0-9_]*)\b",
                content[: match.end() + len(after)],
            )
            if bp_matches and bp_matches[-1] in path_constants:
                add(method, path_constants[bp_matches[-1]], op, query)

    for match in re.finditer(
        r"update_if_changed\(\s*self\.build_path\(\s*([A-Z][A-Z0-9_]*)\b",
        content,
    ):
        const = match.group(1)
        if const in path_constants:
            add("patch", path_constants[const], "update")

    for match in re.finditer(
        r"path\s*=\s*self\.build_path\(\s*([A-Z][A-Z0-9_]*)\b[^)]*\)[\s\S]{0,300}?update_if_changed\(\s*path",
        content,
    ):
        const = match.group(1)
        if const in path_constants:
            add("patch", path_constants[const], "update")

    if "_ACTIONS" in content and "DIRECTORIES_PATH" in path_constants:
        block = re.search(r"_ACTIONS\s*=\s*\{([^}]+)\}", content, re.DOTALL)
        if block:
            base = strip_query(path_constants["DIRECTORIES_PATH"])
            for am in re.finditer(r'"([a-z_]+)"\s*:\s*"([^"]+)"', block.group(1)):
                add("post", f"{base}?action={am.group(2)}")

    post_action_match = re.search(
        r"def _post_action\(self, action\):.*?self\.client\.request\(\s*"
        r'["\']POST["\']\s*,\s*([A-Z][A-Z0-9_]*)',
        content,
        re.DOTALL,
    )
    if post_action_match:
        const = post_action_match.group(1)
        if const in path_constants:
            for am in re.finditer(r'_post_action\("([^"]+)"\)', content):
                add("post", path_constants[const], None, {"action": am.group(1)})

    resize_match = re.search(
        r"def _post_resize\(self, action\):.*?self\.client\.request\(\s*"
        r'["\']POST["\']\s*,\s*([A-Z][A-Z0-9_]*)',
        content,
        re.DOTALL,
    )
    if resize_match:
        const = resize_match.group(1)
        if const in path_constants:
            for op_name in payload_format:
                action_val = "resize-ex" if op_name == "resize_ex" else op_name
                add("post", path_constants[const], op_name, {"action": action_val})

    for match in re.finditer(
        r'query\s*=\s*self\.build_query\(self\.PAYLOAD_FORMAT\["([a-z_]+)"\]\)'
        r"[\s\S]{0,400}?self\.client\.post\(\s*path",
        content,
    ):
        op = match.group(1)
        pf = payload_format.get(op, {})
        query = dict(pf.get("query_fields", {}))
        bp_matches = re.findall(
            r"build_path\(\s*([A-Z][A-Z0-9_]*)\b",
            content[: match.end()],
        )
        if bp_matches and bp_matches[-1] in path_constants:
            add("post", path_constants[bp_matches[-1]], op, query)

    return operations


def dedupe_operations(
    raw_ops: list[tuple[str, str, str | None, dict[str, str]]],
    payload_format: dict[str, dict],
) -> list[Operation]:
    seen: set[tuple[str, str]] = set()
    result: list[Operation] = []
    action_bases = {
        strip_query(path)
        for method, path, _op, _query in raw_ops
        if "?" in path and method == "post"
    }

    for method, path, op_name, query in raw_ops:
        if method == "post" and "?" not in path and strip_query(path) in action_bases:
            continue

        key = (method.lower(), path)
        if key in seen:
            continue
        seen.add(key)
        body_fields: set[str] = set()
        query_fields: set[str] = set(query.keys()) if query else set()
        if op_name and op_name in payload_format:
            body_fields = payload_format[op_name].get("body_fields", set())
            query_fields |= set(payload_format[op_name].get("query_fields", {}).keys())
        result.append(
            Operation(
                method=method.lower(),
                path=path,
                body_fields=body_fields,
                query_fields=query_fields,
            )
        )
    return result


def compare_operation(
    op: Operation,
    target_paths: dict,
    target_spec_data: dict,
    target_version: str,
) -> list[BreakingChange]:
    issues: list[BreakingChange] = []
    resolved_path, path_ops = find_path_ops(target_paths, op.path)
    if not path_ops:
        issues.append(
            BreakingChange(
                "Missing endpoint",
                op.method.upper(),
                op.path,
                f"path not present in {target_version} spec",
            )
        )
        return issues

    operation = path_ops.get(op.method)
    if not operation:
        issues.append(
            BreakingChange(
                "Missing method",
                op.method.upper(),
                op.path,
                f"path exists as {resolved_path} but {op.method.upper()} not supported",
            )
        )
        return issues

    req_schema = get_request_schema(target_spec_data, operation)
    required = schema_required(req_schema, target_spec_data)
    props = schema_properties(req_schema, target_spec_data)

    missing_required = required - op.body_fields
    if missing_required and op.body_fields:
        issues.append(
            BreakingChange(
                "Required body field added",
                op.method.upper(),
                op.path,
                f"target requires {sorted(missing_required)} not sent by module",
            )
        )

    for field_name in op.body_fields:
        if field_name not in props and props:
            issues.append(
                BreakingChange(
                    "Body field removed or renamed",
                    op.method.upper(),
                    op.path,
                    f"module sends '{field_name}' absent from target request schema",
                )
            )

    return issues


def update_module_notes(module_path: Path, target_version: str) -> None:
    content = module_path.read_text(encoding="utf-8")
    note = f"  - Has support for vSphere API {target_version}."
    if note.strip() in content:
        return

    gen_match = re.search(
        r"(  - Generated from vSphere API spec [0-9]+\.[0-9]+\.[0-9]+\.\n)",
        content,
    )
    if not gen_match:
        return

    content = content.replace(gen_match.group(1), gen_match.group(1) + note + "\n")
    module_path.write_text(content, encoding="utf-8")


def validate_module(
    module_name: str,
    target_paths: dict,
    target_spec_data: dict,
    target_version: str,
    update_notes: bool,
) -> dict:
    module_path = MODULES_DIR / f"{module_name}.py"
    meta = parse_llm_module(module_path)
    if not meta:
        return {
            "module": module_name,
            "status": "skipped",
            "reason": "not LLM-generated",
        }

    source_version = meta["source_version"]
    if same_major_version(source_version, target_version):
        return {
            "module": module_name,
            "status": "skipped",
            "reason": f"generated from same major version ({source_version})",
        }

    if has_support_note(meta["content"], target_version):
        return {
            "module": module_name,
            "status": "skipped",
            "reason": f"already documents support for {target_version}",
        }

    content = meta["content"]
    path_constants = extract_path_constants(content)
    payload_format = extract_payload_format(content)
    raw_ops = extract_client_operations(content, path_constants, payload_format)
    operations = dedupe_operations(raw_ops, payload_format)

    if not operations:
        return {
            "module": module_name,
            "status": "error",
            "reason": "no API operations extracted",
        }

    all_issues: list[BreakingChange] = []
    for op in operations:
        all_issues.extend(
            compare_operation(op, target_paths, target_spec_data, target_version)
        )

    if all_issues:
        return {
            "module": module_name,
            "status": "incompatible",
            "operations": [(o.method, o.path) for o in operations],
            "issues": all_issues,
        }

    if update_notes:
        update_module_notes(module_path, target_version)

    return {
        "module": module_name,
        "status": "compatible",
        "operations": [(o.method, o.path) for o in operations],
    }


def resolve_target_version(requested: str) -> str:
    requested = re.sub(r"^[^0-9]*", "", requested.strip())
    if not requested:
        raise ValueError("target version is required")

    available = sorted(
        p.name
        for p in SPECS_DIR.iterdir()
        if p.is_dir() and re.match(r"^[0-9]", p.name)
    )
    if requested in available:
        return requested

    major = requested.split(".", 1)[0]
    matches = [v for v in available if v.startswith(major + ".")]
    if matches:
        return matches[-1]

    raise ValueError(f"No spec for {requested!r}. Available: {', '.join(available)}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate LLM-generated modules against a vSphere API spec version.",
    )
    parser.add_argument(
        "--target",
        default=DEFAULT_TARGET_VERSION,
        help=f"Target API version directory name (default: {DEFAULT_TARGET_VERSION})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report results without updating module notes",
    )
    parser.add_argument(
        "modules",
        nargs="*",
        help="Optional module names (without .py). Default: all LLM-generated modules",
    )
    args = parser.parse_args()

    try:
        target_version = resolve_target_version(args.target)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    target_paths, target_spec_data = load_all_specs(target_version)

    if args.modules:
        llm_modules = sorted(args.modules)
    else:
        llm_modules = sorted(
            p.stem
            for p in MODULES_DIR.glob("*.py")
            if p.name != "__init__.py" and parse_llm_module(p) is not None
        )

    compatible: list[str] = []
    incompatible: list[dict] = []
    skipped: list[dict] = []
    errors: list[dict] = []

    for name in llm_modules:
        result = validate_module(
            name,
            target_paths,
            target_spec_data,
            target_version,
            update_notes=not args.dry_run,
        )
        status = result["status"]
        if status == "compatible":
            compatible.append(name)
        elif status == "incompatible":
            incompatible.append(result)
        elif status == "skipped":
            skipped.append(result)
        else:
            errors.append(result)

    print(f"# vSphere {target_version} compatibility validation")
    print(f"LLM-generated modules checked: {len(llm_modules)}")
    print(f"Compatible: {len(compatible)}")
    print(f"Incompatible: {len(incompatible)}")
    print(f"Skipped: {len(skipped)}")
    print(f"Errors: {len(errors)}")
    if args.dry_run:
        print("Mode: dry-run (module notes not updated)")
    print()

    if compatible:
        print("## Compatible modules")
        for name in compatible:
            print(f"- {name}")
        print()

    if incompatible:
        print("## Incompatible modules")
        for result in incompatible:
            print(f"\n### {result['module']}")
            for method, path in result.get("operations", []):
                print(f"  - {method.upper()} {path}")
            for issue in result["issues"]:
                print(
                    f"  - [{issue.category}] {issue.method} {issue.path}: {issue.detail}"
                )

    if skipped:
        print("\n## Skipped")
        for result in skipped:
            print(f"- {result['module']}: {result['reason']}")

    if errors:
        print("\n## Errors")
        for result in errors:
            print(f"- {result['module']}: {result['reason']}")

    return 1 if incompatible or errors else 0


if __name__ == "__main__":
    sys.exit(main())
