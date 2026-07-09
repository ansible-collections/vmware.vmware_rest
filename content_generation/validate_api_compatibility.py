#!/usr/bin/env python
"""
Validate LLM-generated modules against a target vSphere API spec version.

This script validates that Ansible modules generated for one vSphere version can
work with a different (typically older) vSphere version by comparing the module's
API operations against the target version's OpenAPI specification.

Usage:
    # Validate all LLM-generated modules against vSphere 8.0.2
    python validate_api_compatibility.py --target 8.0.2

    # Validate specific modules
    python validate_api_compatibility.py --target 8.0.2 vcenter_datacenter vcenter_resourcepool

    # Dry run to see results without updating module notes
    python validate_api_compatibility.py --target 8.0.2 --dry-run

How It Works:
    1. Parses LLM-generated modules to extract:
       - API paths (GET, POST, PATCH, DELETE operations)
       - Request body fields
       - Query parameters (including ?action= for action endpoints)

       Supports both module formats:
       - Modern format: OperationConfig objects with body_spec/query_spec
       - Legacy format: PAYLOAD_FORMAT dictionaries and direct client calls

    2. Compares against target API spec to detect:
       - Missing endpoints (path doesn't exist)
       - Missing methods (path exists but HTTP method not supported)
       - Required body fields added (module doesn't send a now-required field)
       - Body fields removed/renamed (module sends a field that doesn't exist)

    3. Updates compatible modules with a note:
       "Has support for vSphere API {target_version}."

Module Format Support:
    Modern (2026) format:
        - OperationConfig objects (CREATE_OPERATION, UPDATE_OPERATION, etc.)
        - Endpoint constants (LIST_ENDPOINT, ITEM_ENDPOINT)
        - Structured body_spec and query_spec with nested subspec
        - ACTION_OPERATIONS dictionary for state-based actions
        - Base classes: VmwareRestCrudModuleBase, VmwareRestInfoModuleBase

    Legacy format:
        - PAYLOAD_FORMAT dictionaries
        - Direct self.client.* calls
        - PATH constants (LIST_PATH, ITEM_PATH)
        - Custom async functions

Output:
    Generates a markdown report with:
    - Summary statistics
    - Compatible modules list
    - Incompatible modules with specific breaking changes
    - Skipped modules (not LLM-generated, same major version, already documented)
    - Errors (no operations extracted, etc.)

Examples:

    # Standard validation against vSphere 8.0.2
    $ python validate_api_compatibility.py --target 8.0.2
    # vSphere 8.0.2 compatibility validation
    LLM-generated modules checked: 45
    Compatible: 38
    Incompatible: 2
    Skipped: 5
    Errors: 0

    ## Compatible modules
    - vcenter_datacenter
    - vcenter_folder
    - vcenter_resourcepool
    ...

    ## Incompatible modules

    ### vcenter_vm_hardware_cpu
      - PATCH /vcenter/vm/{vm}/hardware/cpu
      - [Required body field added] PATCH /vcenter/vm/{vm}/hardware/cpu: target requires ['hot_add_enabled'] not sent by module

    # Dry run to preview without updates
    $ python validate_api_compatibility.py --target 8.0.2 --dry-run
    Mode: dry-run (module notes not updated)
    ...

    # Validate only datacenter and resourcepool modules
    $ python validate_api_compatibility.py --target 8.0.2 vcenter_datacenter vcenter_resourcepool
    LLM-generated modules checked: 2
    Compatible: 2
    ...

    # Use major version (resolves to latest patch)
    $ python validate_api_compatibility.py --target 8
    # Resolves to 8.0.2 (latest available 8.x spec)

Module Detection:
    Only validates modules marked as LLM-generated with:
    - "This module is generated using LLM agents" in file content
    - "Generated from vSphere API spec X.Y.Z." version marker

    Skips modules if:
    - Not LLM-generated
    - Generated from same major version as target (e.g., 9.1.0 → 9.2.0)
    - Already has support note for target version

Path Matching Strategy:
    Uses flexible path matching to handle API inconsistencies:
    1. Exact match
    2. With/without /api prefix
    3. Hyphenated variants (resourcepool → resource-pool)
    4. Library ID variants ({library} → {library_id})
    5. Normalized template matching (strips parameters and query strings)

Breaking Change Categories:
    - Missing endpoint: Path doesn't exist in target spec
    - Missing method: Path exists but HTTP method not available
    - Required body field added: Target requires field module doesn't send
    - Body field removed or renamed: Module sends field absent from target

Exit Codes:
    0 - All modules compatible
    1 - One or more incompatibilities or errors found
    2 - Invalid target version or spec not found

Dependencies:
    - content_generation/api_specs/{version}/*.json - Target OpenAPI specs
    - plugins/modules/*.py - LLM-generated modules to validate

Notes:
    - Only validates API-level compatibility (endpoints, methods, schemas)
    - Does not validate runtime behavior or response handling
    - Does not detect deprecation warnings or soft failures
    - Updates module DOCUMENTATION notes only for compatible modules
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from _common_lib import get_repo_root, get_api_specs_dir, get_modules_dir
from _generation_lib import (
    extract_module_constants,
    normalize_path_for_comparison,
    resolve_schema_ref,
)

REPO_ROOT = get_repo_root()
MODULES_DIR = get_modules_dir()
SPECS_DIR = get_api_specs_dir()

DEFAULT_TARGET_VERSION = "8.0.2"

# Regex patterns for parsing module operations
_BUILD_PATH_CONST_PATTERN = r"build_path\(\s*([A-Z][A-Z0-9_]*)\b"
_POST_METHOD_PATTERN = r"def _{method}\(self, action\):.*?self\.client\.request\(\s*[\"']POST[\"']\s*,\s*([A-Z][A-Z0-9_]*)"


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
    """Strip query string from API path.

    Args:
        path: API path possibly with query string

    Returns:
        Path without query string

    Examples:
        >>> strip_query("/vcenter/vm?action=start")
        '/vcenter/vm'
        >>> strip_query("/vcenter/datacenter")
        '/vcenter/datacenter'
    """
    return path.split("?", 1)[0]


def normalize_path_template(path: str) -> str:
    """Normalize path for comparison: strip query, strip /api prefix, unify param placeholder names.

    Builds on normalize_path_for_comparison() from _generation_lib and additionally
    removes /api and /rest prefixes for validation-specific path matching.

    Args:
        path: API path to normalize

    Returns:
        Normalized path without query, parameters, or API prefixes

    Examples:
        >>> normalize_path_template("/api/vcenter/datacenter/{datacenter}?filter=foo")
        '/vcenter/datacenter'
        >>> normalize_path_template("/rest/vcenter/vm/{vm}")
        '/vcenter/vm'
    """
    # Use library function for base normalization (removes query and params)
    base = normalize_path_for_comparison(path)
    # Additionally strip /api and /rest prefixes for this validation use case
    if base.startswith("/api/"):
        base = base[4:]
    elif base.startswith("/rest/"):
        base = base[5:]
    return base


def _add_api_prefix_variants(base: str, variants: list[str]) -> None:
    """Add /api prefix variants to the list."""
    if not base.startswith("/api"):
        variants.append("/api" + base)
    else:
        variants.append(base[4:])


def _add_hyphenated_variants(base: str, variants: list[str]) -> None:
    """Add hyphenated suffix variants (e.g., resourcepool -> resource-pool)."""
    parts = base.rstrip("/").split("/")
    if len(parts) <= 1:
        return

    last = parts[-1]
    if "{" in last or "-" in last:
        return

    for suffix in ("pool", "policy", "profile", "filesystem"):
        if not (last.endswith(suffix) and len(last) > len(suffix)):
            continue
        hyphenated = last[: -len(suffix)] + "-" + suffix
        hyp_parts = parts[:-1] + [hyphenated]
        variants.append("/".join(hyp_parts))
        variants.append("/api" + "/".join(hyp_parts))


def _add_library_id_variants(base: str, variants: list[str]) -> None:
    """Add {library_id} variants for paths with {library} placeholder."""
    library_placeholder = "{library}"
    library_id_placeholder = "{library_id}"
    if "{library}" not in base:
        return
    variants.append(base.replace(library_placeholder, library_id_placeholder))
    variants.append("/api" + base.replace(library_placeholder, library_id_placeholder))


def path_variants(path: str) -> list[str]:
    """Generate all possible path variants for matching against spec.

    Generates variants to handle API inconsistencies:
    - With/without /api prefix
    - Hyphenated compound words (resourcepool → resource-pool)
    - Library parameter variants ({library} → {library_id})

    Args:
        path: API path to generate variants for

    Returns:
        List of unique path variants

    Examples:
        >>> path_variants("/vcenter/resourcepool")
        ['/vcenter/resourcepool', '/api/vcenter/resourcepool', '/vcenter/resource-pool', '/api/vcenter/resource-pool']
        >>> path_variants("/content/library/{library}")
        ['/content/library/{library}', '/api/content/library/{library}', '/content/library/{library_id}', '/api/content/library/{library_id}']
    """
    base = strip_query(path)
    variants = [base]
    _add_api_prefix_variants(base, variants)
    _add_hyphenated_variants(base, variants)
    _add_library_id_variants(base, variants)
    return list(dict.fromkeys(variants))


def action_path_candidates(path: str) -> list[str]:
    """Return path variants including /api prefix for action (query) endpoints."""
    candidates = [path]
    if not path.startswith("/api"):
        candidates.append("/api" + path)
    return list(dict.fromkeys(candidates))


def parse_query_dict(tail: str) -> dict[str, str]:
    query: dict[str, str] = {}
    query_match = re.search(r"query\s*=\s*\{([^}]*)\}", tail, re.DOTALL)
    if not query_match:
        return query
    for qm in re.finditer(r'"([^"]+)"\s*:\s*"([^"]+)"', query_match.group(1)):
        query[qm.group(1)] = qm.group(2)
    return query


def load_all_specs(version: str) -> tuple[dict, dict]:
    """Load and merge all API specs for a version.

    Loads all JSON files from content_generation/api_specs/<version>/ and merges
    their paths and schemas. This includes automation/vcenter.json,
    automation/appliance.json, vi-json/vi-json.json, and any other specs.

    Args:
        version: API version directory name (e.g., "9.1.0", "8.0.2")

    Returns:
        Tuple of (merged_paths, merged_spec_data):
        - merged_paths: All API paths from all spec files
        - merged_spec_data: Merged components/schemas and definitions

    Examples:
        >>> paths, spec = load_all_specs("9.1.0")
        >>> "/vcenter/datacenter" in paths
        True
        >>> "Datacenter" in spec["components"]["schemas"]
        True
        >>> "/appliance/networking" in paths  # From appliance.json
        True
    """
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
    """Find operations for a path in the spec using flexible matching.

    Uses a multi-strategy approach to find matching paths:
    1. Action endpoints: Match full path including ?action= query parameter
    2. Exact variants: Try all path variants (with/without /api, hyphenated, etc.)
    3. Normalized matching: Strip parameters and compare normalized paths

    Args:
        spec_paths: Dictionary of paths from OpenAPI spec (spec["paths"])
        path: Path from module to find in spec

    Returns:
        Tuple of (matched_spec_path, operations_dict) or (None, None) if not found

    Examples:
        >>> paths = {"/vcenter/datacenter": {"get": {...}, "post": {...}}}
        >>> find_path_ops(paths, "/api/vcenter/datacenter")
        ('/vcenter/datacenter', {'get': {...}, 'post': {...}})

        >>> paths = {"/vcenter/vm?action=start": {"post": {...}}}
        >>> find_path_ops(paths, "/api/vcenter/vm?action=start")
        ('/vcenter/vm?action=start', {'post': {...}})
    """
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


# Schema ref resolution now handled by _generation_lib.resolve_schema_ref
# Kept as wrapper for backward compatibility with existing code


def get_request_schema(spec_data: dict, operation: dict) -> dict:
    if "requestBody" in operation:
        content = operation["requestBody"].get("content", {})
        for media in content.values():
            schema = media.get("schema", {})
            if "$ref" in schema:
                return resolve_schema_ref(spec_data, schema["$ref"])
            return schema
    for param in operation.get("parameters", []):
        if param.get("in") == "body":
            schema = param.get("schema", {})
            if "$ref" in schema:
                return resolve_schema_ref(spec_data, schema["$ref"])
            return schema
    return {}


def schema_properties(schema: dict, spec_data: dict) -> dict:
    if not schema:
        return {}
    if "$ref" in schema:
        schema = resolve_schema_ref(spec_data, schema["$ref"])
    props = dict(schema.get("properties", {}))
    for key, value in list(props.items()):
        if "$ref" in value:
            props[key] = resolve_schema_ref(spec_data, value["$ref"])
    return props


def schema_required(schema: dict, spec_data: dict) -> set[str]:
    if not schema:
        return set()
    if "$ref" in schema:
        schema = resolve_schema_ref(spec_data, schema["$ref"])
    return set(schema.get("required", []))


def parse_llm_module(path: Path) -> dict | None:
    """Parse an LLM-generated module to extract metadata.

    Checks if a module was generated by LLM agents and extracts its
    source API version.

    Args:
        path: Path to the module file

    Returns:
        Dictionary with 'content' and 'source_version' if LLM-generated,
        None if not an LLM-generated module

    Examples:
        >>> meta = parse_llm_module(Path("plugins/modules/vcenter_datacenter.py"))
        >>> meta["source_version"]
        '9.1.0'
        >>> parse_llm_module(Path("plugins/modules/manual_module.py"))
        None
    """
    content = path.read_text(encoding="utf-8")
    if "This module is generated using LLM agents" not in content:
        return None
    gen_match = re.search(
        r"Generated from vSphere API spec (\d+\.\d+\.\d+)\.",
        content,
    )
    if not gen_match:
        return None
    return {
        "content": content,
        "source_version": gen_match.group(1),
    }


def extract_path_constants(content: str) -> dict[str, str]:
    """Extract PATH constants from module code.

    Finds all module-level constants containing "PATH" in the name and
    extracts their string values.

    Args:
        content: Module source code

    Returns:
        Dictionary mapping constant names to their path values

    Examples:
        >>> code = '''
        ... ITEM_PATH = "/vcenter/datacenter/{datacenter}"
        ... LIST_PATH = "/vcenter/datacenter"
        ... OTHER_VALUE = "not a path"
        ... '''
        >>> extract_path_constants(code)
        {'ITEM_PATH': '/vcenter/datacenter/{datacenter}', 'LIST_PATH': '/vcenter/datacenter'}
    """
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


def _extract_balanced_braces_block(content: str, start: int) -> str:
    """Extract block from start position to matching closing brace."""
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
    return content[start:end]


def _extract_body_fields(
    op_block: str, body_constants: dict[str, set[str]]
) -> set[str]:
    """Extract body fields from an operation block."""
    body_match = re.search(r"\"body\"\s*:\s*(\{[^}]*\}|_[A-Z_]+)", op_block)
    if not body_match:
        return set()

    body_ref = body_match.group(1).strip()
    if body_ref.startswith("{"):
        return {m.group(1) for m in re.finditer(r"\"([^\"]+)\"\s*:", body_ref)}
    if body_ref in body_constants:
        return body_constants[body_ref]
    return set()


def _extract_query_fields(op_block: str) -> dict[str, str]:
    """Extract query fields from an operation block."""
    query_fields: dict[str, str] = {}
    query_match = re.search(r"\"query\"\s*:\s*\{([^}]*)\}", op_block)
    if not query_match:
        return query_fields

    for qm in re.finditer(
        r"\"([^\"]+)\"\s*:\s*(?:\"([^\"]+)\"|([a-z_]+))",
        query_match.group(1),
    ):
        api_field = qm.group(1)
        literal = qm.group(2) or qm.group(3)
        query_fields[api_field] = literal
    return query_fields


def extract_payload_format(content: str) -> dict[str, dict]:
    payload_format: dict[str, dict] = {}
    pf_match = re.search(r"(?:_)?PAYLOAD_FORMAT\s*=\s*\{", content)
    if not pf_match:
        return payload_format

    start = pf_match.end() - 1
    block = _extract_balanced_braces_block(content, start)
    body_constants = extract_body_constants(content)

    for op_match in re.finditer(
        r"\"([a-z_]+)\"\s*:\s*\{(.*?)\n\s*\}",
        block,
        re.DOTALL,
    ):
        op_name = op_match.group(1)
        op_block = op_match.group(2)
        payload_format[op_name] = {
            "body_fields": _extract_body_fields(op_block, body_constants),
            "query_fields": _extract_query_fields(op_block),
        }

    return payload_format


def _get_method_for_operation(operation: str, content: str) -> str:
    """Determine HTTP method for a PayloadMap operation."""
    method_map = {
        "get": "get",
        "list": "get",
        "create": "post",
        "update": "patch",
        "delete": "delete",
    }
    if operation == "update":
        update_method_match = re.search(r'UPDATE_METHOD\s*=\s*"([^"]+)"', content)
        if update_method_match:
            return update_method_match.group(1).lower()
        return "patch"
    return method_map.get(operation, operation)


def _extract_payload_map_operations(
    content: str, path_constants: dict[str, str], add_fn
) -> None:
    """Extract operations from PayloadMap declarations."""
    for match in re.finditer(
        r'PayloadMap\(\s*operation\s*=\s*"([^"]+)"\s*,\s*uri\s*=\s*([A-Z][A-Z0-9_]*)',
        content,
    ):
        operation, path_const = match.groups()
        if path_const in path_constants:
            method = _get_method_for_operation(operation, content)
            add_fn(method, path_constants[path_const], operation)


def _extract_direct_client_calls(
    content: str, path_constants: dict[str, str], add_fn
) -> None:
    """Extract operations from direct self.client.METHOD(CONST) calls."""
    for match in re.finditer(
        r"self\.client\.(get|post|put|patch|delete)\(\s*([A-Z][A-Z0-9_]*)\b([^)]*)\)",
        content,
        re.DOTALL,
    ):
        method, const, tail = match.groups()
        if const in path_constants:
            add_fn(method, path_constants[const], None, parse_query_dict(tail))


def _extract_literal_path_calls(content: str, add_fn) -> None:
    """Extract operations from self.client.METHOD("literal") calls."""
    for match in re.finditer(
        r"self\.client\.(get|post|put|patch|delete)\(\s*[\"']([^\"']+)[\"']",
        content,
    ):
        method, literal = match.groups()
        add_fn(method, literal)


def _extract_request_calls(
    content: str, path_constants: dict[str, str], add_fn
) -> None:
    """Extract operations from self.client.request() calls."""
    for match in re.finditer(
        r"self\.client\.request\(\s*[\"'](GET|POST|PUT|PATCH|DELETE)[\"']\s*,\s*([A-Z][A-Z0-9_]*)\b([^)]*)\)",
        content,
        re.DOTALL,
    ):
        method, const, tail = match.groups()
        if const in path_constants:
            add_fn(method, path_constants[const], None, parse_query_dict(tail))


def _extract_fetch_list_calls(
    content: str, path_constants: dict[str, str], add_fn
) -> None:
    """Extract GET operations from fetch_list() calls."""
    for match in re.finditer(
        r"fetch_list\(\s*([A-Z][A-Z0-9_]*)\s*,\s*(?:self\.)?(?:_)?PAYLOAD_FORMAT\[\"([a-z_]+)\"\]",
        content,
    ):
        const, op = match.groups()
        if const in path_constants:
            add_fn("get", path_constants[const], op)

    for match in re.finditer(
        r"path\s*=\s*self\.build_path\(\s*([A-Z][A-Z0-9_]*)\b[^)]*\)\s*\n\s*return self\.fetch_list\(path",
        content,
    ):
        const = match.group(1)
        if const in path_constants:
            add_fn("get", path_constants[const])


def _extract_dynamic_path_calls(
    content: str,
    path_constants: dict[str, str],
    payload_format: dict[str, dict],
    add_fn,
) -> None:
    """Extract operations from self.client.METHOD(path) calls with dynamic paths."""
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
                query = _get_query_from_payload_format(payload_format, qm.group(1))
        const = _find_last_build_path_const(content, match.start(), path_constants)
        if const:
            add_fn(method, path_constants[const], None, query)


def _extract_build_payload_calls(
    content: str,
    path_constants: dict[str, str],
    payload_format: dict[str, dict],
    add_fn,
) -> None:
    """Extract operations from build_payload() followed by client calls."""
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
        query = _get_query_from_payload_format(payload_format, op)
        query.update(parse_query_dict(call_tail))
        if target in path_constants:
            add_fn(method, path_constants[target], op, query)
        elif target == "path":
            const = _find_last_build_path_const(
                content, match.end() + len(after), path_constants
            )
            if const:
                add_fn(method, path_constants[const], op, query)


def _extract_update_if_changed_calls(
    content: str, path_constants: dict[str, str], add_fn
) -> None:
    """Extract PATCH operations from update_if_changed() calls."""
    for match in re.finditer(
        r"update_if_changed\(\s*self\.build_path\(\s*([A-Z][A-Z0-9_]*)\b",
        content,
    ):
        const = match.group(1)
        if const in path_constants:
            add_fn("patch", path_constants[const], "update")

    for match in re.finditer(
        r"path\s*=\s*self\.build_path\(\s*([A-Z][A-Z0-9_]*)\b[^)]*\)[\s\S]{0,300}?update_if_changed\(\s*path",
        content,
    ):
        const = match.group(1)
        if const in path_constants:
            add_fn("patch", path_constants[const], "update")


def _extract_actions_dict(content: str, path_constants: dict[str, str], add_fn) -> None:
    """Extract POST operations from _ACTIONS dictionary."""
    if "_ACTIONS" not in content or "DIRECTORIES_PATH" not in path_constants:
        return
    block = re.search(r"_ACTIONS\s*=\s*\{([^}]+)\}", content, re.DOTALL)
    if not block:
        return
    base = strip_query(path_constants["DIRECTORIES_PATH"])
    for am in re.finditer(r'"([a-z_]+)"\s*:\s*"([^"]+)"', block.group(1)):
        add_fn("post", f"{base}?action={am.group(2)}")


def _find_post_method_path_const(content: str, method_name: str) -> str | None:
    """Find the path constant used in a _post_* helper method."""
    pattern = _POST_METHOD_PATTERN.replace("{method}", method_name)
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1) if match else None


def _get_query_from_payload_format(
    payload_format: dict[str, dict], op_name: str
) -> dict[str, str]:
    """Extract query fields from payload_format for a given operation."""
    return dict(payload_format.get(op_name, {}).get("query_fields", {}))


def _find_last_build_path_const(
    content: str, end_pos: int, path_constants: dict[str, str]
) -> str | None:
    """Find the last build_path() constant before end_pos that exists in path_constants."""
    bp_matches = re.findall(_BUILD_PATH_CONST_PATTERN, content[:end_pos])
    if bp_matches and bp_matches[-1] in path_constants:
        return bp_matches[-1]
    return None


def _extract_post_action_calls(
    content: str, path_constants: dict[str, str], add_fn
) -> None:
    """Extract operations from _post_action() helper method."""
    const = _find_post_method_path_const(content, "post_action")
    if not const or const not in path_constants:
        return
    for am in re.finditer(r'_post_action\("([^"]+)"\)', content):
        add_fn("post", path_constants[const], None, {"action": am.group(1)})


def _extract_post_resize_calls(
    content: str,
    path_constants: dict[str, str],
    payload_format: dict[str, dict],
    add_fn,
) -> None:
    """Extract operations from _post_resize() helper method."""
    const = _find_post_method_path_const(content, "post_resize")
    if not const or const not in path_constants:
        return
    for op_name in payload_format:
        action_val = "resize-ex" if op_name == "resize_ex" else op_name
        add_fn("post", path_constants[const], op_name, {"action": action_val})


def _extract_build_query_post_calls(
    content: str,
    path_constants: dict[str, str],
    payload_format: dict[str, dict],
    add_fn,
) -> None:
    """Extract POST operations from build_query() followed by client.post()."""
    for match in re.finditer(
        r'query\s*=\s*self\.build_query\(self\.PAYLOAD_FORMAT\["([a-z_]+)"\]\)'
        r"[\s\S]{0,400}?self\.client\.post\(\s*path",
        content,
    ):
        op = match.group(1)
        query = _get_query_from_payload_format(payload_format, op)
        const = _find_last_build_path_const(content, match.end(), path_constants)
        if const:
            add_fn("post", path_constants[const], op, query)


def extract_client_operations(
    content: str,
    path_constants: dict[str, str],
    payload_format: dict[str, dict],
) -> list[tuple[str, str, str | None, dict[str, str]]]:
    """Extract all API client operations from module code.

    Parses module source to find all self.client.* calls and PayloadMap
    declarations to understand what API operations the module performs.

    Uses multiple extraction strategies to handle different coding patterns:
    - PayloadMap operations (CRUD modules)
    - Direct client.METHOD() calls
    - Literal path strings
    - client.request() calls
    - fetch_list() calls
    - Dynamic path construction with build_path()
    - Action methods (_post_action, _post_resize)
    - _ACTIONS dictionary entries

    Args:
        content: Module source code
        path_constants: Dictionary of PATH constants and their values
        payload_format: Parsed PAYLOAD_FORMAT dictionary from module

    Returns:
        List of tuples: (method, path, operation_name, query_fields)
        - method: HTTP method (get, post, patch, delete)
        - path: API path (may include ?action= for action endpoints)
        - operation_name: Operation name from PAYLOAD_FORMAT (or None)
        - query_fields: Dictionary of query parameters

    Examples:
        >>> constants = {"LIST_PATH": "/vcenter/datacenter"}
        >>> payload = {"list": {"query_fields": {"filter.names": "names"}}}
        >>> ops = extract_client_operations(module_code, constants, payload)
        >>> ops[0]
        ('get', '/vcenter/datacenter', 'list', {'filter.names': 'names'})
    """
    operations: list[tuple[str, str, str | None, dict[str, str]]] = []

    def add(method: str, path: str, op: str | None = None, query: dict | None = None):
        query_fields = dict(query or {})
        if not query_fields and op and op in payload_format:
            query_fields = dict(payload_format[op].get("query_fields", {}))
        # Build action path inline
        if "?" not in path:
            action = query_fields.get("action")
            full_path = (
                f"{strip_query(path)}?action={action}" if action else strip_query(path)
            )
        else:
            full_path = path
        operations.append((method.lower(), full_path, op, query_fields))

    _extract_payload_map_operations(content, path_constants, add)
    _extract_direct_client_calls(content, path_constants, add)
    _extract_literal_path_calls(content, add)
    _extract_request_calls(content, path_constants, add)
    _extract_fetch_list_calls(content, path_constants, add)
    _extract_dynamic_path_calls(content, path_constants, payload_format, add)
    _extract_build_payload_calls(content, path_constants, payload_format, add)
    _extract_update_if_changed_calls(content, path_constants, add)
    _extract_actions_dict(content, path_constants, add)
    _extract_post_action_calls(content, path_constants, add)
    _extract_post_resize_calls(content, path_constants, payload_format, add)
    _extract_build_query_post_calls(content, path_constants, payload_format, add)

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


# --- Modern OperationConfig-based module parsing ---


def is_modern_module(content: str) -> bool:
    """Check if module uses modern OperationConfig format.

    Modern modules import and use OperationConfig objects to declare operations,
    while legacy modules use PAYLOAD_FORMAT dictionaries.

    Args:
        content: Module source code

    Returns:
        True if module uses OperationConfig, False otherwise

    Examples:
        >>> code = "from ...module_utils._operation_configs import OperationConfig"
        >>> is_modern_module(code)
        True
        >>> is_modern_module("PAYLOAD_FORMAT = {...}")
        False
    """
    return "OperationConfig" in content


def extract_endpoint_constants(content: str) -> dict[str, str]:
    """Extract LIST_ENDPOINT and ITEM_ENDPOINT constants from modern modules.

    Uses extract_module_constants() from _generation_lib to find endpoint constants
    that are used in OperationConfig objects.

    Args:
        content: Module source code

    Returns:
        Dictionary mapping constant names to their path values

    Examples:
        >>> code = '''
        ... LIST_ENDPOINT = "/vcenter/datacenter"
        ... ITEM_ENDPOINT = "/vcenter/datacenter/{datacenter}"
        ... '''
        >>> extract_endpoint_constants(code)
        {'LIST_ENDPOINT': '/vcenter/datacenter', 'ITEM_ENDPOINT': '/vcenter/datacenter/{datacenter}'}
    """
    patterns = {
        "LIST_ENDPOINT": r'LIST_ENDPOINT\s*=\s*"([^"]+)"',
        "ITEM_ENDPOINT": r'ITEM_ENDPOINT\s*=\s*"([^"]+)"',
    }
    return extract_module_constants(content, patterns)


def flatten_body_spec(body_spec: dict, prefix: str = "") -> set[str]:
    """Recursively extract all field names from nested body_spec.

    Handles nested subspec dictionaries by recursing into them and collecting
    all field names at all levels. Skips metadata keys like "required" and "subspec".

    Args:
        body_spec: Body specification dictionary from OperationConfig
        prefix: Internal parameter for tracking nesting (not used in current implementation)

    Returns:
        Set of all field names found at all nesting levels

    Examples:
        >>> spec = {
        ...     "name": {"required": True},
        ...     "backing": {
        ...         "required": False,
        ...         "subspec": {
        ...             "type": {"required": True},
        ...             "image_file": {"required": False}
        ...         }
        ...     }
        ... }
        >>> flatten_body_spec(spec)
        {'name', 'backing', 'type', 'image_file'}
    """
    fields = set()
    for key, value in body_spec.items():
        # Skip metadata keys
        if key in ("required", "subspec"):
            continue

        # Add the field name
        fields.add(key)

        # If this field has a subspec, recurse into it
        if isinstance(value, dict) and "subspec" in value:
            fields.update(flatten_body_spec(value["subspec"], prefix=f"{prefix}{key}."))

    return fields


def extract_query_fields(query_spec: dict | None) -> set[str]:
    """Extract query parameter names from query_spec.

    Args:
        query_spec: Query specification dictionary from OperationConfig

    Returns:
        Set of query parameter names

    Examples:
        >>> spec = {"names": {"required": False}, "datacenters": {"required": False}}
        >>> extract_query_fields(spec)
        {'names', 'datacenters'}
        >>> extract_query_fields(None)
        set()
    """
    return set(query_spec.keys()) if query_spec else set()


def parse_operation_config_object(config_block: str) -> dict:
    """Parse a single OperationConfig(...) constructor.

    Extracts uri, http_method, body_spec, and query_spec from an OperationConfig
    constructor call. Uses regex for string literals and balanced brace extraction
    for nested dictionaries.

    Args:
        config_block: String containing OperationConfig(...) constructor

    Returns:
        Dictionary with parsed values:
        - uri: API endpoint path (string)
        - http_method: HTTP method (string)
        - body_spec: Body specification dict (or empty dict if not present)
        - query_spec: Query specification dict (or empty dict if not present)

    Examples:
        >>> block = '''OperationConfig(
        ...     name="create",
        ...     uri=LIST_ENDPOINT,
        ...     http_method="POST",
        ...     body_spec={"name": {"required": True}},
        ... )'''
        >>> config = parse_operation_config_object(block)
        >>> config["http_method"]
        'POST'
    """
    result: dict = {
        "uri": "",
        "http_method": "",
        "body_spec": {},
        "query_spec": {},
    }

    # Extract uri (can be a constant reference or literal string)
    uri_match = re.search(r'uri\s*=\s*([A-Z_]+|"([^"]+)")', config_block)
    if uri_match:
        result["uri"] = uri_match.group(1)

    # Extract http_method (always a string literal)
    method_match = re.search(r'http_method\s*=\s*"([^"]+)"', config_block)
    if method_match:
        result["http_method"] = method_match.group(1)

    # Extract body_spec (dict literal)
    body_match = re.search(r"body_spec\s*=\s*\{", config_block)
    if body_match:
        spec_block = _extract_balanced_braces_block(config_block, body_match.end() - 1)
        try:
            # Use eval with restricted builtins to parse the dict literal
            result["body_spec"] = eval(spec_block, {"__builtins__": {}})
        except Exception:
            # If parsing fails, leave empty dict
            pass

    # Extract query_spec (dict literal)
    query_match = re.search(r"query_spec\s*=\s*\{", config_block)
    if query_match:
        spec_block = _extract_balanced_braces_block(config_block, query_match.end() - 1)
        try:
            result["query_spec"] = eval(spec_block, {"__builtins__": {}})
        except Exception:
            pass

    return result


def extract_operation_configs(content: str) -> list[dict]:
    """Find all OperationConfig declarations in module.

    Searches for:
    1. Standalone assignments: CREATE_OPERATION = OperationConfig(...)
    2. ACTION_OPERATIONS dictionary: {"connect": OperationConfig(...), ...}

    Args:
        content: Module source code

    Returns:
        List of parsed config dicts, each with uri, http_method, body_spec, query_spec

    Examples:
        >>> code = '''
        ... CREATE_OPERATION = OperationConfig(
        ...     name="create",
        ...     uri=LIST_ENDPOINT,
        ...     http_method="POST",
        ... )
        ... ACTION_OPERATIONS = {
        ...     "connect": OperationConfig(name="connect", uri="/path?action=connect", http_method="POST"),
        ... }
        ... '''
        >>> configs = extract_operation_configs(code)
        >>> len(configs)
        2
    """
    configs = []

    # Find standalone *_OPERATION = OperationConfig(...) assignments
    for match in re.finditer(
        r"([A-Z_]+_OPERATION)\s*=\s*OperationConfig\(",
        content,
    ):
        # Find the closing parenthesis for this OperationConfig call
        start = match.end()
        depth = 1
        end = start
        while end < len(content) and depth > 0:
            if content[end] == "(":
                depth += 1
            elif content[end] == ")":
                depth -= 1
            end += 1

        config_block = content[match.start() : end]
        configs.append(parse_operation_config_object(config_block))

    # Find ACTION_OPERATIONS = {...} dictionary
    action_match = re.search(r"ACTION_OPERATIONS\s*=\s*\{", content)
    if action_match:
        dict_block = _extract_balanced_braces_block(content, action_match.end() - 1)

        # Find all OperationConfig(...) calls within the dictionary
        for config_match in re.finditer(r"OperationConfig\(", dict_block):
            start = config_match.end()
            depth = 1
            end = start
            while end < len(dict_block) and depth > 0:
                if dict_block[end] == "(":
                    depth += 1
                elif dict_block[end] == ")":
                    depth -= 1
                end += 1

            config_block = dict_block[config_match.start() : end]
            configs.append(parse_operation_config_object(config_block))

    return configs


def operation_config_to_operation(
    config: dict,
    endpoint_constants: dict[str, str],
) -> Operation:
    """Convert parsed OperationConfig to Operation object.

    Resolves endpoint constant references (LIST_ENDPOINT, ITEM_ENDPOINT),
    flattens nested body_spec to field names, and extracts query parameters.

    Args:
        config: Parsed OperationConfig dictionary
        endpoint_constants: Dictionary mapping endpoint constant names to paths

    Returns:
        Operation object with method, path, body_fields, query_fields

    Examples:
        >>> config = {
        ...     "uri": "LIST_ENDPOINT",
        ...     "http_method": "POST",
        ...     "body_spec": {"name": {"required": True}},
        ...     "query_spec": {}
        ... }
        >>> endpoints = {"LIST_ENDPOINT": "/vcenter/datacenter"}
        >>> op = operation_config_to_operation(config, endpoints)
        >>> op.method
        'post'
        >>> op.path
        '/vcenter/datacenter'
    """
    # Resolve URI (may be a constant reference or literal path)
    uri = config.get("uri", "")
    if uri in endpoint_constants:
        path = endpoint_constants[uri]
    else:
        # Remove quotes if it's a literal string
        path = uri.strip('"')

    # Flatten body_spec to get all field names
    body_spec = config.get("body_spec", {})
    body_fields = flatten_body_spec(body_spec) if body_spec else set()

    # Extract query parameter names
    query_spec = config.get("query_spec")
    query_fields = extract_query_fields(query_spec)

    # Create Operation object
    return Operation(
        method=config.get("http_method", "").lower(),
        path=path,
        body_fields=body_fields,
        query_fields=query_fields,
    )


def extract_operations_unified(content: str) -> list[Operation]:
    """Extract API operations from module, auto-detecting format.

    Supports both modern OperationConfig-based modules and legacy PAYLOAD_FORMAT
    modules. Auto-detects the format and routes to the appropriate parser.

    Args:
        content: Module source code

    Returns:
        List of Operation objects extracted from the module

    Examples:
        >>> modern_code = '''
        ... LIST_ENDPOINT = "/vcenter/datacenter"
        ... CREATE_OPERATION = OperationConfig(
        ...     name="create",
        ...     uri=LIST_ENDPOINT,
        ...     http_method="POST",
        ...     body_spec={"name": {"required": True}},
        ... )
        ... '''
        >>> ops = extract_operations_unified(modern_code)
        >>> ops[0].method
        'post'

        >>> legacy_code = '''
        ... LIST_PATH = "/vcenter/datacenter"
        ... PAYLOAD_FORMAT = {"create": {"body": {...}}}
        ... self.client.post(LIST_PATH)
        ... '''
        >>> ops = extract_operations_unified(legacy_code)
        >>> len(ops) > 0
        True
    """
    if is_modern_module(content):
        # Modern format: Extract from OperationConfig objects
        endpoints = extract_endpoint_constants(content)
        configs = extract_operation_configs(content)

        operations = [
            operation_config_to_operation(config, endpoints) for config in configs
        ]

        return operations
    else:
        # Legacy format: Use existing extraction pipeline
        path_constants = extract_path_constants(content)
        payload_format = extract_payload_format(content)
        raw_ops = extract_client_operations(content, path_constants, payload_format)
        operations = dedupe_operations(raw_ops, payload_format)
        return operations


def compare_operation(
    op: Operation,
    target_paths: dict,
    target_spec_data: dict,
    target_version: str,
) -> list[BreakingChange]:
    """Compare a module operation against the target API spec.

    Checks for breaking changes that would prevent the module from working
    with the target API version:

    1. Missing endpoint: Path doesn't exist in target spec
    2. Missing method: Path exists but HTTP method not supported
    3. Required body field added: Target requires field module doesn't send
    4. Body field removed/renamed: Module sends field absent from target

    Args:
        op: Operation extracted from module
        target_paths: Paths dictionary from target OpenAPI spec
        target_spec_data: Full target OpenAPI spec data
        target_version: Target version string for error messages

    Returns:
        List of BreakingChange objects (empty if compatible)

    Examples:
        >>> op = Operation(method="patch", path="/vcenter/datacenter/{datacenter}",
        ...                body_fields={"name"}, query_fields=set())
        >>> issues = compare_operation(op, target_paths, target_spec, "8.0.2")
        >>> len(issues)
        0  # Compatible

        >>> op = Operation(method="post", path="/vcenter/new-feature",
        ...                body_fields=set(), query_fields=set())
        >>> issues = compare_operation(op, target_paths, target_spec, "8.0.2")
        >>> issues[0].category
        'Missing endpoint'
    """
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
        r"( {2}- Generated from vSphere API spec \d+\.\d+\.\d+\.\n)",
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
    if source_version.split(".", 1)[0] == target_version.split(".", 1)[0]:
        return {
            "module": module_name,
            "status": "skipped",
            "reason": f"generated from same major version ({source_version})",
        }

    if f"Has support for vSphere API {target_version}." in meta["content"]:
        return {
            "module": module_name,
            "status": "skipped",
            "reason": f"already documents support for {target_version}",
        }

    content = meta["content"]
    operations = extract_operations_unified(content)

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
    """Resolve a version string to an available API spec directory.

    Supports exact matches or major version resolution:
    - "9.1.0" → "9.1.0" (if exists)
    - "9" → "9.2.0" (latest 9.x version)
    - "8.0.2" → "8.0.2" (if exists)

    Args:
        requested: Version string (exact or major version)

    Returns:
        Exact version directory name

    Raises:
        ValueError: If no matching spec found

    Examples:
        >>> resolve_target_version("9.1.0")
        '9.1.0'
        >>> resolve_target_version("9")
        '9.2.0'  # Latest 9.x
        >>> resolve_target_version("999")
        ValueError: No spec for '999'. Available: 8.0.2, 9.1.0, 9.2.0
    """
    requested = re.sub(r"^\D*", "", requested.strip())
    if not requested:
        raise ValueError("target version is required")

    available = sorted(
        p.name for p in SPECS_DIR.iterdir() if p.is_dir() and re.match(r"^\d", p.name)
    )
    if requested in available:
        return requested

    major = requested.split(".", 1)[0]
    matches = [v for v in available if v.startswith(major + ".")]
    if matches:
        return matches[-1]

    raise ValueError(f"No spec for {requested!r}. Available: {', '.join(available)}")


def _parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
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
    return parser.parse_args()


def _get_llm_modules(module_names: list[str]) -> list[str]:
    """Get list of LLM-generated modules to validate."""
    if module_names:
        return sorted(module_names)
    return sorted(
        p.stem
        for p in MODULES_DIR.glob("*.py")
        if p.name != "__init__.py" and parse_llm_module(p) is not None
    )


def _categorize_results(
    results: list[dict],
) -> tuple[list[str], list[dict], list[dict], list[dict]]:
    """Categorize validation results by status."""
    compatible: list[str] = []
    incompatible: list[dict] = []
    skipped: list[dict] = []
    errors: list[dict] = []

    for result in results:
        status = result["status"]
        if status == "compatible":
            compatible.append(result["module"])
        elif status == "incompatible":
            incompatible.append(result)
        elif status == "skipped":
            skipped.append(result)
        else:
            errors.append(result)

    return compatible, incompatible, skipped, errors


def _print_summary(
    target_version: str,
    total: int,
    compatible: list[str],
    incompatible: list[dict],
    skipped: list[dict],
    errors: list[dict],
    dry_run: bool,
) -> None:
    """Print validation summary statistics."""
    print(f"# vSphere {target_version} compatibility validation")
    print(f"LLM-generated modules checked: {total}")
    print(f"Compatible: {len(compatible)}")
    print(f"Incompatible: {len(incompatible)}")
    print(f"Skipped: {len(skipped)}")
    print(f"Errors: {len(errors)}")
    if dry_run:
        print("Mode: dry-run (module notes not updated)")
    print()


def _print_compatible_modules(compatible: list[str]) -> None:
    """Print compatible modules section."""
    if not compatible:
        return
    print("## Compatible modules")
    for name in compatible:
        print(f"- {name}")
    print()


def _print_incompatible_modules(incompatible: list[dict]) -> None:
    """Print incompatible modules section."""
    if not incompatible:
        return
    print("## Incompatible modules")
    for result in incompatible:
        print(f"\n### {result['module']}")
        for method, path in result.get("operations", []):
            print(f"  - {method.upper()} {path}")
        for issue in result["issues"]:
            print(f"  - [{issue.category}] {issue.method} {issue.path}: {issue.detail}")


def _print_skipped_modules(skipped: list[dict]) -> None:
    """Print skipped modules section."""
    if not skipped:
        return
    print("\n## Skipped")
    for result in skipped:
        print(f"- {result['module']}: {result['reason']}")


def _print_errors(errors: list[dict]) -> None:
    """Print errors section."""
    if not errors:
        return
    print("\n## Errors")
    for result in errors:
        print(f"- {result['module']}: {result['reason']}")


def main() -> int:
    args = _parse_arguments()

    try:
        target_version = resolve_target_version(args.target)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    target_paths, target_spec_data = load_all_specs(target_version)
    llm_modules = _get_llm_modules(args.modules)

    results = [
        validate_module(
            name,
            target_paths,
            target_spec_data,
            target_version,
            update_notes=not args.dry_run,
        )
        for name in llm_modules
    ]

    compatible, incompatible, skipped, errors = _categorize_results(results)

    _print_summary(
        target_version,
        len(llm_modules),
        compatible,
        incompatible,
        skipped,
        errors,
        args.dry_run,
    )
    _print_compatible_modules(compatible)
    _print_incompatible_modules(incompatible)
    _print_skipped_modules(skipped)
    _print_errors(errors)

    return 1 if incompatible or errors else 0


if __name__ == "__main__":
    sys.exit(main())
