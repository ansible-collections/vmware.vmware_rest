#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Generate Ansible modules from module name.

This script automatically calls the required scripts to generate endpoint data,
then generates complete module files in the new format that uses
VmwareRestCrudModuleBase or VmwareRestInfoModuleBase with OperationConfig objects.
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import textwrap

# Import utilities from _generation_lib
from _generation_lib import get_collection_version

# Import from sibling scripts
from get_api_endpoints_for_module import (
    load_api_spec,
    get_spec_file_for_module,
    parse_module_endpoints,
)
from format_api_endpoints_for_module_generation import (
    format_api_endpoints_for_module_generation,
)

# ============================================================================
# CONSTANTS AND TEMPLATES
# ============================================================================

FILTER_ALIAS_PARAMS = {"datacenters", "folders", "names", "types", "type"}

HEADER_TEMPLATE = """#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This module is generated using LLM agents and skills defined in the vmware.vmware_rest repository.
# See: https://github.com/ansible-collections/vmware.vmware_rest
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type
"""


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def format_dict_literal(dict_obj: Dict, indent: int = 0) -> str:
    """
    Format a Python dictionary as a code string.

    Args:
        dict_obj: Dictionary to format
        indent: Base indentation level (spaces)

    Returns:
        Formatted dictionary as string
    """
    if not dict_obj:
        return "{}"

    lines = ["{"]
    base_indent = " " * indent
    item_indent = " " * (indent + 4)

    for key, value in dict_obj.items():
        if isinstance(value, dict):
            # Nested dict - recurse
            nested = format_dict_literal(value, indent + 4)
            lines.append(f'{item_indent}"{key}": {nested},')
        elif isinstance(value, bool):
            # Python boolean literal
            lines.append(f'{item_indent}"{key}": {value},')
        elif isinstance(value, (int, float)):
            # Numeric literal
            lines.append(f'{item_indent}"{key}": {value},')
        elif isinstance(value, str):
            # String literal - escape quotes
            escaped = value.replace('"', '\\"')
            lines.append(f'{item_indent}"{key}": "{escaped}",')
        elif value is None:
            lines.append(f'{item_indent}"{key}": None,')
        else:
            # Fallback - repr
            lines.append(f'{item_indent}"{key}": {repr(value)},')

    lines.append(base_indent + "}")
    return "\n".join(lines)


def indent_lines(lines: List[str], indent_level: int) -> str:
    """
    Indent a list of strings by the given level.

    Args:
        lines: List of string lines
        indent_level: Number of 4-space indents to add

    Returns:
        Joined string with indentation
    """
    indent = " " * (indent_level * 4)
    return "\n".join(indent + line if line.strip() else line for line in lines)


def _format_yaml_description(
    param_def: Dict, base_indent: str, lines: List[str]
) -> None:
    """Add description section to YAML lines.

    Args:
        param_def: Parameter definition
        base_indent: Base indentation string
        lines: List to append lines to
    """
    if "description" not in param_def:
        return

    lines.append(f"{base_indent}  description:")
    for desc_line in param_def["description"]:
        lines.append(f"{base_indent}    - {desc_line}")


def _format_yaml_choices(param_def: Dict, base_indent: str, lines: List[str]) -> None:
    """Add choices section to YAML lines.

    Args:
        param_def: Parameter definition
        base_indent: Base indentation string
        lines: List to append lines to
    """
    if "choices" not in param_def:
        return

    lines.append(f"{base_indent}  choices:")
    for choice in param_def["choices"]:
        lines.append(f"{base_indent}    - {choice}")


def _format_yaml_simple_fields(
    param_def: Dict, base_indent: str, lines: List[str]
) -> None:
    """Add simple scalar fields to YAML lines.

    Args:
        param_def: Parameter definition
        base_indent: Base indentation string
        lines: List to append lines to
    """
    if "type" in param_def:
        lines.append(f"{base_indent}  type: {param_def['type']}")

    if "required" in param_def:
        lines.append(f"{base_indent}  required: {str(param_def['required']).lower()}")

    if "default" in param_def:
        lines.append(f"{base_indent}  default: {param_def['default']}")

    if "elements" in param_def:
        lines.append(f"{base_indent}  elements: {param_def['elements']}")


