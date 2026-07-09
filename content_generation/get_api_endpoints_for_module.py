#!/usr/bin/env python
"""
Parse API endpoints and parameters for a vmware.vmware_rest module.

This script analyzes OpenAPI specifications to extract detailed parameter
information for all endpoints associated with a module. It produces structured
JSON output showing path parameters, query parameters, and body parameters
for each HTTP method on each endpoint.

Usage:
    # Parse a vcenter module
    python get_api_endpoints_for_module.py vcenter_resourcepool

    # Parse an appliance module
    python get_api_endpoints_for_module.py appliance_networking

    # Use a different API spec version
    python get_api_endpoints_for_module.py vcenter_resourcepool --spec-version 8.0.2

    # Pretty-print the output
    python get_api_endpoints_for_module.py vcenter_resourcepool --format pretty

Output Format:
    {
      "/api/path": {
        "method": {
          "path": ["param1", "param2"],
          "query": {
            "param_name": {
              "required": bool,
              "description": [array of strings],
              "schema": {...}
            }
          },
          "body": {
            "param_name": {
              "type": "string",
              "description": [array],
              "required": bool,
              "properties": {...}
            }
          }
        }
      }
    }

Format Rules Applied:
    - Descriptions split on double newlines into separate array items
    - Backticks (`) replaced with single quotes (')
    - "(MOID)" added after "identifier" for resource identifiers
    - Enum values mapped to "choices" field
    - Schema references followed recursively
    - All properties captured for nested objects
"""

import argparse
import json
import re
import sys
from typing import Any, Dict, List

from _common_lib import APPLICATION_JSON, get_spec_path
from _generation_lib import (
    find_matching_paths,
    get_path_operations,
    extract_path_params,
    resolve_schema_ref,
    module_name_to_api_path,
)


def get_spec_file_for_module(module_name: str) -> str:
    """Determine which spec file to use based on module prefix.

    Args:
        module_name: Module name (e.g., vcenter_resourcepool, appliance_networking)

    Returns:
        Spec filename (vcenter.json, appliance.json, or content.json)
    """
    if module_name.startswith("appliance_"):
        return "appliance.json"
    elif module_name.startswith("content_"):
        return "content.json"
    else:
        return "vcenter.json"


def load_api_spec(spec_version: str, spec_file: str) -> Dict[str, Any]:
    """Load OpenAPI specification from file.

    Args:
        spec_version: API version (e.g., "9.1.0")
        spec_file: Spec filename (e.g., "vcenter.json")

    Returns:
        Parsed OpenAPI spec dictionary

    Raises:
        FileNotFoundError: If spec file doesn't exist
    """
    # Use shared utility to get spec path
    spec_path = get_spec_path(spec_version, spec_file)

    if not spec_path.exists():
        raise FileNotFoundError(
            f"API spec not found: {spec_path}\n"
            f"Please ensure the spec file exists for version {spec_version}"
        )

    with open(spec_path, "r") as f:
        return json.load(f)


