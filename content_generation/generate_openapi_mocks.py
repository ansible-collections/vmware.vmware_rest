#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate OpenAPI mock specifications for integration tests.

This script generates properly formatted OpenAPI 3.0.3 mock specs that work
with MockServer for integration testing of vmware.vmware_rest modules.

The script works with the new OperationConfig-based module format that uses:
- MOID_PARAMETER_HINTS instead of MOID_ATTRIBUTE_NAME
- LIST_ENDPOINT/ITEM_ENDPOINT instead of LIST_PATH/ITEM_PATH
- OperationConfig objects instead of PAYLOAD_MAP constants

Usage:
    # Generate mocks for a CRUD module pair
    python generate_openapi_mocks.py vcenter_datacenter [output_dir]

    # Generate mocks for an info-only module
    python generate_openapi_mocks.py vcenter_vm_tools_installer_info [output_dir]

    # Generate mocks for nested path modules
    python generate_openapi_mocks.py vcenter_vm_hardware_floppy [output_dir]

If output_dir is not specified, mocks are generated in:
    tests/integration/targets/<module_base_name>/openapi_spec_mocks/

Generated Files:
    - default.json: Empty state (no resources exist)
    - created.json: One resource exists
    - list_multiple.json: Multiple resources exist
    - updated.json: Resource exists (same as created.json by default)

Note on updated.json:
    The script generates updated.json with the same values as created.json
    since it cannot know what fields your test will update. If your test
    updates specific fields and checks for those updated values, you must
    manually edit updated.json to reflect those changes.

    Example: If your test updates cpu_allocation, edit updated.json to
    have the expected cpu_allocation values after the update.