def _format_yaml_suboptions(
    param_def: Dict, base_indent: str, lines: List[str], indent: int
) -> None:
    """Add suboptions section to YAML lines.

    Args:
        param_def: Parameter definition
        base_indent: Base indentation string
        lines: List to append lines to
        indent: Base indentation level (spaces)
    """
    if "suboptions" not in param_def:
        return

    lines.append(f"{base_indent}  suboptions:")
    suboptions_yaml = format_options_yaml(param_def["suboptions"], indent + 4)
    lines.append(suboptions_yaml)


def _format_yaml_aliases(param_def: Dict, base_indent: str, lines: List[str]) -> None:
    """Add aliases section to YAML lines.

    Args:
        param_def: Parameter definition
        base_indent: Base indentation string
        lines: List to append lines to
    """
    if "aliases" not in param_def:
        return

    lines.append(f"{base_indent}  aliases:")
    for alias in param_def["aliases"]:
        lines.append(f"{base_indent}    - {alias}")


def _format_single_option(
    param_name: str, param_def: Dict, base_indent: str, indent: int, lines: List[str]
) -> None:
    """Format a single parameter option.

    Args:
        param_name: Parameter name
        param_def: Parameter definition
        base_indent: Base indentation string
        indent: Base indentation level (spaces)
        lines: List to append lines to
    """
    lines.append(f"{base_indent}{param_name}:")
    _format_yaml_aliases(param_def, base_indent, lines)
    _format_yaml_description(param_def, base_indent, lines)
    _format_yaml_simple_fields(param_def, base_indent, lines)
    _format_yaml_choices(param_def, base_indent, lines)
    _format_yaml_suboptions(param_def, base_indent, lines, indent)


def format_options_yaml(options_dict: Dict, indent: int = 2) -> str:
    """
    Format options dictionary as YAML for DOCUMENTATION section.

    Args:
        options_dict: Options from YAML spec
        indent: Base indentation level (spaces)

    Returns:
        YAML-formatted options string
    """
    lines = []
    base_indent = " " * indent

    for param_name, param_def in options_dict.items():
        _format_single_option(param_name, param_def, base_indent, indent, lines)

    return "\n".join(lines)


# ============================================================================
# INPUT PROCESSING
# ============================================================================


def generate_yaml_spec(module_name: str, spec_version: str) -> Dict:
    """
    Generate YAML specification by calling format_api_endpoints_for_module_generation.

    Args:
        module_name: Name of the module
        spec_version: OpenAPI spec version

    Returns:
        Formatted YAML data as dict
    """
    # Step 1: Get API endpoints
    spec_file = get_spec_file_for_module(module_name)
    spec = load_api_spec(spec_version, spec_file)
    endpoints_data = parse_module_endpoints(module_name, spec)

    if not endpoints_data:
        raise ValueError(f"No endpoints found for module {module_name}")

    # Step 2: Format endpoints for module generation
    return format_api_endpoints_for_module_generation(module_name, endpoints_data)


def validate_yaml_structure(yaml_data: Dict) -> None:
    """
    Validate YAML has required structure.

    Args:
        yaml_data: Parsed YAML data

    Raises:
        ValueError: If YAML structure is invalid
    """
    required_keys = ["options"]
    missing = [k for k in required_keys if k not in yaml_data]

    if missing:
        raise ValueError(f"YAML missing required keys: {missing}")

    # Must have at least one endpoint
    has_endpoint = (
        yaml_data.get("list_endpoint")
        or yaml_data.get("item_endpoint")
        or yaml_data.get("action_endpoints")
    )

    if not has_endpoint:
        raise ValueError("YAML must define at least one endpoint")


def detect_available_operations(yaml_data: Dict) -> Dict[str, bool]:
    """
    Determine which operations are available from the YAML spec.

    Args:
        yaml_data: Parsed YAML data

    Returns:
        Dict with operation availability flags
    """
    ops = {
        "has_list": False,
        "has_get": False,
        "has_create": False,
        "has_update": False,
        "has_delete": False,
        "has_actions": False,
    }

    # Check list endpoint
    if "list_endpoint" in yaml_data and yaml_data["list_endpoint"]:
        list_ops = yaml_data["list_endpoint"].get("operations", {})
        ops["has_list"] = "get" in list_ops
        ops["has_create"] = "post" in list_ops

    # Check item endpoint
    if "item_endpoint" in yaml_data and yaml_data["item_endpoint"]:
        item_ops = yaml_data["item_endpoint"].get("operations", {})
        ops["has_get"] = "get" in item_ops
        ops["has_update"] = "patch" in item_ops or "put" in item_ops
        ops["has_delete"] = "delete" in item_ops

    # Check actions
    if "action_endpoints" in yaml_data and yaml_data["action_endpoints"]:
        ops["has_actions"] = bool(yaml_data["action_endpoints"])

    return ops


