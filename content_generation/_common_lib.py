#!/usr/bin/env python
"""
Common utilities shared by all content generation scripts.

This library provides basic project structure discovery and common resources
that are used across all generation, classification, and spec-fetching scripts.

Usage:
    from _common_lib import get_repo_root, get_api_specs_dir, load_version_map
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict
from urllib.request import Request, urlopen

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Common constants
APPLICATION_JSON = "application/json"


def get_repo_root() -> Path:
    """Get the repository root directory.

    Returns:
        Path object pointing to repository root (parent of content_generation/)
    """
    return Path(__file__).resolve().parents[1]


def get_api_specs_dir() -> Path:
    """Get the API specifications directory.

    Returns:
        Path to content_generation/api_specs/
    """
    return get_repo_root() / "content_generation" / "api_specs"


def get_modules_dir() -> Path:
    """Get the plugins/modules directory.

    Returns:
        Path to plugins/modules/
    """
    return get_repo_root() / "plugins" / "modules"


def load_version_map() -> Dict[str, Any]:
    """Load the vSphere to VCF version mapping.

    Returns:
        Dictionary with version mapping data

    Raises:
        RuntimeError: If PyYAML is not installed
        FileNotFoundError: If version map file doesn't exist
    """
    if not HAS_YAML:
        raise RuntimeError("PyYAML is required. Install with: pip install pyyaml")

    version_map_path = (
        get_repo_root() / ".agents" / "references" / "vcf-spec-versions.yaml"
    )

    if not version_map_path.exists():
        raise FileNotFoundError(f"Version map not found: {version_map_path}")

    with version_map_path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def http_get(url: str, user_agent: str = "vmware.vmware_rest/1.0") -> bytes:
    """Make an HTTP GET request.

    Args:
        url: URL to fetch
        user_agent: User agent string for the request

    Returns:
        Response body as bytes

    Raises:
        URLError: If the request fails
    """
    request = Request(url, headers={"User-Agent": user_agent})
    with urlopen(request) as response:
        return response.read()


def normalize_api_version(version: str) -> str:
    """Normalize an API version string to major.minor.patch format.

    Args:
        version: Version string (e.g., "9.1.0.0" or "9.1")

    Returns:
        Normalized version (e.g., "9.1.0")

    Examples:
        >>> normalize_api_version("9.1.0.0")
        '9.1.0'
        >>> normalize_api_version("9.1")
        '9.1.0'
    """
    parts = version.split(".")

    # Ensure we have at least 3 parts
    while len(parts) < 3:
        parts.append("0")

    # Return only major.minor.patch
    return ".".join(parts[:3])


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case.

    Args:
        name: CamelCase or camelCase string

    Returns:
        snake_case string

    Examples:
        >>> camel_to_snake("ResourcePool")
        'resource_pool'
        >>> camel_to_snake("datacenter")
        'datacenter'
    """
    result = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    return result


def get_spec_path(spec_version: str, spec_file: str = "vcenter.json") -> Path:
    """Get the path to an OpenAPI spec file for a given version.

    For vSphere 9.0+, uses automation/vcenter.json structure.
    For earlier versions, uses the spec_file parameter.

    Args:
        spec_version: Version string (e.g., "8.0.3", "9.1.0")
        spec_file: Spec file name for pre-9.0 versions

    Returns:
        Path to the spec file

    Examples:
        >>> get_spec_path("9.1.0")
        PosixPath('.../content_generation/api_specs/9.1.0/automation/vcenter.json')
        >>> get_spec_path("8.0.3", "appliance.json")
        PosixPath('.../content_generation/api_specs/8.0.3/appliance.json')
    """
    spec_dir = get_api_specs_dir()
    major_version = int(spec_version.split(".")[0])

    if major_version >= 9:
        return spec_dir / spec_version / "automation" / "vcenter.json"
    else:
        return spec_dir / spec_version / spec_file