def clean_description_text(description: str) -> List[str]:
    """Clean and format API description text.

    Applies format rules:
    - Split on double newlines (\\n\\n) into separate array items
    - Replace backticks with single quotes
    - Add (MOID) after "identifier" when referencing resources
    - Remove excessive whitespace

    Args:
        description: Raw API description text

    Returns:
        List of cleaned description strings
    """
    if not description:
        return ["No description available."]

    # Replace backticks with single quotes
    description = description.replace("`", "'")

    # Add (MOID) after "identifier" for resource references
    # Pattern: "identifier for the resource type"
    description = re.sub(
        r"\bidentifier\b(?=\s+for\s+the\s+resource\s+type)",
        "identifier (MOID)",
        description,
        flags=re.IGNORECASE,
    )

    # Also handle: "identifiers for the resource type" (plural)
    description = re.sub(
        r"\bidentifiers\b(?=\s+for\s+the\s+resource\s+type)",
        "identifiers (MOIDs)",
        description,
        flags=re.IGNORECASE,
    )

    # Split on double newlines to create separate description items
    # This preserves paragraph structure
    parts = re.split(r"\n\n+", description)

    # Clean each part
    cleaned = []
    for part in parts:
        # First, split on list item patterns: newline followed by optional whitespace and dash
        # This handles bullet points like "\n  - item" or "\n- item"
        # Also handle parts that start with whitespace and dash (after \n\n split)
        list_items = re.split(r"\n\s*-\s+", part)

        for item in list_items:
            # Remove single newlines within the item and join
            item = " ".join(item.split())
            item = item.strip()

            # Remove leading dash and whitespace if present (for items that started a paragraph with dash)
            item = re.sub(r"^-\s+", "", item)

            if not item:
                continue

            # Capitalize the first character
            item = item[0].upper() + item[1:] if len(item) > 1 else item.upper()

            if item == "Possible values:":
                continue

            # Fix ENUM descriptions
            item = re.sub(r"'(\w+)': (.*)", "\\1 - \\2", item)

            # Remove any remaining colons, since they break YAML
            item = item.replace(": ", " ")

            cleaned.append(item)

    return cleaned if cleaned else ["No description available."]


def _handle_schema_ref(
    schema: Dict[str, Any], spec: Dict[str, Any], depth: int
) -> Dict[str, Any]:
    """Handle $ref in schema.

    Args:
        schema: Schema with $ref
        spec: Full OpenAPI spec
        depth: Current recursion depth

    Returns:
        Formatted schema dict
    """
    resolved = resolve_schema_ref(spec, schema["$ref"])
    if not resolved:
        return {"type": "string"}

    if "enum" in resolved:
        return {"type": resolved.get("type", "string"), "choices": resolved["enum"]}

    return format_schema_info(resolved, spec, depth + 1)


def _merge_allof_schemas(
    schema: Dict[str, Any], spec: Dict[str, Any]
) -> Dict[str, Any]:
    """Merge all schemas in allOf.

    Args:
        schema: Schema with allOf
        spec: Full OpenAPI spec

    Returns:
        Merged schema dict
    """
    merged = {}
    for sub_schema in schema["allOf"]:
        if "$ref" in sub_schema:
            resolved = resolve_schema_ref(spec, sub_schema["$ref"])
            if resolved:
                merged.update(resolved)
        else:
            merged.update(sub_schema)
    return merged


def _format_array_schema(
    schema_type: str,
    schema: Dict[str, Any],
    spec: Dict[str, Any],
    depth: int,
    result: Dict[str, Any],
) -> None:
    """Format array type schema.

    Args:
        schema_type: Schema type
        schema: Schema definition
        spec: Full OpenAPI spec
        depth: Current recursion depth
        result: Result dict to modify in place
    """
    if schema_type == "array" and "items" in schema:
        result["items"] = format_schema_info(schema["items"], spec, depth + 1)


def _extract_enum_from_description(desc_text: str, spec: Dict[str, Any]) -> List[Any]:
    """Extract enum choices from description reference.

    Args:
        desc_text: Description text
        spec: Full OpenAPI spec

    Returns:
        List of enum choices or empty list
    """
    enum_match = re.search(r"For more information see: \*([^*]+)\*", desc_text)
    if not enum_match:
        return []

    enum_schema_name = enum_match.group(1)
    enum_schema = resolve_schema_ref(spec, f"#/components/schemas/{enum_schema_name}")

    if enum_schema and "enum" in enum_schema:
        return enum_schema["enum"]

    return []


def _format_property_info(
    prop_name: str,
    prop_schema: Dict[str, Any],
    required_fields: List[str],
    spec: Dict[str, Any],
    depth: int,
) -> Dict[str, Any]:
    """Format a single property's information.

    Args:
        prop_name: Property name
        prop_schema: Property schema
        required_fields: List of required field names
        spec: Full OpenAPI spec
        depth: Current recursion depth

    Returns:
        Formatted property info dict
    """
    prop_info = format_schema_info(prop_schema, spec, depth + 1)
    prop_info["required"] = prop_name in required_fields

    if "description" in prop_schema:
        prop_info["description"] = clean_description_text(prop_schema["description"])

        # Extract enum from description reference if not already present
        if "choices" not in prop_info:
            enum_choices = _extract_enum_from_description(
                prop_schema["description"], spec
            )
            if enum_choices:
                prop_info["choices"] = enum_choices

    return prop_info


