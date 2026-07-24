#!/usr/bin/env python
"""
Generate formatted YAML module specification from module name.

This script automatically calls get_api_endpoints_for_module.py to get endpoint data,
then creates a structured YAML dictionary containing:
  - list_endpoint: The collection endpoint (if exists)
  - item_endpoint: The individual resource endpoint (if exists)
  - action_endpoints: Named action endpoints (if any)
  - options: Ansible module options with proper formatting

Usage:
    # Generate from module name
    python format_api_endpoints_for_module_generation.py vcenter_vm_hardware_floppy

    # Specify output file
    python format_api_endpoints_for_module_generation.py vcenter_vm_hardware_floppy -o output.yaml

    # Use different API version
    python format_api_endpoints_for_module_generation.py vcenter_vm_hardware_floppy --spec-version 8.0.2
"""

import argparse
import re
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

# Import from common libraries
from _common_lib import camel_to_snake
from _generation_lib import extract_path_params

# Import from sibling scripts
from get_api_endpoints_for_module import (
    load_api_spec,
    get_spec_file_for_module,
    parse_module_endpoints,
)


# Custom YAML dumper that preserves order and formats nicely
class OrderedDumper(yaml.SafeDumper):
    """Custom YAML dumper with better formatting."""

    pass


def represent_ordereddict(dumper, data):
    """Represent OrderedDict as a YAML mapping."""
    return dumper.represent_mapping("tag:yaml.org,2002:map", data.items())


def represent_none(dumper, data):
    """Represent None as null in YAML."""
    return dumper.represent_scalar("tag:yaml.org,2002:null", "")


OrderedDumper.add_representer(OrderedDict, represent_ordereddict)
OrderedDumper.add_representer(type(None), represent_none)


def classify_endpoint(uri: str) -> Tuple[str, Optional[str]]:
    """Classify an endpoint as list, item, or action.

    Args:
        uri: API endpoint URI

    Returns:
        Tuple of (endpoint_type, action_name) where:
        - endpoint_type: "list", "item", or "action"
        - action_name: Name of action (for action endpoints) or None
    """
    # Check for action endpoint: ?action=<action_name>
    action_match = re.search(r"\?action=([^&]+)", uri)
    if action_match:
        action_name = action_match.group(1)
        # Skip 'change' actions per rule 7
        if action_name == "change":
            return None, None
        return "action", action_name

    # Check if URI ends with a path parameter (item endpoint)
    # Pattern: ends with /{param}
    if re.search(r"/\{[^}]+\}$", uri):
        return "item", None

    # Otherwise it's a list endpoint
    return "list", None


def _format_params_dict(params: Dict[str, Any]) -> OrderedDict:
    """Convert parameters to ordered dict with required flags."""
    result = OrderedDict()
    for param_name, param_info in params.items():
        result[param_name] = param_info.get("required", False)
    return result


def format_endpoint_operations(
    operations: Dict[str, Any], endpoint_type: str
) -> OrderedDict:
    """Format operations section for an endpoint.

    Args:
        operations: Dictionary of method -> parameters
        endpoint_type: "list", "item", or "action"

    Returns:
        OrderedDict of formatted operations
    """
    ops = OrderedDict()
    method_order = ["get", "post", "patch", "put", "delete"]

    for method in method_order:
        if method not in operations:
            continue

        method_data = operations[method]
        op_dict = OrderedDict()

        # Add body parameters if present
        if "body" in method_data:
            op_dict["body"] = _format_params_dict(method_data["body"])

        # Add query parameters if present
        if "query" in method_data:
            op_dict["query"] = _format_params_dict(method_data["query"])

        # Use empty dict if no parameters
        ops[method] = op_dict if op_dict else {}

    return ops


def _extract_params_from_operations(operations: Dict[str, Any]) -> List[str]:
    """Extract path parameters from operation method data.

    Args:
        operations: Dictionary of method -> method_data

    Returns:
        List of parameter names from operation path data
    """
    params = []
    for method, method_data in operations.items():
        if "path" in method_data:
            for param in method_data["path"]:
                if param not in params:
                    params.append(param)
    return params