# ============================================================================
# BODY/QUERY SPEC BUILDERS
# ============================================================================


def _get_required_flag(nested_body_params: Dict, param_name: str) -> bool:
    """Get required flag from nested body params.

    Args:
        nested_body_params: Nested body params dictionary
        param_name: Parameter name to look up

    Returns:
        True if parameter is required, False otherwise
    """
    if not nested_body_params:
        return False

    is_required = nested_body_params.get(param_name, False)
    return is_required if isinstance(is_required, bool) else False


def _get_further_nested_params(nested_body_params: Dict, param_name: str) -> Dict:
    """Get further nested parameters for a parameter.

    Args:
        nested_body_params: Nested body params dictionary
        param_name: Parameter name to look up

    Returns:
        Dictionary of further nested params or empty dict
    """
    param_value = nested_body_params.get(param_name, {})
    return param_value if isinstance(param_value, dict) else {}


def _build_nested_param_spec(
    param_name: str,
    param_def: Dict,
    options_dict: Dict,
    nested_body_params: Dict,
    parent_key: str,
) -> Dict:
    """Build spec for a nested parameter.

    Args:
        param_name: Parameter name
        param_def: Parameter definition
        options_dict: Full options dict
        nested_body_params: Nested body params
        parent_key: Parent key path

    Returns:
        Parameter spec with required flag and subspec
    """
    is_required = _get_required_flag(nested_body_params, param_name)
    further_nested = _get_further_nested_params(nested_body_params, param_name)
    new_parent_key = f"{parent_key}.{param_name}" if parent_key else param_name

    return {
        "required": is_required,
        "subspec": build_subspec(
            param_def["suboptions"],
            options_dict,
            further_nested,
            new_parent_key,
        ),
    }


def _build_leaf_param_spec(nested_body_params: Dict, param_name: str) -> Dict:
    """Build spec for a leaf parameter.

    Args:
        nested_body_params: Nested body params
        param_name: Parameter name

    Returns:
        Parameter spec with required flag
    """
    return {"required": _get_required_flag(nested_body_params, param_name)}


def build_subspec(
    suboptions: Dict, options_dict: Dict, nested_body_params: Dict, parent_key: str = ""
) -> Dict:
    """
    Recursively build subspec from nested suboptions.

    Args:
        suboptions: Suboptions dict from parameter definition
        options_dict: Full options dict for looking up nested structures
        nested_body_params: Nested body params from YAML with required flags
        parent_key: Parent parameter key for nested lookups

    Returns:
        Subspec dict
    """
    subspec = {}

    for param_name, param_def in suboptions.items():
        if param_def.get("type") == "dict" and "suboptions" in param_def:
            subspec[param_name] = _build_nested_param_spec(
                param_name, param_def, options_dict, nested_body_params, parent_key
            )
        else:
            subspec[param_name] = _build_leaf_param_spec(nested_body_params, param_name)

    return subspec


def build_body_spec(body_params: Dict, options_dict: Dict) -> Optional[Dict]:
    """
    Convert body params from YAML to body_spec dict for OperationConfig.

    Args:
        body_params: Dict of {param_name: is_required_or_nested_dict} from YAML
        options_dict: Complete options dict from YAML

    Returns:
        body_spec dict or None if no body params
    """
    if not body_params:
        return None

    spec = {}

    for param_name, param_value in body_params.items():
        # param_value can be:
        # - A boolean (true/false) for simple parameters
        # - A dict of nested params for complex parameters
        param_option = options_dict.get(param_name, {})

        if param_option.get("type") == "dict" and "suboptions" in param_option:
            # Has nested structure - build subspec
            # If param_value is a dict, it contains the nested required flags
            # If param_value is a boolean, use empty dict for nested params
            nested_params = param_value if isinstance(param_value, dict) else {}

            # The parameter itself is required if ALL nested values are dict, OR if it's explicitly True
            # In the YAML structure, if we have backing: {type: true, ...}, backing itself is not required
            # but its nested params have their own required flags
            is_param_required = param_value if isinstance(param_value, bool) else False

            spec[param_name] = {
                "required": is_param_required,
                "subspec": build_subspec(
                    param_option["suboptions"], options_dict, nested_params, param_name
                ),
            }
        else:
            # Simple parameter - param_value should be a boolean
            spec[param_name] = {
                "required": param_value if isinstance(param_value, bool) else False
            }

    return spec


