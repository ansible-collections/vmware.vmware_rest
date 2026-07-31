# Generate Integration Tests for VMware REST Modules

## Purpose

Generate complete integration test suites for vmware.vmware_rest Ansible modules. Integration tests validate module behavior against a MockServer API simulator, focusing on idempotency, check mode, and basic input/output expectations.

## Scope

Integration tests should be **meaningful but short**. They validate:
- **Idempotency**: Operations don't change when repeated
- **Check mode**: Modules correctly report changes without applying them
- **Basic I/O**: Modules accept expected parameters and return expected results
- **State transitions**: Modules correctly handle different API states

**DO NOT** test in integration tests:
- Edge cases (handled by unit tests)
- Complex error scenarios (handled by unit tests)
- Parameter validation (handled by unit tests)
- Every possible parameter combination (handled by unit tests)

## When to Use This Skill

Use this skill when asked to generate integration tests for a module or module pair (e.g., `vcenter_datacenter` and `vcenter_datacenter_info`).

## Prerequisites

- Module(s) must exist in `plugins/modules/`
- The `generate_openapi_mocks.py` script must be available at `content_generation/generate_openapi_mocks.py`
- The `prepare_simulator` role must be available in the test infrastructure

## Workflow

### Step 1: Analyze the Module(s)

Read the module file(s) to understand:

1. **Module Type**:
   - CRUD module (has state parameter, supports create/delete)
   - Info module (read-only, ends with `_info`)

2. **API Operations** - Look for these OperationConfig definitions:
   - `LIST_OPERATION` → LIST operation supported
   - `GET_OPERATION` → GET operation supported
   - `CREATE_OPERATION` → CREATE operation supported
   - `UPDATE_OPERATION` → UPDATE operation supported
   - `DELETE_OPERATION` → DELETE operation supported

3. **Module Constants**:
   - `MOID_PARAMETER_HINTS` - List of path parameters (last one is typically the main MOID)
   - `LIST_ENDPOINT` - API path for list operations (e.g., `/vcenter/resource-pool`)
   - `ITEM_ENDPOINT` - API path for item operations (e.g., `/vcenter/resource-pool/{resource_pool}`)

4. **Module Parameters** - From `create_module_argument_spec()`:
   - Required parameters
   - Identifying parameters (name, folder, etc.)
   - Resource-specific parameters

### Step 2: Generate OpenAPI Mocks

Run the mock generator script:

```bash
python content_generation/generate_openapi_mocks.py <module_name> [output_dir]
```

Example:
```bash
python content_generation/generate_openapi_mocks.py vcenter_datacenter
```

This generates mock specification files in `tests/integration/targets/<module_name>/openapi_spec_mocks/`:
- `default.json` - Empty state (no resources exist)
- `created.json` - Resource exists (if CREATE supported)
- `list_multiple.json` - Multiple resources exist (if LIST supported)
- `updated.json` - Updated resource state (if UPDATE supported)

**Note**: If the module name ends with `_info`, the script automatically strips it for the target directory name.

### Step 2.5: Understand updated.json Customization

**IMPORTANT**: The generated `updated.json` is a baseline (identical to `created.json`) and will need manual customization after you write your update tests.

The script cannot know what fields your tests will update. The workflow is:
1. Generate initial mocks (including baseline `updated.json`)
2. Write your integration tests (defining what fields to update)
3. **Manually edit `updated.json`** to reflect the values your UPDATE operation sets
4. Re-run tests to verify idempotency

**Example**: If your update test sets:
```yaml
cpu_allocation:
  reservation: 2000
  limit: 8000
  shares:
    level: HIGH
```

Then `updated.json` must return these same values in the GET response for idempotency tests to pass.

**Why this matters**: When the module does an idempotent UPDATE, it:
1. Reads current state via GET (returns values from `updated.json`)
2. Compares with desired state (from test parameters)
3. If they match → `changed=false` ✓
4. If they differ → `changed=true` ✗ (test fails)

### Step 3: Create Test Directory Structure

Create the integration test target directory:

```
tests/integration/targets/<module_name>/
├── meta/
│   └── main.yml
├── tasks/
│   ├── main.yml
│   ├── info.yml
│   ├── create.yml      # If CREATE operation exists
│   ├── update.yml      # If UPDATE operation exists
│   └── delete.yml      # If DELETE operation exists
└── openapi_spec_mocks/ # Generated in Step 2
    ├── default.json
    ├── created.json
    ├── list_multiple.json
    └── updated.json
```