def _format_object_properties(
    schema: Dict[str, Any], spec: Dict[str, Any], depth: int, result: Dict[str, Any]
) -> None:
    """Format object type properties.

    Args:
        schema: Schema definition
        spec: Full OpenAPI spec
        depth: Current recursion depth
        result: Result dict to modify in place
    """
    if "properties" not in schema:
        return

    result["properties"] = {}
    required_fields = schema.get("required", [])

    for prop_name, prop_schema in schema["properties"].items():
        result["properties"][prop_name] = _format_property_info(
            prop_name, prop_schema, required_fields, spec, depth
        )


def _format_object_schema(
    schema_type: str,
    schema: Dict[str, Any],
    spec: Dict[str, Any],
    depth: int,
    result: Dict[str, Any],
) -> None:
    """Format object type schema.

    Args:
        schema_type: Schema type
        schema: Schema definition
        spec: Full OpenAPI spec
        depth: Current recursion depth
        result: Result dict to modify in place
    """
    if schema_type == "object" or "properties" in schema:
        result["type"] = "object"
        _format_object_properties(schema, spec, depth, result)


def format_schema_info(
    schema: Dict[str, Any], spec: Dict[str, Any], depth: int = 0
) -> Dict[str, Any]:
    """Format schema information into output structure.

    Args:
        schema: Schema definition (can be inline or resolved from $ref)
        spec: Full OpenAPI spec for resolving references
        depth: Current recursion depth (prevents infinite loops)

    Returns:
        Formatted schema dict with type, items, properties, etc.
    """
    if depth > 5:
        return {"type": "object"}

    # Handle $ref
    if "$ref" in schema:
        return _handle_schema_ref(schema, spec, depth)

    # Handle allOf
    if "allOf" in schema:
        merged = _merge_allof_schemas(schema, spec)
        return format_schema_info(merged, spec, depth + 1)

    # Get basic type
    schema_type = schema.get("type", "string")
    result = {"type": schema_type}

    # Handle enum/choices
    if "enum" in schema:
        result["choices"] = schema["enum"]

    # Handle array type
    _format_array_schema(schema_type, schema, spec, depth, result)

    # Handle object type
    _format_object_schema(schema_type, schema, spec, depth, result)

    return result


def extract_query_parameters(
    operation: Dict[str, Any], spec: Dict[str, Any]
) -> Dict[str, Any]:
    """Extract query parameters from an operation.

    Args:
        operation: OpenAPI operation object (get, post, etc.)
        spec: Full OpenAPI spec for resolving references

    Returns:
        Dictionary of query parameter definitions
    """
    query_params = {}

    for param in operation.get("parameters", []):
        if param.get("in") != "query":
            continue

        param_name = param["name"]
        param_info = {
            "required": param.get("required", False),
            "description": clean_description_text(param.get("description", "")),
        }

        # Extract schema information and merge it directly into param_info
        # This flattens the structure so "schema.type" becomes just "type"
        if "schema" in param:
            schema_info = format_schema_info(param["schema"], spec)
            # Merge schema fields directly into param_info
            param_info.update(schema_info)

        query_params[param_name] = param_info

    return query_params


def _resolve_schema_reference(
    schema: Dict[str, Any], spec: Dict[str, Any]
) -> Dict[str, Any]:
    """Resolve schema reference if present.

    Args:
        schema: Schema that may contain $ref
        spec: Full OpenAPI spec

    Returns:
        Resolved schema or original schema
    """
    if "$ref" in schema:
        resolved = resolve_schema_ref(spec, schema["$ref"])
        return resolved if resolved else {}
    return schema