def _extract_params_from_endpoint(uri: str, operations: Dict[str, Any]) -> set:
    """Extract all path parameters from a single endpoint.

    Args:
        uri: Endpoint URI
        operations: Operations for this endpoint

    Returns:
        Set of parameter names
    """
    # Extract from URI using shared utility
    params = extract_path_params(uri)

    # Add from operations
    operation_params = _extract_params_from_operations(operations)
    for param in operation_params:
        if param not in params:
            params.append(param)

    return set(params)


def _build_ordered_param_list(params_per_endpoint: List[set]) -> List[str]:
    """Build ordered list of unique parameters preserving order of appearance.

    Args:
        params_per_endpoint: List of parameter sets, one per endpoint

    Returns:
        Ordered list of unique parameter names
    """
    seen = set()
    all_params = []
    for param_set in params_per_endpoint:
        for param in param_set:
            if param not in seen:
                seen.add(param)
                all_params.append(param)
    return all_params


def extract_path_parameters(
    endpoints_data: Dict[str, Any],
) -> Tuple[List[str], List[str]]:
    """Extract all path parameters across all endpoints.

    Path parameters that appear in ALL endpoints are required module parameters.
    Path parameters that appear in SOME endpoints are optional module parameters.

    Args:
        endpoints_data: Dictionary of endpoint URI -> operations

    Returns:
        Tuple of (all_path_params, required_path_params) where:
        - all_path_params: List of all path parameter names
        - required_path_params: List of path parameters that appear in ALL endpoints
    """
    # Collect parameters for each endpoint
    params_per_endpoint = [
        _extract_params_from_endpoint(uri, operations)
        for uri, operations in endpoints_data.items()
    ]

    # Find parameters that appear in ALL endpoints (required)
    required_params_set = (
        set.intersection(*params_per_endpoint) if params_per_endpoint else set()
    )

    # Build ordered list of all unique parameters
    all_path_params = _build_ordered_param_list(params_per_endpoint)

    # Filter to get required parameters in same order
    required_path_params = [p for p in all_path_params if p in required_params_set]

    return all_path_params, required_path_params


def _merge_param_type(merged: Dict[str, Any], params: Dict[str, Any]) -> None:
    """Merge parameters of a specific type (body or query) into the merged dict.

    Args:
        merged: Dictionary to merge into (modified in place)
        params: Parameters to merge
    """
    for param_name, param_info in params.items():
        if param_name not in merged:
            merged[param_name] = param_info.copy()
            merged[param_name]["required"] = False


def _process_method_data(merged: Dict[str, Any], method_data: Dict[str, Any]) -> None:
    """Process a single method's data and merge its parameters.

    Args:
        merged: Dictionary to merge into (modified in place)
        method_data: Method data containing body and/or query parameters
    """
    if "body" in method_data:
        _merge_param_type(merged, method_data["body"])

    if "query" in method_data:
        _merge_param_type(merged, method_data["query"])


