# Unit Test Generation Walkthrough

This document summarizes the walkthrough we completed to regenerate unit tests for vmware.vmware_rest modules.

## Modules Tested

1. **vcenter_datacenter** - CRUD module (21 tests)
2. **vcenter_datacenter_info** - Info module with LIST support (19 tests)
3. **vcenter_vm_tools_installer_info** - Item-only info module (14 tests)

**Total: 54 tests, all passing ✓**

## Key Lessons Learned

### 1. Info Modules Require Multiple Mock Responses

**Critical Discovery:** Info modules with LIST support call `_list_resource_details()`, which:
1. Calls LIST endpoint to get resource summaries
2. For EACH resource, calls GET endpoint to fetch full details

**Initial Mistake:**
```python
# This FAILS - only mocks the LIST call
mock_client.get.return_value = _response(200, list_response)
```

**Correct Approach:**
```python
# Mock LIST + GET for each resource
mock_client.get.side_effect = [
    _response(200, list_response),      # LIST call
    _response(200, get_response_1),     # GET for first resource
    _response(200, get_response_2),     # GET for second resource
]
```

### 2. Test Execution is Mandatory

**Problem:** Initially created tests without running them - discovered failures only when user pointed it out.

**Solution:** Always run tests and fix failures before completing:
```bash
make units UNIT_TARGETS="tests/unit/plugins/modules/test_<module_name>.py"
```

Look for "XX passed" in output - Docker cleanup errors (exit code 2) are non-fatal.

### 3. PayloadMap Uses Public Attributes

**Initial Mistake:**
```python
assert payload_map._uri == "/path"      # AttributeError
assert payload_map._operation == "get"   # AttributeError
```

**Correct:**
```python
assert payload_map.uri == "/path"       # ✓
assert payload_map.operation == "get"    # ✓
```

### 4. Empty List Tests Don't Need GET Mocks

When testing empty list responses, no GET calls are made (no resources to fetch):

```python
# Correct - only LIST call needed
list_response = []
mock_client.get.return_value = _response(200, list_response)
```

## Test Patterns Used

### CRUD Module (vcenter_datacenter)

- **CREATE tests**: New resource, idempotent (existing resource), name-only
- **DELETE tests**: By ID, by name, not found (idempotent)
- **Check mode tests**: Create and delete scenarios
- **Module constants tests**: MOID, paths, payload maps
- **Payload mapping tests**: Body mappings, query mappings
- **Argument spec tests**: State, MOID, parameters
- **API call payload tests**: Verify request bodies and paths

### Info Module with LIST (vcenter_datacenter_info)

- **LIST tests**: All resources, empty, with name filter, with folder filter
- **GET tests**: By ID (found), by ID (not found)
- **Check mode tests**: List and get operations
- **Module constants tests**: MOID, paths, payload maps
- **Payload mapping tests**: Path and query mappings
- **Argument spec tests**: MOID, filter parameters with aliases

### Item-Only Info Module (vcenter_vm_tools_installer_info)

- **GET tests**: Found, not found, different response values
- **Check mode tests**: Get operation
- **Module constants tests**: MOID, item path, no list path
- **Payload mapping tests**: Path mapping, URI construction
- **Argument spec tests**: Required MOID, no filter parameters
- **API call tests**: Correct path construction

## Test Utilities Used

- `AnsibleExitJson` / `AnsibleFailJson` - Exception classes for catching module results
- `exit_json()` / `fail_json()` - Mock functions for module execution
- `_response(status, body)` - Creates mock HTTP Response objects
- `set_module_args(args)` - Merges test args with connection params
- `mock_client` fixture - MagicMock HTTP client
- `module_args` fixture - Pre-filled connection parameters

## Files Created

1. `tests/unit/plugins/modules/test_vcenter_datacenter.py`
2. `tests/unit/plugins/modules/test_vcenter_datacenter_info.py`
3. `tests/unit/plugins/modules/test_vcenter_vm_tools_installer_info.py`
4. `.agents/skills/generate-unit-tests/SKILL.md` - Comprehensive skill documentation
5. `.agents/skills/generate-unit-tests/reference/` - Reference examples and utilities

## Running All Tests

```bash
# Individual modules
make units UNIT_TARGETS="tests/unit/plugins/modules/test_vcenter_datacenter.py"
make units UNIT_TARGETS="tests/unit/plugins/modules/test_vcenter_datacenter_info.py"
make units UNIT_TARGETS="tests/unit/plugins/modules/test_vcenter_vm_tools_installer_info.py"

# All together
make units UNIT_TARGETS="tests/unit/plugins/modules/test_vcenter_datacenter.py tests/unit/plugins/modules/test_vcenter_datacenter_info.py tests/unit/plugins/modules/test_vcenter_vm_tools_installer_info.py"
```

## Success Metrics

- ✅ 54 tests created
- ✅ 100% pass rate
- ✅ All three module types covered (CRUD, info with LIST, item-only info)
- ✅ Comprehensive skill documentation created
- ✅ Reference examples captured
- ✅ Common pitfalls documented
- ✅ Test-driven workflow established (run tests, fix failures, repeat)

## Next Steps

Use this skill to generate unit tests for other modules in the collection:
1. Analyze the module to determine type and operations
2. Create test file using patterns from references
3. **Run tests and fix failures** (critical!)
4. Verify all tests pass before completing