def build_query_spec(query_params: Dict, options_dict: Dict) -> Optional[Dict]:
    """
    Convert query params from YAML to query_spec dict for OperationConfig.

    Args:
        query_params: Dict of {param_name: is_required} from YAML
        options_dict: Complete options dict from YAML

    Returns:
        query_spec dict or None if no query params
    """
    # Query spec uses same structure as body spec
    return build_body_spec(query_params, options_dict)


# ============================================================================
# OPERATION CONFIG GENERATORS
# ============================================================================


def generate_operation_config(
    operation_name: str,
    uri: str,
    http_method: str,
    body_spec: Optional[Dict] = None,
    query_spec: Optional[Dict] = None,
    is_list_operation: bool = False,
) -> str:
    """
    Generate a single OperationConfig constant.

    Args:
        operation_name: Name of the operation (e.g., "get", "create")
        uri: URI template string
        http_method: HTTP method (GET, POST, PATCH, DELETE)
        body_spec: Optional body_spec dict
        query_spec: Optional query_spec dict
        is_list_operation: True if this is a list operation

    Returns:
        Python code string for OperationConfig
    """
    lines = [
        f"{operation_name.upper()}_OPERATION = OperationConfig(",
        f'    name="{operation_name}",',
    ]

    # Determine which endpoint constant to use
    if is_list_operation or (operation_name in ["list", "create"] and "{" not in uri):
        lines.append("    uri=LIST_ENDPOINT,")
    else:
        lines.append("    uri=ITEM_ENDPOINT,")

    lines.append(f'    http_method="{http_method}",')

    # Add body_spec if present
    if body_spec:
        body_spec_str = format_dict_literal(body_spec, indent=4)
        lines.append(f"    body_spec={body_spec_str},")

    # Add query_spec if present
    if query_spec:
        query_spec_str = format_dict_literal(query_spec, indent=4)
        lines.append(f"    query_spec={query_spec_str},")

    lines.append(")")

    return "\n".join(lines)


def _get_singular_form(plural_name: str) -> Optional[str]:
    """Return the singular form of a plural parameter name, or None if unknown.

    Args:
        plural_name: Plural parameter name (e.g., "names", "folders")

    Returns:
        Singular form or None
    """
    if plural_name.endswith("ss"):
        return None
    if plural_name.endswith("ies"):
        return plural_name[:-3] + "y"
    if plural_name.endswith(("ses", "xes", "zes")):
        return plural_name[:-2]
    if plural_name.endswith("s"):
        return plural_name[:-1]
    return None


def _build_crud_list_query_spec(
    query_params: Dict, options_dict: Dict
) -> Optional[Dict]:
    """Build query_spec for a CRUD module's LIST operation.

    Only includes filters that have a matching singular module param,
    and adds a module_param key to map the plural API name to the singular option.

    Args:
        query_params: Dict of {filter_name: is_required} from YAML
        options_dict: Module options dict

    Returns:
        query_spec dict or None if no matching filters
    """
    if not query_params:
        return None

    spec = {}
    for filter_name, is_required in query_params.items():
        singular = _get_singular_form(filter_name)
        if singular and singular in options_dict:
            spec[filter_name] = {
                "required": is_required if isinstance(is_required, bool) else False,
                "module_param": singular,
            }

    return spec if spec else None