**Important**: Use the base module name (without `_info`) for the target directory. Both `vcenter_datacenter` and `vcenter_datacenter_info` tests go in `tests/integration/targets/vcenter_datacenter/`.

### Step 4: Create meta/main.yml

This file declares the dependency on the simulator role:

```yaml
---
dependencies:
  - role: prepare_simulator
    vars:
      prepare_simulator_mock_api_spec_file_dir: <module_name>/openapi_spec_mocks
```

Replace `<module_name>` with the target directory name.

### Step 5: Create tasks/main.yml

This is the orchestrator that sets up the initial mock state and includes other task files:

```yaml
---
- name: Test <module_name> modules against MockServer
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
            <OperationId>_list: "200"  # Replace with actual operation ID

    # Include test files based on supported operations
    - name: Include info tests
      ansible.builtin.include_tasks: info.yml

    - name: Include create tests
      ansible.builtin.include_tasks: create.yml
      # Only include if CREATE operation is supported

    - name: Include update tests
      ansible.builtin.include_tasks: update.yml
      # Only include if UPDATE operation is supported

    - name: Include delete tests
      ansible.builtin.include_tasks: delete.yml
      # Only include if DELETE operation is supported
```

### Step 6: Create tasks/info.yml

Tests for the info module (LIST and GET operations). See `reference/info_tests_pattern.yml` for the standard pattern.

**Key tests**:
1. List when empty
2. Get by ID
3. List multiple items

Each test should:
- Load appropriate mock spec state before the test
- Execute the module operation
- Assert expected results (check specific fields, not just presence)

### Step 7: Create tasks/create.yml (if CREATE supported)

Tests for CREATE operations. See `reference/create_tests_pattern.yml` for the standard pattern.

**Key tests**:
1. Initial creation (verify `changed=true` and ID returned)
2. Idempotent creation (verify `changed=false` when repeated)
3. Check mode when resource doesn't exist (verify `changed=true`)
4. Check mode when resource exists (verify `changed=false`)

**Mock state transitions**:
- Start with `default.json` (empty)
- Switch to `created.json` after first create
- Switch back to `default.json` for check mode tests

### Step 8: Create tasks/update.yml (if UPDATE supported)

Tests for UPDATE operations. See `reference/update_tests_pattern.yml` for the standard pattern.

**Key tests**:
1. Initial update (verify `changed=true`)
2. Idempotent update (verify `changed=false` when repeated)
3. Check mode tests

### Step 9: Create tasks/delete.yml (if DELETE supported)

Tests for DELETE operations. See `reference/delete_tests_pattern.yml` for the standard pattern.

**Key tests**:
1. Delete by ID (verify `changed=true`)
2. Delete by name (if name-based lookup supported)
3. Idempotent deletion (verify `changed=false` when already deleted)
4. Check mode when resource exists (verify `changed=true`)
5. Check mode when resource doesn't exist (verify `changed=false`)

**Mock state transitions**:
- Start with `created.json` (resource exists)
- Switch to `default.json` after deletion
- Switch back and forth for check mode tests

### Step 10: Run and Validate Tests ⚠️ MANDATORY

**CRITICAL**: This step is NOT optional. You MUST run the integration tests and iterate until they pass. Tests have uncovered critical bugs that would otherwise go undetected.

Execute the integration tests:

```bash
make integration CLI_ARGS=-vvvv INTEGRATION_TARGETS=<module_name>
```

**Success criteria**:
- All tasks pass (ok)
- No failures
- Changed counts match expectations

**When tests fail** (iterate until resolved):

1. **Review the failure output carefully** - Note the exact assertion or module error

2. **Categorize the failure**:
   - **Test issue**: Wrong assertions, incorrect mock state, missing mock operations
   - **Mock customization needed**: `updated.json` doesn't reflect test's UPDATE values
   - **Module bug**: Module code has actual defects

3. **Fix test issues**:
   - Incorrect assertions → Update test expectations
   - Wrong mock state loaded → Check `operationsAndResponses` in URI tasks
   - Missing `GET` operation → Add to `operationsAndResponses`
   - Idempotency fails → Customize `updated.json` (see Step 2.5)

4. **Report module bugs to user** with:
   - The specific test that failed
   - The expected behavior
   - The actual behavior
   - The module code location if identified
   - **DO NOT modify module code yourself** - report for user to fix

