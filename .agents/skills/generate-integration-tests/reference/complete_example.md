# Complete Example: vcenter_datacenter Integration Tests

This is a complete, working example showing all files generated for the `vcenter_datacenter` / `vcenter_datacenter_info` module pair.

## Module Analysis Results

- **Module Type**: CRUD module pair
- **Operations**: CREATE, DELETE, GET, LIST (no UPDATE)
- **MOID Attribute**: `datacenter`
- **Resource ID Format**: `datacenter-1001`
- **Test Target Directory**: `tests/integration/targets/vcenter_datacenter/`

## Generated Structure

```
tests/integration/targets/vcenter_datacenter/
├── meta/
│   └── main.yml
├── openapi_spec_mocks/
│   ├── created.json
│   ├── default.json
│   └── list_multiple.json
└── tasks/
    ├── create.yml
    ├── delete.yml
    ├── info.yml
    └── main.yml
```

## File Contents

### meta/main.yml

```yaml
---
dependencies:
  - role: prepare_simulator
    vars:
      prepare_simulator_mock_api_spec_file_dir: vcenter_datacenter/openapi_spec_mocks
```

### tasks/main.yml

```yaml
---
- name: Test vcenter_datacenter modules against MockServer
  environment: "{{ environment_auth_vars }}"
  block:
    - name: Load default API spec expectations
      ansible.builtin.uri:
        url: "{{ mockserver_url }}/mockserver/openapi"
        method: PUT
        status_code: [200, 201]
        body_format: json
        body:
          specUrlOrPayload: "file:/mockserver_specs/default.json"
          operationsAndResponses:
            Vcenter.Datacenter_list: "200"

    - name: Include info tests
      ansible.builtin.include_tasks: info.yml

    - name: Include create tests
      ansible.builtin.include_tasks: create.yml

    - name: Include delete tests
      ansible.builtin.include_tasks: delete.yml
```

### tasks/info.yml

```yaml
---
# ============================================================
# DATACENTER INFO TESTS
# ============================================================
- name: List datacenters (empty)
  vmware.vmware_rest.vcenter_datacenter_info: {}
  register: list_dc_info

- name: Assert empty list
  ansible.builtin.assert:
    that:
      - list_dc_info.datacenters is defined
      - list_dc_info.datacenters | length == 0

- name: Load API spec expectations for get
  ansible.builtin.uri:
    url: "{{ mockserver_url }}/mockserver/openapi"
    method: PUT
    status_code: [200, 201]
    body_format: json
    body:
      specUrlOrPayload: "file:/mockserver_specs/default.json"
      operationsAndResponses:
        Vcenter.Datacenter_get: "200"

- name: Get a datacenter by ID
  vmware.vmware_rest.vcenter_datacenter_info:
    datacenter: datacenter-1001
  register: get_dc_id

- name: Assert datacenter details
  ansible.builtin.assert:
    that:
      - get_dc_id.value is defined
      - get_dc_id.value.datacenter == 'datacenter-1001'
      - get_dc_id.datacenters is defined
      - get_dc_id.datacenters[0].name == 'my_datacenter'
      - get_dc_id.datacenters[0].datastore_folder is defined
      - get_dc_id.datacenters[0].host_folder is defined
      - get_dc_id.datacenters[0].network_folder is defined
      - get_dc_id.datacenters[0].vm_folder is defined

- name: Load API spec expectations for multiple
  ansible.builtin.uri:
    url: "{{ mockserver_url }}/mockserver/openapi"
    method: PUT
    status_code: [200, 201]
    body_format: json
    body:
      specUrlOrPayload: "file:/mockserver_specs/list_multiple.json"
      operationsAndResponses:
        Vcenter.Datacenter_list: "200"
        Vcenter.Datacenter_get: "200"

- name: List datacenters (multi)
  vmware.vmware_rest.vcenter_datacenter_info: {}
  register: list_multi

- name: Check datacenter multi list
  ansible.builtin.assert:
    that:
      - list_multi.value is not defined
      - list_multi.datacenters is defined
      - list_multi.datacenters | length == 2
```

### tasks/create.yml

