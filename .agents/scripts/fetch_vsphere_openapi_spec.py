#!/usr/bin/env python3
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Download vSphere OpenAPI specs from Broadcom/VCF sources and place them in config/."""

from __future__ import annotations

import argparse
import io
import json
import sys
import zipfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]


REPO_ROOT = Path(__file__).resolve().parents[2]
API_SPECS_DIR = REPO_ROOT / "config" / "api_specifications"
VERSION_MAP_PATH = REPO_ROOT / ".agents" / "references" / "vcf-spec-versions.yaml"
GITHUB_API_TAGS = "https://api.github.com/repos/vmware/vcf-api-specs/tags?per_page=20"

OPENAPI_PREFIX = "specifications/vsphere/openapi/"


def _load_version_map() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML is required. Install with: pip install pyyaml")
    with VERSION_MAP_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _http_get(url: str) -> bytes:
    request = Request(
        url,
        headers={"User-Agent": "vmware.vmware_rest-spec-fetcher/1.0"},
    )
    with urlopen(request) as response:
        return response.read()


def _resolve_vcf_tag(vsphere_major: str, version_map: dict) -> dict:
    major_key = str(vsphere_major)
    mapping = version_map["vsphere_major_versions"].get(major_key)
    if mapping is None:
        supported = ", ".join(sorted(version_map["vsphere_major_versions"]))
        raise ValueError(
            f"Unsupported vSphere major version {major_key!r}. Supported: {supported}"
        )
    if (
        mapping.get("available_on_broadcom") is False
        or mapping.get("fallback") == "vmsgen"
    ):
        raise ValueError(
            f"vSphere {major_key}.x specs are not published on Broadcom. "
            f"Use vmsgen against a live vCenter (see docs/development.md)."
        )
    return mapping


def _find_latest_vcf_tag_for_major(vsphere_major: str) -> str | None:
    try:
        payload = json.loads(_http_get(GITHUB_API_TAGS).decode("utf-8"))
    except (HTTPError, URLError, json.JSONDecodeError):
        return None

    prefix = f"{vsphere_major}."
    matching = [tag["name"] for tag in payload if tag["name"].startswith(prefix)]
    if not matching:
        return None
    return max(matching, key=lambda name: [int(part) for part in name.split(".")])


def _download_vcf_zipball(vcf_tag: str) -> bytes:
    url = f"https://api.github.com/repos/vmware/vcf-api-specs/zipball/{vcf_tag}"
    return _http_get(url)


def _list_openapi_yaml_entries(zip_bytes: bytes) -> list[tuple[str, str]]:
    """Return (archive_path, relative_output_path) for each vsphere openapi YAML file."""
    entries: list[tuple[str, str]] = []
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        for name in archive.namelist():
            marker = "/specifications/vsphere/openapi/"
            index = name.find(marker)
            if index == -1:
                continue
            relative = name[index + len(marker) :]
            if not relative.endswith((".yaml", ".yml")):
                continue
            entries.append((name, relative))
    entries.sort(key=lambda item: item[1])
    if not entries:
        raise FileNotFoundError(
            "No YAML files found under specifications/vsphere/openapi/ in archive"
        )
    return entries


def _yaml_relative_to_json(relative_yaml_path: str) -> str:
    path = Path(relative_yaml_path)
    return str(path.with_suffix(".json"))


def _read_spec_version(zip_bytes: bytes, entries: list[tuple[str, str]]) -> str | None:
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        for archive_path, relative in entries:
            if relative.endswith(("vcenter.yaml", "vcenter.yml")):
                spec = yaml.safe_load(archive.read(archive_path))
                version = spec.get("info", {}).get("version")
                if version:
                    return str(version)
    return None


def _normalize_output_version(spec_version: str) -> str:
    parts = spec_version.split(".")
    if len(parts) >= 3:
        return ".".join(parts[:3])
    return spec_version


def _write_json_spec(target: Path, spec: dict) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(spec, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def _remove_yaml_counterpart(output_dir: Path, relative_yaml_path: str) -> None:
    yaml_path = output_dir / relative_yaml_path
    if yaml_path.exists():
        yaml_path.unlink()


def _install_json_specs(
    zip_bytes: bytes,
    output_dir: Path,
    entries: list[tuple[str, str]],
) -> list[str]:
    """Convert YAML specs from the archive to JSON and remove YAML counterparts."""
    written: list[str] = []
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        for archive_path, relative_yaml in entries:
            spec = yaml.safe_load(archive.read(archive_path))
            relative_json = _yaml_relative_to_json(relative_yaml)
            target = output_dir / relative_json
            _write_json_spec(target, spec)
            _remove_yaml_counterpart(output_dir, relative_yaml)
            written.append(relative_json)
    return written


def fetch_and_install(
    vsphere_major: str,
    output_version: str | None = None,
    dry_run: bool = False,
) -> dict:
    version_map = _load_version_map()
    mapping = _resolve_vcf_tag(vsphere_major, version_map)

    vcf_tag = mapping.get("vcf_tag")
    latest = _find_latest_vcf_tag_for_major(vsphere_major)
    if latest and latest != vcf_tag:
        vcf_tag = latest

    zip_bytes = _download_vcf_zipball(vcf_tag)
    entries = _list_openapi_yaml_entries(zip_bytes)

    spec_version = _read_spec_version(zip_bytes, entries)
    target_version = (
        output_version
        or (spec_version and _normalize_output_version(spec_version))
        or mapping.get("output_directory")
        or _normalize_output_version(vcf_tag)
    )
    output_dir = API_SPECS_DIR / target_version

    result = {
        "vsphere_major": vsphere_major,
        "vcf_tag": vcf_tag,
        "spec_version": spec_version,
        "output_directory": str(output_dir.relative_to(REPO_ROOT)),
        "format": "json",
        "source_format": "yaml",
        "installed_files": [
            _yaml_relative_to_json(relative) for _, relative in entries
        ],
        "dry_run": dry_run,
    }

    if dry_run:
        return result

    output_dir.mkdir(parents=True, exist_ok=True)
    result["installed_files"] = _install_json_specs(zip_bytes, output_dir, entries)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch vSphere OpenAPI specs from Broadcom/VCF sources."
    )
    parser.add_argument(
        "--vsphere-major",
        required=True,
        help="Major vSphere version (e.g. 9). Determines which VCF API spec release to download.",
    )
    parser.add_argument(
        "--output-version",
        help="Target directory name under config/api_specifications/ (e.g. 9.1.0). "
        "Defaults to the spec info.version from automation/vcenter.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve versions and report planned output without writing files.",
    )
    args = parser.parse_args()

    try:
        result = fetch_and_install(
            vsphere_major=args.vsphere_major,
            output_version=args.output_version,
            dry_run=args.dry_run,
        )
    except (ValueError, FileNotFoundError, HTTPError, URLError, RuntimeError) as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