"""

import json
import sys
import re
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional

from _common_lib import APPLICATION_JSON, get_repo_root


def create_base_spec(
    title: str, version: str = "9.1.0.0"  # NOSONAR(S1313)
) -> Dict[str, Any]:
    """Create base OpenAPI 3.0.3 spec structure."""
    return {
        "openapi": "3.0.3",
        "info": {"title": title, "version": version},
        "servers": [
            {
                "url": "https://{host}/api",
                "variables": {"host": {"default": "localhost"}},
            }
        ],
        "paths": {},
        "components": {"schemas": {}},
    }


def _ensure_path_exists(spec: Dict[str, Any], path: str) -> None:
    """Ensure a path exists in the spec."""
    if path not in spec["paths"]:
        spec["paths"][path] = {}


def _create_response(description: str, example: Any = None) -> Dict[str, Any]:
    """Create a response definition."""
    response = {"description": description}
    if example is not None:
        response["content"] = {
            APPLICATION_JSON: {
                "schema": {"type": "object"},
                "example": example,
            }
        }
    return response


def add_list_operation(
    spec: Dict[str, Any], path: str, operation_id: str, example: List[Dict[str, Any]]
) -> None:
    """Add a GET list operation to the spec."""
    _ensure_path_exists(spec, path)

    spec["paths"][path]["get"] = {
        "operationId": operation_id,
        "parameters": [],
        "responses": {"200": _create_response("ok", example)},
    }


def add_create_operation(
    spec: Dict[str, Any], path: str, operation_id: str, example: str
) -> None:
    """Add a POST create operation to the spec."""
    _ensure_path_exists(spec, path)

    spec["paths"][path]["post"] = {
        "operationId": operation_id,
        "parameters": [],
        "responses": {"200": _create_response("ok", example)},
    }


def _create_path_parameter(param_name: str) -> Dict[str, Any]:
    """Create a path parameter definition."""
    return {
        "name": param_name,
        "in": "path",
        "required": True,
        "schema": {"type": "string"},
    }


def add_get_operation(
    spec: Dict[str, Any],
    path: str,
    operation_id: str,
    param_name: Optional[str],
    example: Dict[str, Any],
    include_404: bool = True,
) -> None:
    """Add a GET item operation to the spec."""
    _ensure_path_exists(spec, path)

    responses = {"200": _create_response("ok", example)}
    if include_404:
        responses["404"] = _create_response("not found")

    operation = {
        "operationId": operation_id,
        "parameters": [_create_path_parameter(param_name)] if param_name else [],
        "responses": responses,
    }

    spec["paths"][path]["get"] = operation


def add_update_operation(
    spec: Dict[str, Any], path: str, operation_id: str, param_name: str
) -> None:
    """Add a PATCH update operation to the spec."""
    _ensure_path_exists(spec, path)

    spec["paths"][path]["patch"] = {
        "operationId": operation_id,
        "parameters": [_create_path_parameter(param_name)],
        "responses": {"204": _create_response("ok")},
    }


def add_delete_operation(
    spec: Dict[str, Any], path: str, operation_id: str, param_name: str
) -> None:
    """Add a DELETE operation to the spec."""
    _ensure_path_exists(spec, path)

    spec["paths"][path]["delete"] = {
        "operationId": operation_id,
        "parameters": [_create_path_parameter(param_name)],
        "responses": {"204": _create_response("ok")},
    }


def parse_return_block(content: str) -> Dict[str, Any]:
    """
    Parse the RETURN documentation block to extract return value structure.

    Returns a dict with sample data for 'value' and plural keys.
    """
    return_data = {}

    return_match = re.search(r'RETURN\s*=\s*r"""(.*?)"""', content, re.DOTALL)
    if not return_match:
        return return_data

    return_block = return_match.group(1)

    # Parse value field sample
    value_sample = _extract_value_sample(return_block)
    if value_sample:
        return_data["value_sample"] = value_sample

    # Parse plural field sample
    plural_data = _extract_plural_sample(return_block)
    if plural_data:
        return_data.update(plural_data)

    return return_data


def _extract_value_sample(return_block: str) -> Optional[Dict[str, Any]]:
    """Extract the 'value' field sample from RETURN block using YAML."""
    # Look for 'value:' followed by 'sample:' and capture the indented content
    value_match = re.search(
        r"value:.*?sample:\s*\n((?: {4,}.*\n)+)", return_block, re.DOTALL
    )
    if not value_match:
        return None

    sample_text = value_match.group(1)
    try:
        return yaml.safe_load(sample_text)
    except yaml.YAMLError:
        return None


def _extract_plural_sample(return_block: str) -> Optional[Dict[str, Any]]:
    """Extract plural field sample (e.g., 'datacenters') from RETURN block using YAML."""
    plural_match = re.search(
        r"(\w+s):.*?sample:\s*\n(.+)(?:\n\w+:|$)", return_block, re.DOTALL
    )
    if not plural_match:
        return None

    plural_key = plural_match.group(1)
    sample_text = plural_match.group(2)

    try:
        parsed_data = yaml.safe_load(sample_text)
        if isinstance(parsed_data, list) and parsed_data:
            return {"plural_key": plural_key, "list_sample": parsed_data[0]}
    except yaml.YAMLError:
        pass

    return None


# Build operation IDs based on vSphere naming convention
# Format: Vcenter.ResourceName_operation (PascalCase with no underscores or hyphens)
# For nested paths like /vcenter/vm/{vm}/hardware/floppy -> Vcenter.Vm.Hardware.Floppy
# For appliance paths like /appliance/monitoring/query -> Appliance.Monitoring.Query
# Examples from API spec: Vcenter.ResourcePool, Vcenter.Datacenter, Appliance.Monitoring
def to_pascal_case(s: str) -> str:
    """Convert hyphen/underscore-separated string to PascalCase."""
    return "".join(word.capitalize() for word in s.replace("-", "_").split("_"))


def get_moid_name_from_hints(content):
    # Extract MOID parameter hints (optional for action-style modules)
    moid_hints_match = re.search(
        r"MOID_PARAMETER_HINTS\s*=\s*\[(.*?)\]", content, re.DOTALL
    )
    moid_name = None
    if moid_hints_match:
        hints_str = moid_hints_match.group(1).strip()
        if hints_str:  # Only process if not empty
            moid_hints = [
                h.strip().strip("\"'") for h in hints_str.split(",") if h.strip()
            ]
            # The last hint that's not 'vm', 'host', etc. is typically the main MOID
            # For single-item modules, there's only one hint
            moid_name = moid_hints[-1] if moid_hints else None

    return moid_name


def parse_module_file(module_path: Path) -> Dict[str, Any]:
    """Parse a module file to extract API operation details."""
    content = module_path.read_text()

    moid_name = get_moid_name_from_hints(content)

    # Extract endpoint constants
    list_endpoint_match = re.search(r'LIST_ENDPOINT\s*=\s*"([^"]+)"', content)
    item_endpoint_match = re.search(r'ITEM_ENDPOINT\s*=\s*"([^"]+)"', content)

    list_path = list_endpoint_match.group(1) if list_endpoint_match else None
    item_path = item_endpoint_match.group(1) if item_endpoint_match else None

    if not list_path and not item_path:
        raise ValueError(
            f"Could not parse LIST_ENDPOINT or ITEM_ENDPOINT from {module_path}"
        )

    # Determine the primary path to use for extracting resource name
    primary_path = item_path if item_path else list_path

    # Extract resource name from path
    # For /vcenter/datacenter -> datacenter
    # For /vcenter/vm/{vm}/hardware/floppy -> floppy
    # For /vcenter/resource-pool -> resource_pool (convert hyphens)
    # For /appliance/monitoring/query -> query
    path_parts = [p for p in primary_path.split("/") if p and not p.startswith("{")]
    resource_name = path_parts[-1].replace("-", "_")

    # Determine the API namespace (vcenter, appliance, etc.)
    api_namespace = to_pascal_case(path_parts[0]) if path_parts else "Vcenter"

    if len(path_parts) > 2:  # Nested resource
        resource_title = ".".join([to_pascal_case(p) for p in path_parts[1:]])
    else:
        resource_title = to_pascal_case(path_parts[-1])

    operation_prefix = f"{api_namespace}.{resource_title}"

    # Determine what operations are supported by checking for OperationConfig definitions
    has_list = "LIST_OPERATION" in content and list_path is not None
    has_get = "GET_OPERATION" in content
    has_create = "CREATE_OPERATION" in content
    has_update = "UPDATE_OPERATION" in content
    has_delete = "DELETE_OPERATION" in content

    # Parse RETURN block to get sample data
    return_samples = parse_return_block(content)

    return {
        "moid_name": moid_name,
        "resource_name": resource_name,
        "list_path": list_path,
        "item_path": item_path,
        "operation_prefix": operation_prefix,
        "has_create": has_create,
        "has_update": has_update,
        "has_delete": has_delete,
        "has_get": has_get,
        "has_list": has_list,
        "return_samples": return_samples,
    }


def _build_resource_examples(
    module_info: Dict[str, Any], resource_examples: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Build or normalize resource example data."""
    if resource_examples:
        return resource_examples

    resource_name = module_info["resource_name"]
    moid_name = module_info.get("moid_name")
    return_samples = module_info.get("return_samples", {})

    # For modules without MOID (action-style modules), use simpler examples
    if not moid_name:
        # Use value_sample if available, otherwise provide a minimal example
        get_result = return_samples.get("value_sample")
        if not get_result:
            # Provide a generic structure hint
            get_result = {"result": "data"}
        return {
            "moid": None,
            "name": resource_name,
            "list_item": {},
            "get_result": get_result,
        }

    # Try to get MOID from list_sample first, otherwise generate one
    list_item_sample = return_samples.get("list_sample", {})
    if list_item_sample and moid_name in list_item_sample:
        moid_value = list_item_sample[moid_name]
    else:
        moid_value = f"{resource_name}-1001"

    get_result = return_samples.get("value_sample", {"name": f"my_{resource_name}"})

    if not list_item_sample:
        list_item_sample = {moid_name: moid_value, "name": f"my_{resource_name}"}
    # Don't override the moid_name in list_item_sample if it already exists

    return {
        "moid": moid_value,
        "name": f"my_{resource_name}",
        "list_item": list_item_sample,
        "get_result": get_result,
    }