def _get_param_description(prop_schema: Dict[str, Any], prop_name: str) -> List[str]:
    """Get or generate description for a parameter.

    Args:
        prop_schema: Property schema
        prop_name: Property name

    Returns:
        List of description strings
    """
    if "description" in prop_schema:
        return clean_description_text(prop_schema["description"])
    return [f"Parameter {prop_name}"]


def _extract_body_params_from_schema(
    schema: Dict[str, Any], spec: Dict[str, Any]
) -> Dict[str, Any]:
    """Extract body parameters from a resolved schema.

    Args:
        schema: Resolved schema with properties
        spec: Full OpenAPI spec

    Returns:
        Dictionary of body parameter definitions
    """
    if not schema:
        return {}

    body_params = {}
    properties = schema.get("properties", {})
    required_fields = schema.get("required", [])

    for prop_name, prop_schema in properties.items():
        prop_info = format_schema_info(prop_schema, spec)
        prop_info["required"] = prop_name in required_fields
        prop_info["description"] = _get_param_description(prop_schema, prop_name)
        body_params[prop_name] = prop_info

    return body_params


def _extract_openapi3_body_params(
    operation: Dict[str, Any], spec: Dict[str, Any]
) -> Dict[str, Any]:
    """Extract body parameters from OpenAPI 3.0 requestBody.

    Args:
        operation: OpenAPI operation object
        spec: Full OpenAPI spec

    Returns:
        Dictionary of body parameter definitions or empty dict
    """
    if "requestBody" not in operation:
        return {}

    request_body = operation["requestBody"]
    content = request_body.get("content", {})

    if APPLICATION_JSON not in content:
        return {}

    schema = content[APPLICATION_JSON].get("schema", {})
    schema = _resolve_schema_reference(schema, spec)

    return _extract_body_params_from_schema(schema, spec)


def _extract_openapi2_body_params(
    operation: Dict[str, Any], spec: Dict[str, Any]
) -> Dict[str, Any]:
    """Extract body parameters from OpenAPI 2.0 parameters with in: body.

    Args:
        operation: OpenAPI operation object
        spec: Full OpenAPI spec

    Returns:
        Dictionary of body parameter definitions or empty dict
    """
    for param in operation.get("parameters", []):
        if param.get("in") == "body":
            schema = param.get("schema", {})
            schema = _resolve_schema_reference(schema, spec)
            return _extract_body_params_from_schema(schema, spec)

    return {}


def extract_body_parameters(
    operation: Dict[str, Any], spec: Dict[str, Any], method: str
) -> Dict[str, Any]:
    """Extract body parameters from request schema.

    Args:
        operation: OpenAPI operation object
        spec: Full OpenAPI spec for resolving references
        method: HTTP method (for determining if body expected)

    Returns:
        Dictionary of body parameter definitions
    """
    if method.upper() not in ["POST", "PATCH", "PUT"]:
        return {}

    # Try OpenAPI 3.0 style first
    body_params = _extract_openapi3_body_params(operation, spec)
    if body_params:
        return body_params

    # Fall back to OpenAPI 2.0 style
    return _extract_openapi2_body_params(operation, spec)


def _find_module_paths(module_name: str, spec: Dict[str, Any]) -> List[str]:
    """Find all API paths matching the module name.

    Args:
        module_name: Module name
        spec: OpenAPI specification dictionary

    Returns:
        List of matching paths
    """
    api_path = module_name_to_api_path(module_name)
    all_paths = list(spec.get("paths", {}).keys())
    matching_paths = find_matching_paths(all_paths, api_path)

    if not matching_paths:
        print(
            f"Warning: No API paths found for module '{module_name}' (searched: {api_path})",
            file=sys.stderr,
        )

    return matching_paths


def _should_include_method(is_info_module: bool, method: str) -> bool:
    """Check if method should be included for this module type.

    Args:
        is_info_module: True if this is an info module
        method: HTTP method name

    Returns:
        True if method should be included
    """
    if is_info_module:
        return method.upper() == "GET"
    return True