```yaml
---
# ============================================================
# CREATE DATACENTER TESTS
# ============================================================
- name: Load API spec expectations for create
  ansible.builtin.uri:
    url: "{{ mockserver_url }}/mockserver/openapi"
    method: PUT
    status_code: [200, 201]
    body_format: json
    body:
      specUrlOrPayload: "file:/mockserver_specs/default.json"
      operationsAndResponses:
        Vcenter.Datacenter_create: "200"
        Vcenter.Datacenter_list: "200"

- name: Create a datacenter
  vmware.vmware_rest.vcenter_datacenter:
    name: my_datacenter
    folder: group-d1
    state: present
  register: create_dc

- name: Assert creation success
  ansible.builtin.assert:
    that:
      - create_dc.changed
      - create_dc.id == 'datacenter-1001'

- name: Load API spec expectations for created state
  ansible.builtin.uri:
    url: "{{ mockserver_url }}/mockserver/openapi"
    method: PUT
    status_code: [200, 201]
    body_format: json
    body:
      specUrlOrPayload: "file:/mockserver_specs/created.json"
      operationsAndResponses:
        Vcenter.Datacenter_list: "200"
        Vcenter.Datacenter_get: "200"

- name: Create datacenter again (idempotent)
  vmware.vmware_rest.vcenter_datacenter:
    name: my_datacenter
    folder: group-d1
    state: present
  register: create_dc_again

- name: Assert idempotent
  ansible.builtin.assert:
    that:
      - not create_dc_again.changed
      - create_dc_again.id == 'datacenter-1001'

- name: Load API spec for deleted state (for check mode test)
  ansible.builtin.uri:
    url: "{{ mockserver_url }}/mockserver/openapi"
    method: PUT
    status_code: [200, 201]
    body_format: json
    body:
      specUrlOrPayload: "file:/mockserver_specs/default.json"
      operationsAndResponses:
        Vcenter.Datacenter_list: "200"

- name: Create datacenter in check mode (when doesn't exist)
  vmware.vmware_rest.vcenter_datacenter:
    name: new_datacenter
    folder: group-d1
    state: present
  check_mode: true
  register: create_dc_check

- name: Assert check mode reports change when creating
  ansible.builtin.assert:
    that:
      - create_dc_check.changed

- name: Load API spec back to created state
  ansible.builtin.uri:
    url: "{{ mockserver_url }}/mockserver/openapi"
    method: PUT
    status_code: [200, 201]
    body_format: json
    body:
      specUrlOrPayload: "file:/mockserver_specs/created.json"
      operationsAndResponses:
        Vcenter.Datacenter_list: "200"
        Vcenter.Datacenter_get: "200"

- name: Create existing datacenter in check mode (idempotent)
  vmware.vmware_rest.vcenter_datacenter:
    name: my_datacenter
    folder: group-d1
    state: present
  check_mode: true
  register: create_dc_check_idem

- name: Assert check mode reports no change when already exists
  ansible.builtin.assert:
    that:
      - not create_dc_check_idem.changed
```

### tasks/delete.yml