5. **Re-run tests after each fix** until all pass

**Example bugs found during vcenter_resourcepool testing**:
- `build_path()` not assigning replaced path (all GET/UPDATE/DELETE operations failed)
- `_list_resource_details()` returning Response objects instead of JSON
- Incorrect `build_query()` parameter usage
- `http_operation` vs `http_method` typo

Without running tests, these critical bugs would have shipped!

## Test Writing Guidelines

### MockServer State Management

The MockServer maintains the current API state. Tests must explicitly load the appropriate mock spec before each operation.

**IMPORTANT — Reset Before Each Expectation Load**: MockServer 7.x treats `PUT /mockserver/openapi` as **additive** — each call adds expectations without clearing previous ones. This means expectations from earlier test steps bleed into later ones, causing non-deterministic failures (e.g., an "empty list" expectation competing with a "resource exists" expectation).

**You must reset MockServer before every expectation load** (except the first one in `main.yml`, since MockServer has just started). Use the `prepare_simulator` role with `prepare_simulator_reset: true`:

```yaml
- name: Reset before <context> expectations
  ansible.builtin.include_role:
    name: prepare_simulator
  vars:
    prepare_simulator_reset: true

- name: Load API spec expectations for <state>
  ansible.builtin.uri:
    url: "{{ mockserver_url }}/mockserver/openapi"
    method: PUT
    status_code: [200, 201]
    body_format: json
    body:
      specUrlOrPayload: "file:/mockserver_specs/<spec_file>.json"
      operationsAndResponses:
        <OperationId>_<operation>: "<response_code>"
```

The reset clears all expectations and re-establishes the session authentication expectation (required for modules to connect).

**Common patterns**:
- Load `default.json` before testing creation of non-existent resource
- Load `created.json` before testing idempotent operations
- Switch specs to simulate state changes
- Always reset before switching specs to avoid expectation conflicts

### Assertion Patterns

**Good assertions** - Check specific values:
```yaml
- name: Assert datacenter details
  ansible.builtin.assert:
    that:
      - get_dc_id.value.datacenter == 'datacenter-1001'
      - get_dc_id.datacenters[0].name == 'my_datacenter'
      - get_dc_id.datacenters[0].datastore_folder == 'group-s5'
```

**Weak assertions** - Only check presence:
```yaml
# Avoid this - too generic
- ansible.builtin.assert:
    that:
      - result.value is defined
```

### Check Mode Testing

Always test both scenarios for check mode:
1. When the operation would cause a change
2. When the operation would not cause a change

Example:
```yaml
# Check mode - would create (resource doesn't exist)
- name: Create resource in check mode (when doesn't exist)
  vmware.vmware_rest.vcenter_datacenter:
    name: new_datacenter
    folder: group-d1
    state: present
  check_mode: true
  register: create_check

- name: Assert check mode reports change when creating
  ansible.builtin.assert:
    that:
      - create_check.changed

# Check mode - would not create (resource exists)
- name: Create resource in check mode (when exists)
  vmware.vmware_rest.vcenter_datacenter:
    name: my_datacenter
    folder: group-d1
    state: present
  check_mode: true
  register: create_check_idem

- name: Assert check mode reports no change when already exists
  ansible.builtin.assert:
    that:
      - not create_check_idem.changed
```

## Operation ID Format

vSphere APIs use the format: `Vcenter.ResourceName_operation`

Examples:
- `Vcenter.Datacenter_list`
- `Vcenter.Datacenter_get`
- `Vcenter.Datacenter_create`
- `Vcenter.Datacenter_delete`

For nested resources like `/vcenter/vm/{vm}/tools/installer`:
- `Vcenter.Vm.Tools.Installer_get`

The mock generator automatically determines these from the module's `LIST_PATH`.

## Common Patterns

### Testing List Operations

```yaml
- name: List resources (empty)
  vmware.vmware_rest.<module_name>_info: {}
  register: list_result

- name: Assert empty list
  ansible.builtin.assert:
    that:
      - list_result.<resource_plural> is defined
      - list_result.<resource_plural> | length == 0
```

### Testing Get Operations