def _extract_method_parameters(
    path: str, operation: Dict[str, Any], spec: Dict[str, Any], method: str
) -> Dict[str, Any]:
    """Extract all parameters for a single method.

    Args:
        path: API path
        operation: Operation definition
        spec: Full OpenAPI spec
        method: HTTP method name

    Returns:
        Dictionary of method parameters
    """
    method_info = {}

    # Extract path parameters
    path_params = extract_path_params(path)
    if path_params:
        method_info["path"] = path_params

    # Extract query parameters
    query_params = extract_query_parameters(operation, spec)
    if query_params:
        method_info["query"] = query_params

    # Extract body parameters
    body_params = extract_body_parameters(operation, spec, method)
    if body_params:
        method_info["body"] = body_params

    return method_info


def _process_path_operations(
    path: str, spec: Dict[str, Any], is_info_module: bool
) -> Dict[str, Any]:
    """Process all operations for a single path.

    Args:
        path: API path
        spec: Full OpenAPI spec
        is_info_module: True if this is an info module

    Returns:
        Dictionary of method info for this path
    """
    path_info = {}
    operations = get_path_operations(spec, path)

    for method, operation in operations.items():
        if not _should_include_method(is_info_module, method):
            continue

        method_info = _extract_method_parameters(path, operation, spec, method)

        # Only add method if it has parameters or is an operation on this path
        if method_info or method:
            path_info[method.lower()] = method_info

    return path_info


def parse_module_endpoints(module_name: str, spec: Dict[str, Any]) -> Dict[str, Any]:
    """Parse all endpoints for a module.

    Args:
        module_name: Module name (e.g., vcenter_resourcepool)
        spec: OpenAPI specification dictionary

    Returns:
        Dictionary mapping paths to methods to parameter information
    """
    result = {}
    is_info_module = module_name.endswith(("_info", "_query"))
    matching_paths = _find_module_paths(module_name, spec)

    # Process each matching path
    for path in sorted(matching_paths):
        path_info = _process_path_operations(path, spec, is_info_module)

        # Only add path if it has operations
        if path_info:
            result[path] = path_info

    return result


def format_short_output(result: Dict[str, Any]) -> str:
    """Format output in short form showing only endpoints and methods.

    Args:
        result: Parsed endpoint data

    Returns:
        Formatted string showing endpoints and their supported methods
    """
    lines = []
    for path in sorted(result.keys()):
        lines.append(f"{path}:")
        methods = sorted(result[path].keys())
        for method in methods:
            lines.append(f"  - {method}")
    return "\n".join(lines)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Parse API endpoints and parameters for a vmware.vmware_rest module",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse vcenter_resourcepool module
  python get_api_endpoints_for_module.py vcenter_resourcepool

  # Parse appliance_networking module with pretty output
  python get_api_endpoints_for_module.py appliance_networking --format pretty

  # Show just endpoints and methods
  python get_api_endpoints_for_module.py vcenter_resourcepool --format short

  # Use a specific API version
  python get_api_endpoints_for_module.py vcenter_datacenter --spec-version 8.0.2
        """,
    )

    parser.add_argument(
        "module", help="Module name (e.g., vcenter_resourcepool, appliance_networking)"
    )
    parser.add_argument(
        "--spec-version",
        default="9.1.0",
        help="OpenAPI spec version to use (default: 9.1.0)",
    )
    parser.add_argument(
        "--format",
        default="json",
        choices=["json", "pretty", "short"],
        help="Output format (default: json)",
    )

    args = parser.parse_args()

    try:
        # Determine which spec file to use
        spec_file = get_spec_file_for_module(args.module)

        # Load the spec
        spec = load_api_spec(args.spec_version, spec_file)

        # Parse endpoints
        result = parse_module_endpoints(args.module, spec)

        # Output results
        if args.format == "short":
            print(format_short_output(result))
        elif args.format == "pretty":
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps(result))

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing module '{args.module}': {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