def _add_common_operations(
    spec: Dict[str, Any],
    module_info: Dict[str, Any],
    resource_examples: Dict[str, Any],
    list_data: Optional[List[Dict[str, Any]]] = None,
) -> None:
    """Add common CRUD operations to a spec."""
    moid_name = module_info.get("moid_name")
    list_path = module_info["list_path"]
    item_path = module_info["item_path"]
    op_prefix = module_info["operation_prefix"]

    if module_info["has_list"] and list_data is not None:
        add_list_operation(spec, list_path, f"{op_prefix}_list", list_data)

    if module_info["has_create"]:
        add_create_operation(
            spec, list_path, f"{op_prefix}_create", resource_examples["moid"]
        )

    if module_info["has_get"] and item_path:
        add_get_operation(
            spec,
            item_path,
            f"{op_prefix}_get",
            moid_name,
            resource_examples["get_result"],
        )

    if module_info["has_delete"] and item_path:
        add_delete_operation(spec, item_path, f"{op_prefix}_delete", moid_name)

    if module_info["has_update"] and item_path:
        add_update_operation(spec, item_path, f"{op_prefix}_update", moid_name)


def _generate_default_mock(
    module_info: Dict[str, Any],
    resource_examples: Dict[str, Any],
    output_dir: Path,
) -> None:
    """Generate default.json - empty list, operations available."""
    resource_name = module_info["resource_name"]
    spec = create_base_spec(f"vCenter {resource_name.title()} Mock")
    _add_common_operations(spec, module_info, resource_examples, list_data=[])

    with open(output_dir / "default.json", "w") as f:
        json.dump(spec, f, indent=2)


