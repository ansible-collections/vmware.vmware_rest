#!/usr/bin/env python
"""
Shared utilities for module and mock generation scripts.

This library provides reusable components for generating Ansible modules and test
mocks from vSphere OpenAPI specifications. It centralizes common functionality to
avoid code duplication and ensure consistency across all generation scripts.

Overview
--------
The library provides utilities for:

1. **String Conversion**: Convert API path parameters to Python variable names
2. **API Path Matching**: Find and normalize API paths for comparison
3. **Schema Resolution**: Resolve OpenAPI schema references
4. **Collection Metadata**: Access project-level information (version, paths)

Integration Example
-------------------
To use this library in a new generation script:

    from _generation_lib import (
        path_param_to_python,
        normalize_path_for_comparison,
        resolve_schema_ref,
        get_collection_version,
    )

    # Convert API parameter to Python name
    param = path_param_to_python("{resourcePool}")  # "resource_pool"

    # Normalize paths for comparison
    normalized = normalize_path_for_comparison("/vcenter/datacenter/{datacenter}")

    # Resolve schema references
    schema = resolve_schema_ref(spec, "#/components/schemas/Datacenter")

    # Get collection version
    version = get_collection_version()
"""

import re
from pathlib import Path
from typing import Any, Dict, List

from _common_lib import camel_to_snake

# ============================================================================
# String Conversion Utilities
# ============================================================================
#
# These functions handle conversion between different naming conventions used
# in the vSphere API and Ansible modules.
#
# Usage Pattern:
#   API parameter "{resourcePool}" -> path_param_to_python() -> "resource_pool"
#


def path_param_to_python(param: str) -> str:
    """Convert API path parameter to Python variable name.

    Removes curly braces, converts hyphens to underscores, and applies snake_case.

    Examples:
        >>> path_param_to_python("{datacenter}")
        'datacenter'
        >>> path_param_to_python("{resourcePool}")
        'resource_pool'
        >>> path_param_to_python("{resource-pool}")
        'resource_pool'
    """
    param = param.strip("{}")
    param = param.replace("-", "_")
    param = camel_to_snake(param)
    return param


# ============================================================================
# Collection Metadata
# ============================================================================
#
# Access project-level metadata from galaxy.yml.
#


def get_collection_version() -> str:
    """Get collection version from galaxy.yml.

    Returns:
        Version string, defaults to "5.0.0" if not found
    """
    try:
        # Find project root by looking for galaxy.yml
        current = Path(__file__).parent
        project_root = current.parent  # content_generation/ -> project root
        galaxy_path = project_root / "galaxy.yml"

        if galaxy_path.exists():
            import yaml

            with open(galaxy_path, "r") as f:
                galaxy_data = yaml.safe_load(f)
                return galaxy_data.get("version", "5.0.0")
    except Exception:
        pass

    return "5.0.0"


# ============================================================================
# Path Normalization and Matching
# ============================================================================
#
# These utilities support module classification and API path matching by
# normalizing paths for comparison and finding matching endpoints.
#
# Used by classify_all_modules.py to match module names to API paths.
#


def normalize_path_for_comparison(path: str) -> str:
    """Normalize path for comparison by removing parameters and query strings.

    Args:
        path: API path to normalize

    Returns:
        Normalized path without parameters or query strings

    Examples:
        >>> normalize_path_for_comparison("/vcenter/datacenter/{datacenter}")
        '/vcenter/datacenter'
        >>> normalize_path_for_comparison("/vcenter/vm?action=start")
        '/vcenter/vm'
    """
    # Remove query parameters (?action=...)
    path = path.split("?")[0]
    # Remove path parameters ({vm}, {datacenter}, etc.) but keep the slashes
    path = re.sub(r"/\{[^}]+\}", "", path)
    # Remove trailing slashes
    path = path.rstrip("/")
    return path


def find_matching_paths(api_paths: List[str], search_path: str) -> List[str]:
    """Find all API paths that match the module's resource path.

    Args:
        api_paths: List of all API paths from the spec
        search_path: Path to search for (may contain parameters)

    Returns:
        List of matching API paths

    Examples:
        >>> find_matching_paths(["/vcenter/datacenter", "/vcenter/datacenter/{datacenter}"], "/vcenter/datacenter")
        ['/vcenter/datacenter', '/vcenter/datacenter/{datacenter}']
    """
    matches = []
    search_normalized = normalize_path_for_comparison(search_path)

    for api_path in api_paths:
        api_normalized = normalize_path_for_comparison(api_path)

        # Exact match on normalized paths
        if api_normalized == search_normalized:
            matches.append(api_path)

    return matches


