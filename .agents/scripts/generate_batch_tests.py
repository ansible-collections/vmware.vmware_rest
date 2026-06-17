#!/usr/bin/env python3
"""Generate unit tests and integration scaffolds for vmware.vmware_rest batches."""

from __future__ import annotations

import ast
import json
import re
import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MODULES_DIR = REPO / "plugins/modules"
UNIT_DIR = REPO / "tests/unit/plugins/modules"
INT_DIR = REPO / "tests/integration/targets"

CONNECTION_PARAMS = """CONNECTION_PARAMS = {
    "vcenter_hostname": "vcenter.example.com",
    "vcenter_username": "admin",
    "vcenter_password": "secret",
    "vcenter_port": None,
    "vcenter_validate_certs": False,
    "vcenter_rest_log_file": None,
    "session_timeout": None,
}"""

UNIT_HEADER = """# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.module_utils._client import (
    Response,
)
from ansible_collections.vmware.vmware_rest.plugins.modules import (
    {module_name} as module_under_test,
)


class AnsibleExitJson(Exception):
    def __init__(self, kwargs):
        self.kwargs = kwargs


def exit_json(*args, **kwargs):
    if args:
        kwargs.update(args[0])
    raise AnsibleExitJson(kwargs)


def _response(status, body):
    data = json.dumps(body).encode("utf-8") if body is not None else b""
    return Response(status, data)


{connection_params}


@pytest.fixture
def mock_client():
    return MagicMock()


def set_module_args(args):
    return {{**CONNECTION_PARAMS, **args}}
"""


def load_batches():
    import yaml

    with open(REPO / "config/modules.yaml") as f:
        expected = [list(x.keys())[0] for x in yaml.safe_load(f)]
    batches = []
    i = 0
    while i < len(expected):
        m = expected[i]
        batch = [m]
        if m.endswith("_info") and i + 1 < len(expected) and expected[i + 1] == m[:-5]:
            batch.append(expected[i + 1])
            i += 2
        else:
            i += 1
        batches.append(batch)
    return batches


def target_name(batch):
    if len(batch) == 2 and batch[0].endswith("_info"):
        return batch[0][:-5]
    m = batch[0]
    return m[:-5] if m.endswith("_info") else m


def extract_paths(module_path: Path) -> dict[str, str]:
    text = module_path.read_text()
    paths = {}
    for m in re.finditer(r'^([A-Z_]+PATH)\s*=\s*"([^"]+)"', text, re.M):
        paths[m.group(1)] = m.group(2)
    return paths


def extract_class_name(module_path: Path) -> str:
    text = module_path.read_text()
    for pattern in (
        r"class (VmwareRest\w+Module)",
        r"class (VmwareRest\w+)",
    ):
        m = re.search(pattern, text)
        if m:
            return m.group(1)
    return "VmwareRestInfoModule"


def extract_return_sample(module_path: Path):
    text = module_path.read_text()
    m = re.search(r'RETURN = r"""(.*?)"""', text, re.S)
    if not m:
        return {"value": "sample"}
    block = m.group(1)
    sm = re.search(r"sample:\s*\n((?:    .+\n)+)", block)
    if not sm:
        sm = re.search(r"sample:\s*(.+)", block)
        if sm:
            val = sm.group(1).strip()
            if val in ("green", "yellow", "red", "orange"):
                return val
            return {"value": val}
        return {}
    lines = sm.group(1).splitlines()
    yaml_text = "\n".join(line[4:] for line in lines if line.startswith("    "))
    import yaml

    try:
        return yaml.safe_load(yaml_text)
    except Exception:
        return {"configured": True}


def has_existing_unit(module_name: str) -> bool:
    return (UNIT_DIR / f"test_{module_name}.py").exists()


def has_existing_integration(target: str) -> bool:
    return (INT_DIR / target / "tasks/main.yml").exists()


def generate_info_unit_test(
    module_name: str, path: str, class_name: str, sample, required_params: dict
):
    sample_repr = repr(sample)
    params_setup = repr({**required_params})
    not_found_expected = (
        '{"value": ""}'
        if isinstance(sample, str)
        else (
            '{"value": None}'
            if sample is not None and not isinstance(sample, list)
            else '{"value": []}'
        )
    )
    if module_name.endswith("_info") and "LIST_PATH" in path:
        return None  # skip complex list modules in auto-gen

    api_path = path if isinstance(path, str) else path.get("get", path.get("list", ""))

    return UNIT_HEADER.format(
        module_name=module_name, connection_params=CONNECTION_PARAMS
    ) + textwrap.dedent(
        f"""

        API_PATH = "{api_path}"
        SAMPLE_BODY = {sample_repr}


        @patch.object(module_under_test, "AnsibleModule")
        @patch.object(module_under_test.{class_name}, "_create_client")
        def test_get_success(mock_create_client, mock_ansible_module, mock_client):
            mock_create_client.return_value = mock_client
            mock_module = MagicMock()
            mock_ansible_module.return_value = mock_module
            mock_module.params = set_module_args({params_setup})
            mock_module.exit_json.side_effect = exit_json

            mock_client.get.return_value = _response(200, SAMPLE_BODY)

            with pytest.raises(AnsibleExitJson) as exc:
                module_under_test.main()

            mock_client.get.assert_called_once()
            assert "value" in exc.value.kwargs


        @patch.object(module_under_test, "AnsibleModule")
        @patch.object(module_under_test.{class_name}, "_create_client")
        def test_get_not_found(mock_create_client, mock_ansible_module, mock_client):
            mock_create_client.return_value = mock_client
            mock_module = MagicMock()
            mock_ansible_module.return_value = mock_module
            mock_module.params = set_module_args({params_setup})
            mock_module.exit_json.side_effect = exit_json

            mock_client.get.return_value = _response(404, None)

            with pytest.raises(AnsibleExitJson) as exc:
                module_under_test.main()

            mock_client.get.assert_called_once()
        """
    )