def _generate_created_mock(
    module_info: Dict[str, Any],
    resource_examples: Dict[str, Any],
    output_dir: Path,
) -> None:
    """Generate created.json - one item exists."""
    if not module_info["has_create"]:
        return

    resource_name = module_info["resource_name"]
    spec = create_base_spec(f"vCenter {resource_name.title()} Mock")
    list_data = [resource_examples["list_item"]] if module_info["has_list"] else None
    _add_common_operations(spec, module_info, resource_examples, list_data)

    with open(output_dir / "created.json", "w") as f:
        json.dump(spec, f, indent=2)


def _generate_list_multiple_mock(
    module_info: Dict[str, Any],
    resource_examples: Dict[str, Any],
    output_dir: Path,
) -> None:
    """Generate list_multiple.json - multiple items exist."""
    if not module_info["has_list"]:
        return

    resource_name = module_info["resource_name"]
    moid_name = module_info.get("moid_name")
    list_path = module_info["list_path"]
    item_path = module_info["item_path"]
    op_prefix = module_info["operation_prefix"]

    # Skip if no MOID (can't generate multiple items without unique IDs)
    if not moid_name:
        return

    # Generate second MOID by incrementing the number in the first MOID
    first_moid = resource_examples["moid"]
    # Try to increment the last number in the MOID (e.g., resgroup-1009 -> resgroup-1010)
    import re as moid_re

    match = moid_re.search(r"(\d+)$", first_moid)
    if match:
        num = int(match.group(1))
        second_moid = first_moid[: match.start()] + str(num + 1)
    else:
        second_moid = f"{resource_name}-1002"

    second_item = resource_examples["list_item"].copy()
    second_item[moid_name] = second_moid
    second_item["name"] = f"another-{resource_name.replace('_', '-')}"

    spec = create_base_spec(f"vCenter {resource_name.title()} Mock")
    add_list_operation(
        spec,
        list_path,
        f"{op_prefix}_list",
        [resource_examples["list_item"], second_item],
    )

    if module_info["has_get"] and item_path:
        add_get_operation(
            spec,
            item_path,
            f"{op_prefix}_get",
            moid_name,
            resource_examples["get_result"],
        )

    with open(output_dir / "list_multiple.json", "w") as f:
        json.dump(spec, f, indent=2)