def module_name_to_api_path(module_name: str) -> str:
    """Convert module name to API path following vSphere conventions.

    Handles compound words, special prefixes, and nested resources.

    Args:
        module_name: Module name (e.g., "vcenter_datacenter", "vcenter_resourcepool_info")

    Returns:
        API path (e.g., "/vcenter/datacenter", "/vcenter/resource-pool")

    Examples:
        >>> module_name_to_api_path("vcenter_datacenter")
        '/vcenter/datacenter'
        >>> module_name_to_api_path("vcenter_resourcepool_info")
        '/vcenter/resource-pool'
        >>> module_name_to_api_path("vcenter_vm_tools_installer")
        '/vcenter/vm/tools/installer'
    """
    # Strip _info suffix
    name = module_name.replace("_info", "")

    # Map service prefixes
    parts = name.split("_")

    # First part is service (vcenter, appliance, content)
    service = parts[0]
    path = f"/{service}"

    # Known compound words that should be split with hyphens
    compound_words = {
        "localaccounts": "local-accounts",
        "globalpolicy": "global-policy",
        "resourcepool": "resource-pool",
        "libraryitem": "library-item",
        "libraryitems": "library-items",
        "locallibrary": "local-library",
        "subscribedlibrary": "subscribed-library",
        "databasestorage": "database-storage",
        "softwarepackages": "software-packages",
        "localfilesystem": "local-filesystem",
        "vmtemplate": "vm-template",
    }

    # Rest are resources/subresources
    for part in parts[1:]:
        # Keep special terms as-is
        if part in ["ipv4", "ipv6", "ntp", "dns", "ssh"]:
            path += f"/{part}"
        # Check for compound words
        elif part in compound_words:
            path += f"/{compound_words[part]}"
        else:
            # Default: keep as-is (most single words don't need hyphens)
            path += f"/{part}"

    return path


# ============================================================================
# Path Operations Extraction
# ============================================================================


def get_path_operations(spec: Dict[str, Any], path: str) -> Dict[str, Dict[str, Any]]:
    """Get all HTTP operations defined for an API path.

    Extracts operation objects for standard HTTP methods from an OpenAPI spec path.

    Args:
        spec: Full OpenAPI spec dictionary
        path: API path (e.g., "/vcenter/datacenter")

    Returns:
        Dictionary mapping HTTP methods (uppercase) to operation objects.
        Returns empty dict if path not found in spec.

    Examples:
        >>> ops = get_path_operations(spec, "/vcenter/datacenter")
        >>> "GET" in ops
        True
        >>> ops["GET"]["operationId"]
        'Datacenter_list'
    """
    if path not in spec.get("paths", {}):
        return {}

    path_obj = spec["paths"][path]
    operations = {}

    for method in ["get", "post", "patch", "put", "delete"]:
        if method in path_obj:
            operations[method.upper()] = path_obj[method]

    return operations


# ============================================================================
# Schema Resolution
# ============================================================================


def resolve_schema_ref(spec: Dict[str, Any], ref: str) -> Dict[str, Any]:
    """Resolve a schema $ref to its definition.

    Handles both OpenAPI 3.0 (#/components/schemas/) and older specs (#/definitions/).

    Args:
        spec: Full OpenAPI spec dictionary
        ref: Reference path (e.g., "#/components/schemas/ResourcePool" or "#/definitions/OldType")

    Returns:
        Schema dictionary or empty dict if not found

    Examples:
        >>> schema = resolve_schema_ref(spec, "#/components/schemas/Datacenter")
        >>> schema["properties"]["name"]
    """
    if ref.startswith("#/components/schemas/"):
        return spec.get("components", {}).get("schemas", {}).get(ref.split("/")[-1], {})
    if ref.startswith("#/definitions/"):
        return spec.get("definitions", {}).get(ref.split("/")[-1], {})
    return {}


def extract_path_params(path: str) -> List[str]:
    """Extract all path parameters from an API path.

    Args:
        path: API path (e.g., "/vcenter/vm/{vm}/hardware/floppy/{floppy}")

    Returns:
        List of parameter names in order (e.g., ["vm", "floppy"])

    Examples:
        >>> extract_path_params("/vcenter/datacenter/{datacenter}")
        ['datacenter']
        >>> extract_path_params("/vcenter/vm/{vm}/hardware/floppy/{floppy}")
        ['vm', 'floppy']
    """
    return re.findall(r"\{([^}]+)\}", path)


def extract_module_constants(content: str, patterns: Dict[str, str]) -> Dict[str, str]:
    r"""Extract constants from module source code using configurable patterns.

    Searches module source code for constant definitions matching the provided
    regex patterns and returns their values.

    Args:
        content: Module source code as string
        patterns: Dict mapping constant names to regex patterns. Each pattern
            should have one capture group for the value.
            e.g., {"MOID": r'MOID_ATTRIBUTE_NAME\s*=\s*"([^"]+)"'}

    Returns:
        Dict mapping constant names to extracted values. Only includes constants
        that were found in the content.

    Examples:
        >>> content = 'MOID_ATTRIBUTE_NAME = "datacenter"\\nLIST_PATH = "/vcenter/datacenter"'
        >>> patterns = {
        ...     "MOID": r'MOID_ATTRIBUTE_NAME\s*=\s*"([^"]+)"',
        ...     "LIST_PATH": r'LIST_PATH\s*=\s*"([^"]+)"'
        ... }
        >>> extract_module_constants(content, patterns)
        {'MOID': 'datacenter', 'LIST_PATH': '/vcenter/datacenter'}
    """
    result = {}
    for name, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            result[name] = match.group(1)
    return result