def merge_parameters(all_operations: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Merge and deduplicate parameters from all operations.

    For top-level module parameters, we need to consider that a parameter is
    only truly required if it's needed for ALL state operations. Since different
    operations (POST/PATCH/DELETE) may need different parameters, and the module
    uses a single 'state' parameter to determine which operation to perform, we
    mark parameters as NOT required to allow flexibility across all states.

    The actual validation of which parameters are needed for which state happens
    at runtime in the module logic based on the 'state' parameter.

    Args:
        all_operations: Dictionary of all endpoint operations

    Returns:
        Merged parameter dictionary with all parameters marked as not required
    """
    merged = {}

    for uri, operations in all_operations.items():
        for method, method_data in operations.items():
            _process_method_data(merged, method_data)

    return merged


def python_type_name(schema_type: str) -> str:
    """Convert JSON schema type to Python type name.

    Args:
        schema_type: JSON schema type (string, boolean, object, array, integer, number)

    Returns:
        Python type name (str, bool, dict, list, int, float)
    """
    type_map = {
        "string": "str",
        "boolean": "bool",
        "object": "dict",
        "array": "list",
        "integer": "int",
        "number": "float",
    }
    return type_map.get(schema_type, "str")


def _generate_path_param_description(param_name: str) -> List[str]:
    """Generate description for a path parameter (resource identifier).

    Args:
        param_name: Parameter name in snake_case

    Returns:
        List of description lines
    """
    resource_name_text = param_name.replace("_", " ")
    resource_name_class = param_name.replace("_", " ").title().replace(" ", "")
    return [
        f"Identifier of the {resource_name_text} to manage.",
        f"Must be an identifier (MOID) for a C({resource_name_class}) resource.",
    ]


def _generate_description(
    param_name: str, param_info: Dict[str, Any], all_path_params: List[str]
) -> List[str]:
    """Generate description for a parameter.

    Args:
        param_name: Parameter name
        param_info: Parameter information
        all_path_params: List of all path parameters

    Returns:
        List of description lines
    """
    description = param_info.get("description", [])
    if description:
        return description

    if param_name in all_path_params:
        return _generate_path_param_description(param_name)

    return [f"Parameter {param_name}."]


def _build_suboptions_from_properties(
    properties: Dict[str, Any], module_name: str
) -> OrderedDict:
    """Build suboptions from properties dictionary.

    Args:
        properties: Dictionary of property name -> property info
        module_name: Name of the module

    Returns:
        OrderedDict of formatted suboptions
    """
    suboptions = OrderedDict()
    for prop_name, prop_info in properties.items():
        suboptions[prop_name] = format_parameter_option(
            prop_name, prop_info, [], [], module_name
        )
    return suboptions


def _add_object_suboptions(
    option: OrderedDict, param_info: Dict[str, Any], module_name: str
) -> None:
    """Add suboptions for object/dict type parameters.

    Args:
        option: Option dictionary to modify in place
        param_info: Parameter information
        module_name: Name of the module
    """
    if "properties" in param_info:
        option["suboptions"] = _build_suboptions_from_properties(
            param_info["properties"], module_name
        )


def _add_array_elements(
    option: OrderedDict, param_info: Dict[str, Any], module_name: str
) -> None:
    """Add elements and suboptions for array type parameters.

    Args:
        option: Option dictionary to modify in place
        param_info: Parameter information
        module_name: Name of the module
    """
    if "items" not in param_info:
        return

    items_info = param_info["items"]
    items_type = items_info.get("type", "string")
    option["elements"] = python_type_name(items_type)

    # Add suboptions for arrays of objects
    if items_type == "object" and "properties" in items_info:
        option["suboptions"] = _build_suboptions_from_properties(
            items_info["properties"], module_name
        )


def format_parameter_option(
    param_name: str,
    param_info: Dict[str, Any],
    all_path_params: List[str],
    required_path_params: List[str],
    module_name: str,
) -> OrderedDict:
    """Format a single parameter as an Ansible module option.

    Args:
        param_name: Parameter name (in snake_case if converted)
        param_info: Parameter information from API spec
        all_path_params: List of all path parameters
        required_path_params: List of path parameters that appear in ALL endpoints (required)
        module_name: Name of the module (for generating descriptions)

    Returns:
        OrderedDict of formatted option
    """
    option = OrderedDict()

    # Add description
    option["description"] = _generate_description(
        param_name, param_info, all_path_params
    )

    # Add type
    param_type = param_info.get("type", "string")
    option["type"] = python_type_name(param_type)

    # Add required field
    is_required = param_name in required_path_params or param_info.get(
        "required", False
    )
    option["required"] = is_required

    # Add choices if present
    if "choices" in param_info:
        option["choices"] = param_info["choices"]

    # Add type-specific options
    if param_type == "object":
        _add_object_suboptions(option, param_info, module_name)
    elif param_type == "array":
        _add_array_elements(option, param_info, module_name)

    return option


def create_state_parameter(
    has_list_post: bool, has_item_delete: bool, action_names: List[str]
) -> OrderedDict:
    """Create the state parameter based on available operations.

    Args:
        has_list_post: Whether list endpoint has POST operation
        has_item_delete: Whether item endpoint has DELETE operation
        action_names: List of action endpoint names

    Returns:
        OrderedDict for state parameter
    """
    option = OrderedDict()

    # Build description
    description = ["The desired state of the resource."]

    # Collect all state choices
    choices = []
    if has_list_post:
        choices.append("present")
        description.append("Use C(present) to create or update the resource.")

    if has_item_delete:
        choices.append("absent")
        description.append("Use C(absent) to delete the resource.")

    # Add action states
    for action in action_names:
        choices.append(action)
        description.append(f"Use C({action}) to perform the {action} action.")

    # Add idempotence note if there are non-CRUD states
    if action_names:
        description.append("Only options C(present) and C(absent) support idempotence.")

    option["description"] = description
    option["type"] = "str"
    option["choices"] = choices

    # Set default or required
    if "present" in choices:
        option["default"] = "present"
    else:
        option["required"] = True

    return option


def replace_camel_case_params_in_uri(uri: str, param_mappings: Dict[str, str]) -> str:
    """Replace camelCase parameters in URI with snake_case versions.

    Args:
        uri: URI string containing path parameters in {param} format
        param_mappings: Dictionary mapping camelCase param names to snake_case

    Returns:
        URI with parameters replaced
    """
    result = uri
    for camel_param, snake_param in param_mappings.items():
        result = result.replace(f"{{{camel_param}}}", f"{{{snake_param}}}")
    return result


def _build_path_parameter_mappings(endpoints_data: Dict[str, Any]) -> OrderedDict:
    """Build mappings from camelCase to snake_case for path parameters.

    Args:
        endpoints_data: Dictionary of endpoint URI -> operations

    Returns:
        OrderedDict mapping camelCase param names to snake_case
    """
    mappings = OrderedDict()
    for uri, operations in endpoints_data.items():
        params = re.findall(r"\{([^}]+)\}", uri)
        for param in params:
            if any(c.isupper() for c in param):
                mappings[param] = camel_to_snake(param)
    return mappings


def _classify_and_collect_endpoints(
    endpoints_data: Dict[str, Any], path_parameter_mappings: OrderedDict
) -> Tuple[List[Dict[str, Any]], OrderedDict]:
    """Classify endpoints into non-action and action endpoints.

    Args:
        endpoints_data: Dictionary of endpoint URI -> operations
        path_parameter_mappings: Mappings from camelCase to snake_case

    Returns:
        Tuple of (non_action_endpoints, action_endpoints)
    """
    non_action_endpoints = []
    action_endpoints = OrderedDict()

    for uri, operations in endpoints_data.items():
        endpoint_type, action_name = classify_endpoint(uri)

        if endpoint_type is None:
            continue

        updated_uri = replace_camel_case_params_in_uri(uri, path_parameter_mappings)

        if endpoint_type in ("list", "item"):
            non_action_endpoints.append(
                {"uri": updated_uri, "operations": operations, "type": endpoint_type}
            )
        elif endpoint_type == "action":
            action_endpoints[action_name] = {
                "uri": updated_uri,
                "operations": operations,
            }

    return non_action_endpoints, action_endpoints


def _create_endpoint_dict(uri: str, operations: Dict[str, Any]) -> Dict[str, Any]:
    """Create an endpoint dictionary with uri and operations.

    Args:
        uri: Endpoint URI
        operations: Operations for this endpoint

    Returns:
        Dictionary with uri and operations keys
    """
    return {"uri": uri, "operations": operations}


def _assign_endpoints_by_count(
    non_action_endpoints: List[Dict[str, Any]],
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Assign list and item endpoints based on singleton resource logic.

    Args:
        non_action_endpoints: List of non-action endpoint data

    Returns:
        Tuple of (list_endpoint, item_endpoint)
    """
    list_endpoint = None
    item_endpoint = None

    if len(non_action_endpoints) == 1:
        # Singleton resource: single endpoint is always ITEM
        endpoint = non_action_endpoints[0]
        item_endpoint = _create_endpoint_dict(endpoint["uri"], endpoint["operations"])
    elif len(non_action_endpoints) >= 2:
        if len(non_action_endpoints) > 2:
            print(
                f"Warning: Found {len(non_action_endpoints)} non-action endpoints. "
                "Expected 1 (singleton) or 2 (LIST + ITEM). Using classify_endpoint logic.",
                file=sys.stderr,
            )

        # Use classify_endpoint logic for 2+ endpoints
        for endpoint_data in non_action_endpoints:
            endpoint_dict = _create_endpoint_dict(
                endpoint_data["uri"], endpoint_data["operations"]
            )
            if endpoint_data["type"] == "list":
                list_endpoint = endpoint_dict
            elif endpoint_data["type"] == "item":
                item_endpoint = endpoint_dict

    return list_endpoint, item_endpoint


def _should_omit_list_get_query(
    module_name: str,
    list_endpoint: Optional[Dict[str, Any]],
    item_endpoint: Optional[Dict[str, Any]],
) -> bool:
    """Determine if list GET query parameters should be omitted.

    Args:
        module_name: Name of the module
        list_endpoint: List endpoint data
        item_endpoint: Item endpoint data

    Returns:
        True if list GET query params should be omitted
    """
    is_info_module = module_name.endswith(("_info", "_query"))
    has_list_get = list_endpoint and "get" in list_endpoint["operations"]
    has_item_get = item_endpoint and "get" in item_endpoint["operations"]
    return not is_info_module and has_list_get and has_item_get


def _format_endpoint_spec(
    endpoint: Optional[Dict[str, Any]],
    endpoint_type: str,
) -> OrderedDict:
    """Format a single endpoint specification.

    Args:
        endpoint: Endpoint data with uri and operations
        endpoint_type: Type of endpoint ("list", "item", or "action")

    Returns:
        OrderedDict with uri and operations, or empty dict if endpoint is None
    """
    if not endpoint:
        return OrderedDict()

    return OrderedDict(
        [
            ("uri", endpoint["uri"]),
            (
                "operations",
                format_endpoint_operations(
                    endpoint["operations"],
                    endpoint_type,
                ),
            ),
        ]
    )


def _format_action_endpoints(action_endpoints: OrderedDict) -> OrderedDict:
    """Format all action endpoints.

    Args:
        action_endpoints: Dictionary of action_name -> action data

    Returns:
        OrderedDict of formatted action endpoints
    """
    if not action_endpoints:
        return OrderedDict()

    formatted_actions = OrderedDict()
    for action_name, action_data in action_endpoints.items():
        formatted_actions[action_name] = _format_endpoint_spec(action_data, "action")
    return formatted_actions


def _convert_params_to_snake_case(
    all_path_params: List[str], required_path_params: List[str]
) -> Tuple[List[str], List[str]]:
    """Convert path parameters to snake_case.

    Args:
        all_path_params: All path parameters (may be camelCase)
        required_path_params: Required path parameters (may be camelCase)

    Returns:
        Tuple of (snake_case_all_params, snake_case_required_params)
    """
    snake_case_all = []
    snake_case_required = []

    for param in all_path_params:
        snake_param = (
            camel_to_snake(param) if any(c.isupper() for c in param) else param
        )
        snake_case_all.append(snake_param)
        if param in required_path_params:
            snake_case_required.append(snake_param)

    return snake_case_all, snake_case_required


def _find_param_in_merged(
    snake_param: str, all_path_params: List[str], merged_params: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Find a snake_case parameter in merged_params by checking original camelCase names.

    Args:
        snake_param: Parameter name in snake_case
        all_path_params: List of all original path parameters (may be camelCase)
        merged_params: Merged parameter dictionary

    Returns:
        Parameter info if found, None otherwise
    """
    for original_param in all_path_params:
        if (
            camel_to_snake(original_param) == snake_param
            and original_param in merged_params
        ):
            return merged_params[original_param]
    return None


def _add_path_parameter_option(
    options: OrderedDict,
    param_name: str,
    all_path_params: List[str],
    merged_params: Dict[str, Any],
    snake_case_all_path_params: List[str],
    snake_case_required_path_params: List[str],
    module_name: str,
) -> None:
    """Add a single path parameter option to the options dictionary.

    Args:
        options: Options dictionary to modify in place
        param_name: Parameter name in snake_case
        all_path_params: All original path parameters
        merged_params: Merged parameter dictionary
        snake_case_all_path_params: All path params in snake_case
        snake_case_required_path_params: Required path params in snake_case
        module_name: Name of the module
    """
    param_info = _find_param_in_merged(param_name, all_path_params, merged_params)
    if param_info is None:
        param_info = {"type": "string"}

    options[param_name] = format_parameter_option(
        param_name,
        param_info,
        snake_case_all_path_params,
        snake_case_required_path_params,
        module_name,
    )


def _add_path_parameters_to_options(
    options: OrderedDict,
    snake_case_all_path_params: List[str],
    all_path_params: List[str],
    merged_params: Dict[str, Any],
    snake_case_required_path_params: List[str],
    module_name: str,
) -> None:
    """Add all path parameters to options (item param first, then parents).

    Args:
        options: Options dictionary to modify in place
        snake_case_all_path_params: All path params in snake_case
        all_path_params: All original path parameters
        merged_params: Merged parameter dictionary
        snake_case_required_path_params: Required path params in snake_case
        module_name: Name of the module
    """
    if not snake_case_all_path_params:
        return

    # Item param is last, parents are all others
    item_param = snake_case_all_path_params[-1]
    parent_params = (
        snake_case_all_path_params[:-1] if len(snake_case_all_path_params) > 1 else []
    )

    # Add item parameter
    _add_path_parameter_option(
        options,
        item_param,
        all_path_params,
        merged_params,
        snake_case_all_path_params,
        snake_case_required_path_params,
        module_name,
    )

    # Add parent parameters
    for parent_param in parent_params:
        _add_path_parameter_option(
            options,
            parent_param,
            all_path_params,
            merged_params,
            snake_case_all_path_params,
            snake_case_required_path_params,
            module_name,
        )


def _get_excluded_params(
    exclude_list_get_from_options: bool, list_endpoint: Optional[Dict[str, Any]]
) -> set:
    """Get set of parameters to exclude from options.

    Args:
        exclude_list_get_from_options: Whether to exclude list GET query params from options
        list_endpoint: List endpoint data

    Returns:
        Set of parameter names to exclude
    """
    if not exclude_list_get_from_options or not list_endpoint:
        return set()

    if "get" not in list_endpoint["operations"]:
        return set()

    list_get_data = list_endpoint["operations"]["get"]
    if "query" in list_get_data:
        return set(list_get_data["query"].keys())

    return set()


def _add_remaining_parameters(
    options: OrderedDict,
    merged_params: Dict[str, Any],
    excluded_params: set,
    snake_case_all_path_params: List[str],
    snake_case_required_path_params: List[str],
    module_name: str,
) -> None:
    """Add remaining parameters not already in options.

    Args:
        options: Options dictionary to modify in place
        merged_params: Merged parameter dictionary
        excluded_params: Set of parameters to exclude
        snake_case_all_path_params: All path params in snake_case
        snake_case_required_path_params: Required path params in snake_case
        module_name: Name of the module
    """
    for param_name, param_info in merged_params.items():
        if param_name not in options and param_name not in excluded_params:
            options[param_name] = format_parameter_option(
                param_name,
                param_info,
                snake_case_all_path_params,
                snake_case_required_path_params,
                module_name,
            )


def _build_module_options(
    module_name: str,
    endpoints_data: Dict[str, Any],
    list_endpoint: Optional[Dict[str, Any]],
    item_endpoint: Optional[Dict[str, Any]],
    action_endpoints: OrderedDict,
    exclude_list_get_from_options: bool,
    all_path_params: List[str],
    required_path_params: List[str],
) -> OrderedDict:
    """Build the complete options dictionary for the module.

    Args:
        module_name: Name of the module
        endpoints_data: All endpoint data
        list_endpoint: List endpoint data
        item_endpoint: Item endpoint data
        action_endpoints: Action endpoints dictionary
        exclude_list_get_from_options: Whether to exclude list GET query params from options
        all_path_params: All original path parameters
        required_path_params: Required original path parameters

    Returns:
        OrderedDict of module options
    """
    options = OrderedDict()

    # Convert path params to snake_case
    snake_case_all_path_params, snake_case_required_path_params = (
        _convert_params_to_snake_case(all_path_params, required_path_params)
    )

    # Merge all parameters from all operations
    merged_params = merge_parameters(endpoints_data)

    # Add state parameter if needed
    has_list_post = list_endpoint and any(
        m in ["post", "put"] for m in list_endpoint["operations"]
    )
    has_item_delete = item_endpoint and "delete" in item_endpoint["operations"]
    action_names = list(action_endpoints.keys())

    if has_list_post or has_item_delete or action_names:
        options["state"] = create_state_parameter(
            has_list_post, has_item_delete, action_names
        )

    # Add path parameters
    _add_path_parameters_to_options(
        options,
        snake_case_all_path_params,
        all_path_params,
        merged_params,
        snake_case_required_path_params,
        module_name,
    )

    # Get excluded parameters
    excluded_params = _get_excluded_params(exclude_list_get_from_options, list_endpoint)

    # Add remaining parameters
    _add_remaining_parameters(
        options,
        merged_params,
        excluded_params,
        snake_case_all_path_params,
        snake_case_required_path_params,
        module_name,
    )

    return options


def format_api_endpoints_for_module_generation(
    module_name: str, endpoints_data: Dict[str, Any]
) -> OrderedDict:
    """Format complete module specification.

    Args:
        module_name: Name of the module
        endpoints_data: Parsed endpoint data from get_api_endpoints_for_module

    Returns:
        OrderedDict with list_endpoint, item_endpoint, action_endpoints, options
    """
    spec = OrderedDict()

    # Build path parameter mappings for camelCase to snake_case conversion
    path_parameter_mappings = _build_path_parameter_mappings(endpoints_data)

    # Classify and collect endpoints
    non_action_endpoints, action_endpoints = _classify_and_collect_endpoints(
        endpoints_data, path_parameter_mappings
    )

    # Assign list and item endpoints based on count
    list_endpoint, item_endpoint = _assign_endpoints_by_count(non_action_endpoints)

    # Determine if we should exclude list GET query parameters from module options
    exclude_list_get_from_options = _should_omit_list_get_query(
        module_name, list_endpoint, item_endpoint
    )

    # Format endpoints
    spec["list_endpoint"] = _format_endpoint_spec(list_endpoint, "list")
    spec["item_endpoint"] = _format_endpoint_spec(item_endpoint, "item")
    spec["action_endpoints"] = _format_action_endpoints(action_endpoints)

    # Extract and convert path parameters
    all_path_params, required_path_params = extract_path_parameters(endpoints_data)
    snake_case_all_path_params, _ = (  # pylint: disable=disallowed-name
        _convert_params_to_snake_case(all_path_params, required_path_params)
    )

    # Add moid_parameter_hints
    spec["moid_parameter_hints"] = snake_case_all_path_params

    # Build options
    spec["options"] = _build_module_options(
        module_name,
        endpoints_data,
        list_endpoint,
        item_endpoint,
        action_endpoints,
        exclude_list_get_from_options,
        all_path_params,
        required_path_params,
    )

    return spec


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate formatted YAML module specification from module name",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from module name
  python format_api_endpoints_for_module_generation.py vcenter_vm_hardware_floppy

  # Save to file
  python format_api_endpoints_for_module_generation.py vcenter_vm_hardware_floppy -o spec.yaml

  # Use different API version
  python format_api_endpoints_for_module_generation.py vcenter_vm_hardware_floppy --spec-version 8.0.2
        """,
    )

    parser.add_argument(
        "module", help="Module name (e.g., vcenter_resourcepool, appliance_networking)"
    )
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument(
        "--spec-version", default="9.1.0", help="OpenAPI spec version (default: 9.1.0)"
    )

    args = parser.parse_args()

    try:
        # Load API spec and parse endpoints
        print(f"Generating formatted spec for {args.module}...", file=sys.stderr)
        spec_file = get_spec_file_for_module(args.module)
        spec = load_api_spec(args.spec_version, spec_file)
        endpoints_data = parse_module_endpoints(args.module, spec)

        if not endpoints_data:
            print(
                f"Error: No endpoints found for module {args.module}", file=sys.stderr
            )
            sys.exit(1)

        # Format the spec
        formatted_spec = format_api_endpoints_for_module_generation(
            args.module, endpoints_data
        )

        # Output
        yaml_output = yaml.dump(
            formatted_spec,
            Dumper=OrderedDumper,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=120,
        )

        if args.output:
            Path(args.output).write_text(yaml_output)
            print(f"Wrote spec to {args.output}", file=sys.stderr)
        else:
            print(yaml_output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