```yaml
---
# ============================================================
# DELETE DATACENTER TESTS
# ============================================================
- name: Load API spec expectations for delete
  ansible.builtin.uri:
    url: "{{ mockserver_url }}/mockserver/openapi"
    method: PUT
    status_code: [200, 201]
    body_format: json
    body:
      specUrlOrPayload: "file:/mockserver_specs/created.json"
      operationsAndResponses:
        Vcenter.Datacenter_delete: "204"
        Vcenter.Datacenter_get: "200"

- name: Delete a datacenter by ID
  vmware.vmware_rest.vcenter_datacenter:
    datacenter: datacenter-1001
    state: absent
  register: delete_dc

- name: Assert deletion success
  ansible.builtin.assert:
    that:
      - delete_dc.changed
      - delete_dc.id == 'datacenter-1001'

- name: Load API spec expectations for empty state
  ansible.builtin.uri:
    url: "{{ mockserver_url }}/mockserver/openapi"
    method: PUT
    status_code: [200, 201]
    body_format: json
    body:
      specUrlOrPayload: "file:/mockserver_specs/default.json"
      operationsAndResponses:
        Vcenter.Datacenter_list: "200"

- name: Delete datacenter again (idempotent)
  vmware.vmware_rest.vcenter_datacenter:
    name: my_datacenter
    folder: group-d1
    state: absent
  register: delete_dc_again

- name: Assert idempotent delete
  ansible.builtin.assert:
    that:
      - not delete_dc_again.changed

- name: Load API spec for final delete test
  ansible.builtin.uri:
    url: "{{ mockserver_url }}/mockserver/openapi"
    method: PUT
    status_code: [200, 201]
    body_format: json
    body:
      specUrlOrPayload: "file:/mockserver_specs/created.json"
      operationsAndResponses:
        Vcenter.Datacenter_get: "200"

- name: Delete datacenter in check mode (when exists)
  vmware.vmware_rest.vcenter_datacenter:
    datacenter: datacenter-1001
    state: absent
  check_mode: true
  register: delete_dc_check

- name: Assert check mode reports change when deleting
  ansible.builtin.assert:
    that:
      - delete_dc_check.changed

- name: Load API spec for empty state
  ansible.builtin.uri:
    url: "{{ mockserver_url }}/mockserver/openapi"
    method: PUT
    status_code: [200, 201]
    body_format: json
    body:
      specUrlOrPayload: "file:/mockserver_specs/default.json"
      operationsAndResponses:
        Vcenter.Datacenter_list: "200"

- name: Delete non-existent datacenter in check mode (idempotent)
  vmware.vmware_rest.vcenter_datacenter:
    datacenter: datacenter-1001
    state: absent
  check_mode: true
  register: delete_dc_check_idem

- name: Assert check mode reports no change when already deleted
  ansible.builtin.assert:
    that:
      - not delete_dc_check_idem.changed

- name: Load API spec with datacenter present for final test
  ansible.builtin.uri:
    url: "{{ mockserver_url }}/mockserver/openapi"
    method: PUT
    status_code: [200, 201]
    body_format: json
    body:
      specUrlOrPayload: "file:/mockserver_specs/created.json"
      operationsAndResponses:
        Vcenter.Datacenter_list: "200"
        Vcenter.Datacenter_get: "200"
        Vcenter.Datacenter_delete: "204"

- name: Delete datacenter by name
  vmware.vmware_rest.vcenter_datacenter:
    name: my_datacenter
    folder: group-d1
    state: absent
  register: delete_by_name

- name: Assert delete by name succeeds
  ansible.builtin.assert:
    that:
      - delete_by_name.changed
```

## Running the Tests

```bash
# Generate mocks
python content_generation/generate_openapi_mocks.py vcenter_datacenter

# Run tests
make integration CLI_ARGS=-vvvv INTEGRATION_TARGETS=vcenter_datacenter
```

## Test Results

```
PLAY RECAP *********************************************************************
testhost                   : ok=45   changed=7    unreachable=0    failed=0
```

## Test Coverage Summary

### Info Tests (3 test scenarios)
1. ✅ List when empty
2. ✅ Get by ID with field validation
3. ✅ List multiple items

### Create Tests (4 test scenarios)
1. ✅ Initial creation
2. ✅ Idempotent creation
3. ✅ Check mode when resource doesn't exist
4. ✅ Check mode when resource exists

### Delete Tests (5 test scenarios)
1. ✅ Delete by ID
2. ✅ Idempotent deletion
3. ✅ Check mode when resource exists
4. ✅ Check mode when resource doesn't exist
5. ✅ Delete by name

**Total**: 12 test scenarios, 45 Ansible tasks, ~48 seconds runtime

## Key Points

- **Concise but comprehensive**: 12 scenarios cover the essential behaviors
- **Idempotency validated**: Every state-changing operation tested twice
- **Check mode coverage**: Both positive and negative scenarios tested
- **Specific assertions**: Check actual values, not just presence
- **Mock state management**: Explicit state transitions before each test
- **No edge cases**: Focus on happy path and basic error scenarios
- **Fast execution**: Complete test suite runs in under a minute