def generate_all_operations(
    yaml_data: Dict,
    options_dict: Dict,
    available_ops: Dict[str, bool],
    is_info_module: bool = False,
) -> str:
    """
    Generate all OperationConfig constants based on available operations.

    Args:
        yaml_data: Complete YAML data
        options_dict: Options dict from YAML
        available_ops: Dict of operation availability flags
        is_info_module: True if this is an info module

    Returns:
        Python code string for all operations
    """
    operations = []

    list_endpoint = yaml_data.get("list_endpoint", {})
    item_endpoint = yaml_data.get("item_endpoint", {})

    # Generate LIST operation
    if available_ops["has_list"]:
        list_ops = list_endpoint.get("operations", {})
        get_op = list_ops.get("get", {})
        query_params = get_op.get("query", {})

        if is_info_module:
            query_spec = build_query_spec(query_params, options_dict)
        else:
            query_spec = _build_crud_list_query_spec(query_params, options_dict)

        op = generate_operation_config(
            "list",
            list_endpoint["uri"],
            "GET",
            query_spec=query_spec,
            is_list_operation=True,
        )
        operations.append(op)

    # Generate GET operation
    if available_ops["has_get"]:
        op = generate_operation_config("get", item_endpoint["uri"], "GET")
        operations.append(op)

    # Generate CREATE operation
    if available_ops["has_create"]:
        list_ops = list_endpoint.get("operations", {})
        post_op = list_ops.get("post", {})
        body_params = post_op.get("body", {})
        body_spec = build_body_spec(body_params, options_dict)

        op = generate_operation_config(
            "create",
            list_endpoint["uri"],
            "POST",
            body_spec=body_spec,
            is_list_operation=True,
        )
        operations.append(op)

    # Generate UPDATE operation
    if available_ops["has_update"]:
        item_ops = item_endpoint.get("operations", {})
        patch_op = item_ops.get("patch", item_ops.get("put", {}))
        body_params = patch_op.get("body", {})
        body_spec = build_body_spec(body_params, options_dict)

        http_method = "PATCH" if "patch" in item_ops else "PUT"

        op = generate_operation_config(
            "update", item_endpoint["uri"], http_method, body_spec=body_spec
        )
        operations.append(op)

    # Generate DELETE operation
    if available_ops["has_delete"]:
        item_ops = item_endpoint.get("operations", {})
        delete_op = item_ops.get("delete", {})
        query_params = delete_op.get("query", {})
        query_spec = (
            build_query_spec(query_params, options_dict) if query_params else None
        )

        op = generate_operation_config(
            "delete", item_endpoint["uri"], "DELETE", query_spec=query_spec
        )
        operations.append(op)

    return "\n\n".join(operations)


def generate_action_operations(action_endpoints: Dict, options_dict: Dict) -> str:
    """
    Generate ACTION_OPERATIONS dictionary for action endpoints.

    Args:
        action_endpoints: Dict of action endpoint specs from YAML
        options_dict: Options dict from YAML

    Returns:
        Python code string for ACTION_OPERATIONS dict
    """
    if not action_endpoints:
        return ""

    lines = ["ACTION_OPERATIONS = {"]

    for action_name in sorted(action_endpoints.keys()):
        action_data = action_endpoints[action_name]
        uri = action_data["uri"]
        operations = action_data.get("operations", {})

        # Most actions use POST
        post_op = operations.get("post", {})
        body_params = post_op.get("body", {})
        body_spec = build_body_spec(body_params, options_dict)

        lines.append(f'    "{action_name}": OperationConfig(')
        lines.append(f'        name="{action_name}",')
        lines.append(f'        uri="{uri}",')
        lines.append('        http_method="POST",')

        if body_spec:
            body_spec_str = format_dict_literal(body_spec, indent=8)
            lines.append(f"        body_spec={body_spec_str},")

        lines.append("    ),")

    lines.append("}")

    return "\n".join(lines)


# ============================================================================
# ARGUMENT SPEC GENERATOR
# ============================================================================