def generate_integration_info(target: str, module_name: str, operation_id: str = "get"):
    meta = f"""---
dependencies:
  - role: prepare_simulator
    vars:
      prepare_simulator_mock_api_spec_file_dir: {target}/openapi_spec_mocks
"""
    mock_spec = {
        "openapi": "3.0.3",
        "info": {"title": f"{target} Mock", "version": "9.1.0.0"},
        "servers": [
            {
                "url": "https://{host}/api",
                "variables": {"host": {"default": "localhost"}},
            }
        ],
        "paths": {},
    }
    paths = extract_paths(MODULES_DIR / f"{module_name}.py")
    api_path = list(paths.values())[0] if paths else f"/{target.replace('_', '/')}"
    mock_spec["paths"][api_path] = {
        "get": {
            "operationId": operation_id,
            "responses": {
                "200": {
                    "description": "ok",
                    "content": {
                        "application/json": {
                            "schema": {"type": "object"},
                            "example": {"status": "ok"},
                        }
                    },
                }
            },
        }
    }
    tasks = f"""---
- name: Test {module_name} against MockServer
  environment: "{{{{ environment_auth_vars }}}}"
  block:
    - name: Load API spec expectations
      ansible.builtin.uri:
        url: http://localhost:1080/mockserver/openapi
        method: PUT
        status_code: [200, 201]
        body_format: json
        body:
          specUrlOrPayload: "file:/mockserver_specs/default.json"
          operationsAndResponses:
            {operation_id}: "200"

    - name: Invoke {module_name}
      vmware.vmware_rest.{module_name}:
      register: result

    - name: Assert module returned value
      ansible.builtin.assert:
        that:
          - result.value is defined
"""
    return meta, json.dumps(mock_spec, indent=2), tasks


def main():
    batches = load_batches()
    skip = {25, 35}
    generated_unit = []
    generated_int = []
    skipped = []

    for idx, batch in enumerate(batches, 1):
        if idx < 19 or idx > 71 or idx in skip:
            continue
        tn = target_name(batch)
        if has_existing_integration(tn) and all(has_existing_unit(m) for m in batch):
            skipped.append(idx)
            continue

        for module_name in batch:
            if has_existing_unit(module_name):
                continue
            mod_path = MODULES_DIR / f"{module_name}.py"
            if not mod_path.exists():
                continue
            paths = extract_paths(mod_path)
            class_name = extract_class_name(mod_path)
            sample = extract_return_sample(mod_path)
            if module_name.endswith("_info"):
                api_path = (
                    paths.get("LIST_PATH")
                    or paths.get("PATH")
                    or paths.get("SERVICE_PATH")
                    or paths.get("SHUTDOWN_PATH")
                    or paths.get("STORAGE_PATH")
                    or paths.get("SYSTEM_TIME_PATH")
                    or paths.get("SYSTEM_VERSION_PATH")
                    or paths.get("UPDATE_PATH")
                    or list(paths.values())[0]
                    if paths
                    else ""
                )
                if "{service}" in api_path:
                    api_path = api_path.replace("{service}", "ntpd")
                if "{interface_name}" in api_path:
                    api_path = api_path.replace("{interface_name}", "nic0")
                content = generate_info_unit_test(
                    module_name, api_path, class_name, sample, {}
                )
                if content:
                    out = UNIT_DIR / f"test_{module_name}.py"
                    out.write_text(content)
                    generated_unit.append(str(out))

        if not has_existing_integration(tn):
            info_mod = batch[0] if batch[0].endswith("_info") else batch[0]
            op = (
                "list"
                if "LIST_PATH" in extract_paths(MODULES_DIR / f"{info_mod}.py")
                else "get"
            )
            meta, spec, tasks = generate_integration_info(tn, info_mod, op)
            (INT_DIR / tn).mkdir(parents=True, exist_ok=True)
            (INT_DIR / tn / "meta").mkdir(exist_ok=True)
            (INT_DIR / tn / "tasks").mkdir(exist_ok=True)
            (INT_DIR / tn / "openapi_spec_mocks").mkdir(exist_ok=True)
            (INT_DIR / tn / "meta/main.yml").write_text(meta)
            (INT_DIR / tn / "openapi_spec_mocks/default.json").write_text(spec)
            (INT_DIR / tn / "tasks/main.yml").write_text(tasks)
            generated_int.append(tn)

    print(f"Generated {len(generated_unit)} unit tests")
    for p in generated_unit:
        print(f"  unit: {p}")
    print(f"Generated {len(generated_int)} integration targets")
    for t in generated_int:
        print(f"  int: {t}")
    print(f"Skipped complete batches: {skipped}")


if __name__ == "__main__":
    main()