```yaml
- name: Get resource by ID
  vmware.vmware_rest.<module_name>_info:
    <moid_attribute>: <resource_id>
  register: get_result

- name: Assert resource details
  ansible.builtin.assert:
    that:
      - get_result.value is defined
      - get_result.value.<moid_attribute> == '<resource_id>'
      - get_result.<resource_plural>[0].<field> == '<expected_value>'
```

### Testing Idempotency

```yaml
# First operation
- name: Create resource
  vmware.vmware_rest.<module_name>:
    <parameters>
    state: present
  register: create_result

- name: Assert creation
  ansible.builtin.assert:
    that:
      - create_result.changed
      - create_result.id == '<expected_id>'

# Load created state
- name: Load API spec for created state
  ansible.builtin.uri:
    url: "{{ mockserver_url }}/mockserver/openapi"
    method: PUT
    status_code: [200, 201]
    body_format: json
    body:
      specUrlOrPayload: "file:/mockserver_specs/created.json"
      operationsAndResponses:
        <OperationId>_list: "200"
        <OperationId>_get: "200"

# Repeat operation
- name: Create resource again (idempotent)
  vmware.vmware_rest.<module_name>:
    <parameters>
    state: present
  register: create_again

- name: Assert idempotent
  ansible.builtin.assert:
    that:
      - not create_again.changed
      - create_again.id == '<expected_id>'
```

## Troubleshooting

### Tests fail with "Connection refused"
- MockServer may not be running
- Check that `prepare_simulator` role is properly configured

### Tests fail with "404 Not Found"
- Wrong mock spec loaded
- Operation ID mismatch between test and mock
- Check `operationsAndResponses` in the URI task

### Tests fail on idempotency check
- Mock spec not switched to `created.json` state
- MockServer expectations accumulated from prior steps (add reset before expectation load)
- Module may have actual bug (report to user)

### Check mode test fails
- Ensure proper mock state is loaded before check mode test
- Verify both positive and negative check mode scenarios

### Tests fail on update idempotency
- Check that `updated.json` has been customized with the values your UPDATE test sets
- The mock generator creates `updated.json` identical to `created.json` as a baseline
- You must manually edit it to reflect your test's UPDATE values (see Step 2.5)
- Compare GET response values with what your UPDATE operation sends

### Tests fail with unexpected responses or wrong data
- MockServer expectations from previous test steps may still be active
- Add a `prepare_simulator` reset before each `Load API spec expectations` task
- The only exception is the first load in `main.yml` (MockServer just started)

## Example: Complete Test Generation

For a module pair `vcenter_resourcepool` / `vcenter_resourcepool_info`:

```bash
# Step 1: Analyze modules
# Read plugins/modules/vcenter_resourcepool.py
# Read plugins/modules/vcenter_resourcepool_info.py
# Determine: CRUD module with CREATE, DELETE, GET, LIST operations

# Step 2: Generate mocks
python content_generation/generate_openapi_mocks.py vcenter_resourcepool

# Step 3-9: Create test files
# - tests/integration/targets/vcenter_resourcepool/meta/main.yml
# - tests/integration/targets/vcenter_resourcepool/tasks/main.yml
# - tests/integration/targets/vcenter_resourcepool/tasks/info.yml
# - tests/integration/targets/vcenter_resourcepool/tasks/create.yml
# - tests/integration/targets/vcenter_resourcepool/tasks/delete.yml

# Step 10: Run tests
make integration CLI_ARGS=-vvvv INTEGRATION_TARGETS=vcenter_resourcepool
```

## Reference Files

See the `reference/` directory for complete examples:
- `info_tests_pattern.yml` - Pattern for info module tests
- `create_tests_pattern.yml` - Pattern for CREATE operation tests
- `update_tests_pattern.yml` - Pattern for UPDATE operation tests
- `delete_tests_pattern.yml` - Pattern for DELETE operation tests
- `example_module_analysis.md` - Example of module analysis output

## Remember

- **Keep tests short** - Focus on idempotency, check mode, and basic I/O
- **Don't test edge cases** - Those belong in unit tests
- **Be specific in assertions** - Check actual values, not just presence
- **Manage mock state carefully** - Load the right spec before each test
- **Report suspected module bugs** - Don't modify module code
- **Test both scenarios** - For check mode, test when change would/wouldn't occur
- **Run tests EVERY time** - Step 10 is mandatory, tests uncover critical bugs
- **Customize updated.json** - After writing UPDATE tests, edit the mock to match
- **Iterate until passing** - Fix test issues and re-run; report module bugs to user