def convert_option_to_arg_spec(option_def: Dict) -> Dict:
    """
    Convert single option from YAML documentation format to argument_spec format.

    Args:
        option_def: Option definition from YAML

    Returns:
        argument_spec dict for this option
    """
    spec = {"type": option_def["type"]}

    # Add aliases if present
    if "aliases" in option_def:
        spec["aliases"] = option_def["aliases"]

    # Add choices if present
    if "choices" in option_def:
        spec["choices"] = option_def["choices"]

    # Add default if present
    if "default" in option_def:
        spec["default"] = option_def["default"]

    # Add elements for lists
    if "elements" in option_def:
        spec["elements"] = option_def["elements"]

    # Add required
    # For nested suboptions: always honor the required flag
    # For top-level params: only mark as required if the option definition says so
    # (this happens for path parameters that appear in ALL endpoints)
    # Body/query params are never marked required at top level because
    # requirements are conditional on the operation (state)
    if option_def.get("required"):
        spec["required"] = True

    # Handle nested options (suboptions -> options)
    if "suboptions" in option_def:
        spec["options"] = {}
        for subopt_name, subopt_def in option_def["suboptions"].items():
            spec["options"][subopt_name] = convert_option_to_arg_spec(subopt_def)

    return spec


def generate_argument_spec_function(options_dict: Dict, is_info_module: bool) -> str:
    """
    Generate create_module_argument_spec() function.

    Args:
        options_dict: Options dict from YAML
        is_info_module: True if this is an info module

    Returns:
        Python code string for the function
    """
    lines = [
        "def create_module_argument_spec() -> dict:",
        "    module_args = connection_params_argument_spec()",
    ]

    # Add all parameters except 'state' (handled specially)
    for param_name in sorted(options_dict.keys()):
        if param_name == "state":
            continue

        param_def = options_dict[param_name]
        arg_spec = convert_option_to_arg_spec(param_def)

        # Format the spec dict
        spec_str = format_dict_literal(arg_spec, indent=4)
        lines.append(f'    module_args["{param_name}"] = {spec_str}')

    # Add state parameter if not info module
    if not is_info_module and "state" in options_dict:
        state_def = options_dict["state"]
        state_spec = convert_option_to_arg_spec(state_def)
        spec_str = format_dict_literal(state_spec, indent=4)
        lines.append(f'    module_args["state"] = {spec_str}')

    lines.append("    return module_args")

    return "\n".join(lines)


# ============================================================================
# SECTION GENERATORS
# ============================================================================


def generate_documentation(
    module_name: str, options_dict: Dict, api_version: str
) -> str:
    """
    Generate DOCUMENTATION, EXAMPLES, and RETURN sections.

    Args:
        module_name: Name of the module
        options_dict: Options dict from YAML
        api_version: API version string

    Returns:
        Python code string for documentation sections
    """
    version = get_collection_version()
    options_yaml = format_options_yaml(options_dict)

    doc = f'''
DOCUMENTATION = r"""
module: {module_name}
short_description: PLACEHOLDER
description:
  - PLACEHOLDER

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
{options_yaml}

version_added: {version}

requirements: []

notes:
  - Generated from vSphere API spec {api_version}.
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""
'''
    return doc.strip()


def generate_imports(is_info_module: bool) -> str:
    """
    Generate Python imports section.

    Args:
        is_info_module: True if this is an info module

    Returns:
        Python code string for imports
    """
    base_class = (
        "VmwareRestInfoModuleBase" if is_info_module else "VmwareRestCrudModuleBase"
    )
    module_file = "_info_module" if is_info_module else "_crud_module"

    imports = f"""
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    VmwareModuleError,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils.{module_file} import (
    {base_class},
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)
"""
    return imports.strip()


def generate_constants(
    moid_hints: List[str], list_endpoint: Dict, item_endpoint: Dict
) -> str:
    """
    Generate constant definitions (MOID_PARAMETER_HINTS, endpoints).

    Args:
        moid_hints: List of MOID parameter names
        list_endpoint: List endpoint spec
        item_endpoint: Item endpoint spec

    Returns:
        Python code string for constants
    """
    moid_list = ", ".join(f'"{hint}"' for hint in moid_hints)

    list_uri = list_endpoint.get("uri", "") if list_endpoint else ""
    item_uri = item_endpoint.get("uri", "") if item_endpoint else ""

    constants = f"""
MOID_PARAMETER_HINTS = [{moid_list}]

LIST_ENDPOINT = "{list_uri}"
ITEM_ENDPOINT = "{item_uri}"
"""
    return constants.strip()