def _generate_updated_mock(
    module_info: Dict[str, Any],
    resource_examples: Dict[str, Any],
    output_dir: Path,
) -> None:
    """
    Generate updated.json - item exists and has been updated.

    Note: This mock uses the same values as created.json since we don't know
    what fields the test will update. Tests should verify that the values
    they send match what they expect, not rely on the mock returning specific
    updated values. For test-specific updated values, manually edit this file.
    """
    if not module_info["has_update"]:
        return

    resource_name = module_info["resource_name"]
    moid_name = module_info.get("moid_name")
    list_path = module_info["list_path"]
    item_path = module_info["item_path"]
    op_prefix = module_info["operation_prefix"]

    spec = create_base_spec(f"vCenter {resource_name.title()} Mock")

    # Use the same values as created.json - tests can customize this file
    # if they need specific updated values
    if module_info["has_list"]:
        add_list_operation(
            spec, list_path, f"{op_prefix}_list", [resource_examples["list_item"]]
        )

    if module_info["has_get"] and item_path:
        add_get_operation(
            spec,
            item_path,
            f"{op_prefix}_get",
            moid_name,
            resource_examples["get_result"],
        )

    add_update_operation(spec, item_path, f"{op_prefix}_update", moid_name)

    with open(output_dir / "updated.json", "w") as f:
        json.dump(spec, f, indent=2)


def generate_generic_mocks(
    module_info: Dict[str, Any],
    output_dir: Path,
    resource_examples: Optional[Dict[str, Any]] = None,
) -> None:
    """Generate mock specs for any module based on its operations."""
    output_dir.mkdir(parents=True, exist_ok=True)

    resource_examples = _build_resource_examples(module_info, resource_examples)

    _generate_default_mock(module_info, resource_examples, output_dir)
    _generate_created_mock(module_info, resource_examples, output_dir)
    _generate_list_multiple_mock(module_info, resource_examples, output_dir)
    _generate_updated_mock(module_info, resource_examples, output_dir)

    print(f"Generated {module_info['resource_name']} mock specs in {output_dir}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: generate_openapi_mocks.py <module_name> [output_dir]")
        print("Example: generate_openapi_mocks.py vcenter_datacenter")
        sys.exit(1)

    module_name = sys.argv[1]
    repo_root = get_repo_root()

    # Determine output directory
    if len(sys.argv) > 2:
        output_dir = Path(sys.argv[2])
    else:
        # Default to tests/integration/targets/<module_name>/openapi_spec_mocks
        # Strip _info suffix if present for the target directory
        target_name = module_name.replace("_info", "")
        output_dir = (
            repo_root / f"tests/integration/targets/{target_name}/openapi_spec_mocks"
        )

    # Find the module file
    module_file = repo_root / f"plugins/modules/{module_name}.py"
    if not module_file.exists():
        print(f"Error: Module file not found: {module_file}")
        sys.exit(1)

    # Parse module to understand its operations
    try:
        module_info = parse_module_file(module_file)
    except Exception as e:
        print(f"Error parsing module: {e}")
        sys.exit(1)

    # If this is a CRUD module and an _info module exists, also parse that
    # for better return sample data
    if not module_name.endswith("_info"):
        info_module_file = repo_root / f"plugins/modules/{module_name}_info.py"
        if info_module_file.exists():
            try:
                info_module_info = parse_module_file(info_module_file)
                # Merge return samples from info module (they're usually better)
                if info_module_info.get("return_samples"):
                    module_info["return_samples"] = info_module_info["return_samples"]
            except Exception:
                # If info module parsing fails, just continue with what we have
                pass

    # Generate mocks using parsed return samples
    # resource_examples can still be passed to override if needed
    generate_generic_mocks(module_info, output_dir)


if __name__ == "__main__":
    main()