def _generate_info_module_main(available_ops: Dict[str, bool]) -> str:
    """Generate main() function for info modules.

    Args:
        available_ops: Dict of operation availability flags

    Returns:
        Python code string for info module main() function
    """
    op_assignments = [
        "        get_operation_config=GET_OPERATION,",
    ]
    if available_ops["has_list"]:
        op_assignments.append("        list_operation_config=LIST_OPERATION,")

    op_block = "\n".join(op_assignments)

    return f"""
def main():
    module = AnsibleModule(
        argument_spec=create_module_argument_spec(),
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModuleBase(
        module=module,
        moid_parameter_hints=MOID_PARAMETER_HINTS,
{op_block}
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
"""


def _build_operation_assignments(
    available_ops: Dict[str, bool], has_actions: bool
) -> str:
    """Build operation config assignments for CRUD module.

    Args:
        available_ops: Dict of operation availability flags
        has_actions: True if actions are defined

    Returns:
        String of operation assignments
    """
    op_map = [
        ("has_get", "        get_operation_config=GET_OPERATION,"),
        ("has_list", "        list_operation_config=LIST_OPERATION,"),
        ("has_create", "        create_operation_config=CREATE_OPERATION,"),
        ("has_update", "        update_operation_config=UPDATE_OPERATION,"),
        ("has_delete", "        delete_operation_config=DELETE_OPERATION,"),
    ]

    assignments = [assignment for op_key, assignment in op_map if available_ops[op_key]]

    if has_actions:
        assignments.append("        action_operations=ACTION_OPERATIONS,")

    return "\n".join(assignments)


def _build_state_handler(available_ops: Dict[str, bool], has_actions: bool) -> str:
    """Build the state dispatch block for CRUD module main().

    Only includes branches for states the module actually supports,
    avoiding unreachable code.

    Args:
        available_ops: Dict of operation availability flags
        has_actions: True if actions are defined

    Returns:
        String of if/elif branches for state handling
    """
    has_present = available_ops.get("has_create") or available_ops.get("has_update")
    has_absent = available_ops.get("has_delete")

    branches = []

    if has_present:
        branches.append(
            'module.params["state"] == "present":\n'
            "            result = crud_module.ensure_present()"
        )

    if has_absent:
        branches.append(
            'module.params["state"] == "absent":\n'
            "            result = crud_module.ensure_absent()"
        )

    if has_actions:
        branches.append(
            'module.params["state"] in ACTION_OPERATIONS:\n'
            "            result = crud_module.perform_action()"
        )

    lines = []
    for i, branch in enumerate(branches):
        keyword = "if" if i == 0 else "elif"
        lines.append(f"        {keyword} {branch}")

    lines.append(
        "        else:\n"
        '            module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))'
    )

    return "\n".join(lines)


def _generate_crud_module_main(
    available_ops: Dict[str, bool], has_actions: bool
) -> str:
    """Generate main() function for CRUD modules.

    Args:
        available_ops: Dict of operation availability flags
        has_actions: True if actions are defined

    Returns:
        Python code string for CRUD module main() function
    """
    op_assignments_str = _build_operation_assignments(available_ops, has_actions)
    state_handler = _build_state_handler(available_ops, has_actions)

    return f"""
def main():
    module = AnsibleModule(
        argument_spec=create_module_argument_spec(),
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModuleBase(
        module=module,
        moid_parameter_hints=MOID_PARAMETER_HINTS,
{op_assignments_str}
    )

    try:
{state_handler}
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
"""


def generate_main_function(
    is_info_module: bool, available_ops: Dict[str, bool], has_actions: bool
) -> str:
    """
    Generate main() function.

    Args:
        is_info_module: True if this is an info module
        available_ops: Dict of operation availability flags
        has_actions: True if actions are defined

    Returns:
        Python code string for main() function
    """
    if is_info_module:
        main_func = _generate_info_module_main(available_ops)
    else:
        main_func = _generate_crud_module_main(available_ops, has_actions)

    return main_func.strip()


# ============================================================================
# ASSEMBLY AND OUTPUT
# ============================================================================


def assemble_module(
    header: str,
    documentation: str,
    imports: str,
    constants: str,
    operations: str,
    action_operations: str,
    argument_spec: str,
    main_func: str,
) -> str:
    """
    Assemble all sections into complete module code.

    Args:
        header: Module header
        documentation: DOCUMENTATION/EXAMPLES/RETURN sections
        imports: Import statements
        constants: Constant definitions
        operations: OperationConfig definitions
        action_operations: ACTION_OPERATIONS dict (may be empty)
        argument_spec: create_module_argument_spec() function
        main_func: main() function

    Returns:
        Complete module code
    """
    sections = [header, documentation, imports, constants, operations]

    # Add action operations if present
    if action_operations:
        sections.append(action_operations)

    sections.extend([argument_spec, main_func])

    # Join with double newlines between sections
    return "\n\n\n".join(sections) + "\n"


def write_module_file(
    module_code: str, module_name: str, output_path: Optional[str] = None
) -> Path:
    """
    Write module code to file.

    Args:
        module_code: Complete module code
        module_name: Name of the module
        output_path: Optional output path, defaults to plugins/modules/{module_name}.py

    Returns:
        Path where file was written
    """
    if output_path:
        file_path = Path(output_path)
    else:
        # Default to plugins/modules/
        project_root = Path(__file__).parent.parent
        file_path = project_root / "plugins" / "modules" / f"{module_name}.py"

    # Ensure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write file
    file_path.write_text(module_code)

    return file_path


# ============================================================================
# MAIN GENERATION FUNCTION
# ============================================================================


def generate_module(yaml_data: Dict, module_name: str, api_version: str) -> str:
    """
    Main generation function - orchestrates the entire module generation.

    Args:
        yaml_data: Parsed YAML spec
        module_name: Name of the module
        api_version: API version string

    Returns:
        Complete module code
    """
    # 1. Determine module type
    is_info = module_name.endswith(("_info", "_query"))

    # 2. Detect available operations
    available_ops = detect_available_operations(yaml_data)

    # 3. Extract data from YAML
    options = yaml_data.get("options", {})
    moid_hints = yaml_data.get("moid_parameter_hints", [])
    list_endpoint = yaml_data.get("list_endpoint", {})
    item_endpoint = yaml_data.get("item_endpoint", {})
    action_endpoints = yaml_data.get("action_endpoints", {})

    # 3b. Add filter_ aliases for info modules
    if is_info:
        for param_name in options:
            if param_name in FILTER_ALIAS_PARAMS:
                options[param_name]["aliases"] = [f"filter_{param_name}"]

    # 4. Generate sections
    header = HEADER_TEMPLATE.strip()
    documentation = generate_documentation(module_name, options, api_version)
    imports = generate_imports(is_info)
    constants = generate_constants(moid_hints, list_endpoint, item_endpoint)
    operations = generate_all_operations(yaml_data, options, available_ops, is_info)
    action_ops = generate_action_operations(action_endpoints, options)
    argument_spec = generate_argument_spec_function(options, is_info)
    main_func = generate_main_function(is_info, available_ops, bool(action_endpoints))

    # 5. Assemble module
    return assemble_module(
        header,
        documentation,
        imports,
        constants,
        operations,
        action_ops,
        argument_spec,
        main_func,
    )


# ============================================================================
# CLI INTERFACE
# ============================================================================


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Generate Ansible module from module name",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            Examples:
              # Generate from module name
              %(prog)s vcenter_resourcepool

              # Specify output location
              %(prog)s vcenter_resourcepool -o /tmp/test.py

              # Use different API version
              %(prog)s vcenter_resourcepool --spec-version 8.0.2
        """),
    )

    parser.add_argument(
        "module_name",
        help="Module name (e.g., vcenter_resourcepool or vcenter_resourcepool_info)",
    )
    parser.add_argument(
        "--output", "-o", help="Output file (default: plugins/modules/{module_name}.py)"
    )
    parser.add_argument(
        "--spec-version",
        default="9.1.0",
        help="OpenAPI spec version (default: 9.1.0)",
    )
    parser.add_argument(
        "--api-version",
        "-a",
        help="API version for documentation (default: same as --spec-version)",
    )

    args = parser.parse_args()

    # Set api_version to spec_version if not explicitly provided
    api_version = args.api_version or args.spec_version

    try:
        # Auto-generate YAML spec from module name
        print(f"Generating module for {args.module_name}...", file=sys.stderr)
        yaml_data = generate_yaml_spec(args.module_name, args.spec_version)

        # Validate
        validate_yaml_structure(yaml_data)

        # Generate
        module_code = generate_module(yaml_data, args.module_name, api_version)

        # Write
        output_file = write_module_file(module_code, args.module_name, args.output)

        print(f"Successfully generated: {output_file}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
