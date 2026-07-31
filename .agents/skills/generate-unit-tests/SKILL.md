---
name: generate-unit-tests
description: >-
  Generates comprehensive unit tests for vmware.vmware_rest Ansible modules.
  Tests validate module behavior using mocked HTTP clients and OperationConfig
  objects. Use when asked to create or regenerate unit tests for a module or
  module pair (e.g., vcenter_resourcepool and vcenter_resourcepool_info).
category: developer-tooling
subcategory: testing
---

# Generate Unit Tests for VMware REST Modules

## Purpose

Generate comprehensive unit tests for vmware.vmware_rest Ansible modules. Unit tests validate:
- **Module behavior**: Create, update, delete, get, list operations
- **OperationConfig construction**: Path building, body construction, query parameters
- **Helper methods**: Resource search, diff calculation, response normalization
- **Check mode**: Modules report changes without executing actions
- **Edge cases**: Missing resources, API errors, parameter validation

## Scope

Unit tests should be **comprehensive and fast**. They validate:
- **Base class methods**: `ensure_present()`, `ensure_absent()`, `get_resource_info()`
- **Helper methods**: `_search_for_resource()`, `_calculate_resource_diff()`, `normalize_info_results()`
- **OperationConfig behavior**: Path building, body/query construction from specs
- **Check mode**: No HTTP calls made, but correct `changed` status reported
- **Edge cases**: 404s, empty lists, diff calculations, nested parameters

**Unit tests use mocked HTTP clients** - they never make real API calls.

## Current Module Architecture

Modules now use a configuration-based approach with `OperationConfig` objects:

### Base Classes

- **`VmwareRestModuleBase`** - Abstract base for all modules
  - Creates HTTP client with authentication
  - Provides `_perform_list_operation()` and `_perform_get_operation()`
  
- **`VmwareRestCrudModuleBase`** - For CRUD modules (create/update/delete)
  - Extends `VmwareRestModuleBase`
  - Implements `ensure_present()` and `ensure_absent()`
  - Handles resource search, diff calculation, and updates
  
- **`VmwareRestInfoModuleBase`** - For info modules (read-only)
  - Extends `VmwareRestModuleBase`
  - Implements `get_resource_info()`
  - Handles result normalization

### OperationConfig Pattern

Modules define operation configurations instead of PayloadMap objects:

```python
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)

GET_OPERATION = OperationConfig(
    name="get",
    uri="/vcenter/resource-pool/{resource_pool}",
    http_method="get",
)

LIST_OPERATION = OperationConfig(
    name="list",
    uri="/vcenter/resource-pool",
    http_method="get",
    query_spec={
        "names": {"required": False},
        "parent_resource_pools": {"required": False},
    },
)

CREATE_OPERATION = OperationConfig(
    name="create",
    uri="/vcenter/resource-pool",
    http_method="post",
    body_spec={
        "name": {"required": True},
        "parent": {"required": True},
        "cpu_allocation": {
            "required": False,
            "subspec": {
                "reservation": {"required": False},
                "limit": {"required": False},
            },
        },
    },
)
```

### Module Constants

Modules define these endpoint constants:

```python
LIST_ENDPOINT = "/vcenter/resource-pool"
ITEM_ENDPOINT = "/vcenter/resource-pool/{resource_pool}"
MOID_PARAMETER_HINTS = ["resource_pool"]
```

## When to Use This Skill

Use this skill when asked to:
- Generate unit tests for a new module
- Regenerate unit tests for an existing module
- Add missing test coverage for a module
- Create tests for a module pair (e.g., `vcenter_resourcepool` and `vcenter_resourcepool_info`)

## Prerequisites

- Module(s) must exist in `plugins/modules/`
- Test utilities must be available in `tests/unit/common/utils.py`
- Base classes in `plugins/module_utils/` must be available

## Workflow

### Step 1: Analyze the Module

Read the module file to understand:

1. **Module Type**:
   - CRUD module (has `state` parameter, extends `VmwareRestCrudModuleBase`)
   - Info module (read-only, ends with `_info`, extends `VmwareRestInfoModuleBase`)

2. **Operation Configs** - Look for `OperationConfig` definitions:
   - `GET_OPERATION` - Single resource retrieval
   - `LIST_OPERATION` - Multiple resource retrieval (info modules)
   - `CREATE_OPERATION` - Resource creation (CRUD modules)
   - `UPDATE_OPERATION` - Resource update (CRUD modules)
   - `DELETE_OPERATION` - Resource deletion (CRUD modules)

3. **Module Constants**:
   - `LIST_ENDPOINT` - API path for list operations
   - `ITEM_ENDPOINT` - API path for item operations
   - `MOID_PARAMETER_HINTS` - List of parameter names that represent resource IDs

4. **Module Parameters** - From `create_module_argument_spec()`:
   - `state` parameter (for CRUD modules)
   - MOID parameter (the resource identifier, e.g., `resource_pool`)
   - Required parameters for creation
   - Optional parameters
   - Filter parameters (for info modules with LIST support)

### Step 2: Create Test File Structure

Create test file at `tests/unit/plugins/modules/test_<module_name>.py`:

**IMPORTANT**: Do NOT redefine `mock_client` or other fixtures already available from `conftest.py`. Use the shared fixtures to avoid duplication.

```python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for <module_name> module.

Tests validate the <CRUD/Info> module behavior using the OperationConfig-based
architecture with mocked HTTP clients.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import MagicMock, patch

from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._crud_module import (
    VmwareRestCrudModuleBase,  # or VmwareRestInfoModuleBase
)

from ...common.utils import CONNECTION_PARAMS, fail_json


@pytest.fixture
def mock_module():
    """
    Mock Ansible module object.
    """
    module = MagicMock()
    module.params = CONNECTION_PARAMS.copy()
    module.check_mode = False
    module.fail_json = fail_json
    return module


@pytest.fixture
def crud_module(mock_module, mock_client):
    """
    Create CRUD module instance with operation configs.
    
    Note: mock_client is provided by conftest.py - do not redefine it.
    """
    # Define operation configs matching the actual module
    get_operation = OperationConfig(
        name="get",
        uri="/vcenter/resource-pool/{resource_pool}",
        http_method="GET",
    )
    
    list_operation = OperationConfig(
        name="list",
        uri="/vcenter/resource-pool",
        http_method="GET",
    )
    
    create_operation = OperationConfig(
        name="create",
        uri="/vcenter/resource-pool",
        http_method="POST",
        body_spec={
            "name": {"required": True},
            "parent": {"required": True},
        },
    )
    
    # Patch Client to return our mock
    with patch(
        "ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base.Client",
        return_value=mock_client,
    ):
        module = VmwareRestCrudModuleBase(
            module=mock_module,
            get_operation_config=get_operation,
            list_operation_config=list_operation,
            create_operation_config=create_operation,
            # ... other operation configs
            moid_parameter_hints=["resource_pool"],
        )
        yield module
```

**Available Shared Fixtures** (from `conftest.py`):
- `mock_client` - Mock HTTP client (already defined in `tests/unit/common/utils.py`)
- `module_args` - Base module arguments dictionary with CONNECTION_PARAMS

**Only define module-specific fixtures**:
- `mock_module` - Mock Ansible module object (sets params and check_mode)
- `crud_module` or `info_module` - Module instance with operation configs

### Step 3: Write Operation Tests for CRUD Modules

Test the high-level methods that users call:

#### Test ensure_present() - Create New Resource

```python
def test_ensure_present_creates_resource(crud_module, mock_client):
    """Test creating a new resource."""
    crud_module.params["name"] = "new_pool"
    crud_module.params["parent"] = "parent-pool-1"
    
    # Resource not found, will create
    with patch.object(crud_module, "_search_for_resource", return_value=None):
        create_response = MagicMock()
        create_response.status = 201
        create_response.json = "pool-1"
        mock_client.post.return_value = create_response
        
        result = crud_module.ensure_present()
    
    assert result["changed"] is True
    assert result["id"] == "pool-1"
    mock_client.post.assert_called_once()
```

#### Test ensure_present() - Update Existing Resource

```python
def test_ensure_present_updates_resource(crud_module, mock_client):
    """Test updating an existing resource when changes detected."""
    crud_module.params["resource_pool"] = "pool-1"
    crud_module.params["name"] = "updated_pool"
    
    # Resource found with different name
    existing_resource = {"resource_pool": "pool-1", "name": "old_pool"}
    
    with patch.object(crud_module, "_search_for_resource", return_value=existing_resource):
        update_response = MagicMock()
        update_response.status = 200
        mock_client.patch.return_value = update_response
        
        result = crud_module.ensure_present()
    
    assert result["changed"] is True
    assert result["id"] == "pool-1"
    assert result["diff"] == {"name": {"before": "old_pool", "after": "updated_pool"}}
    mock_client.patch.assert_called_once()
```

#### Test ensure_present() - No Changes (Idempotent)

```python
def test_ensure_present_no_changes(crud_module, mock_client):
    """Test no changes when resource already in desired state."""
    crud_module.params["resource_pool"] = "pool-1"
    crud_module.params["name"] = "my_pool"
    
    # Resource found with same state
    existing_resource = {"resource_pool": "pool-1", "name": "my_pool"}
    
    with patch.object(crud_module, "_search_for_resource", return_value=existing_resource):
        result = crud_module.ensure_present()
    
    assert result["changed"] is False
    assert result["id"] == "pool-1"
    mock_client.patch.assert_not_called()
```

#### Test ensure_absent() - Delete Existing Resource

```python
def test_ensure_absent_deletes_resource(crud_module, mock_client):
    """Test deleting an existing resource."""
    crud_module.params["resource_pool"] = "pool-1"
    
    # Resource exists
    existing_resource = {"resource_pool": "pool-1", "name": "my_pool"}
    
    with patch.object(crud_module, "_search_for_resource", return_value=existing_resource):
        delete_response = MagicMock()
        delete_response.status = 204
        mock_client.delete.return_value = delete_response
        
        result = crud_module.ensure_absent()
    
    assert result["changed"] is True
    mock_client.delete.assert_called_once()
```

#### Test ensure_absent() - Already Absent (Idempotent)

```python
def test_ensure_absent_already_absent(crud_module, mock_client):
    """Test deleting a resource that doesn't exist (idempotent)."""
    crud_module.params["resource_pool"] = "pool-999"
    
    # Resource not found
    with patch.object(crud_module, "_search_for_resource", return_value=None):
        result = crud_module.ensure_absent()
    
    assert result["changed"] is False
    mock_client.delete.assert_not_called()
```

### Step 4: Write Operation Tests for Info Modules

Test the `get_resource_info()` method:

#### Test Get Specific Resource

```python
def test_get_resource_info_by_id(info_module, mock_client):
    """Test getting a specific resource by ID."""
    info_module.params["resource_pool"] = "pool-1"
    
    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "resource_pool": "pool-1",
        "name": "my_pool",
        "cpu_allocation": {"reservation": 1000},
    }
    mock_client.get.return_value = get_response
    
    result = info_module.get_resource_info()
    
    assert result["id"] == "pool-1"
    assert "value" in result
    assert result["value"]["name"] == "my_pool"
```

#### Test List All Resources

```python
def test_get_resource_info_list_all(info_module, mock_client):
    """Test listing all resources."""
    # No resource_pool param = list all
    
    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [
        {"resource_pool": "pool-1", "name": "pool1"},
        {"resource_pool": "pool-2", "name": "pool2"},
    ]
    mock_client.get.return_value = list_response
    
    result = info_module.get_resource_info()
    
    assert "info" in result
    assert len(result["info"]) == 2
    assert result["info"][0]["resource_pool"] == "pool-1"
```

#### Test List Empty Results

```python
def test_get_resource_info_empty_list(info_module, mock_client):
    """Test listing when no resources exist."""
    list_response = MagicMock()
    list_response.status = 200
    list_response.json = []
    mock_client.get.return_value = list_response
    
    result = info_module.get_resource_info()
    
    assert "info" in result
    assert len(result["info"]) == 0
```

#### Test Resource Not Found (404)

```python
def test_get_resource_info_not_found(info_module, mock_client):
    """Test getting a resource that doesn't exist."""
    info_module.params["resource_pool"] = "pool-999"
    
    get_response = MagicMock()
    get_response.status = 404
    mock_client.get.return_value = get_response
    
    result = info_module.get_resource_info()
    
    # Info modules return empty when not found
    assert "info" in result
    assert len(result["info"]) == 0
```

### Step 5: Write Helper Method Tests

Test internal methods used by the base classes:

#### Test _search_for_resource() by ID

```python
def test_search_for_resource_by_id(crud_module, mock_client):
    """Test searching for a resource by its ID."""
    crud_module.params["resource_pool"] = "pool-1"
    
    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {"resource_pool": "pool-1", "name": "my_pool"}
    mock_client.get.return_value = get_response
    
    result = crud_module._search_for_resource()
    
    assert result is not None
    assert result["resource_pool"] == "pool-1"
    assert result["name"] == "my_pool"
```

#### Test _search_for_resource() by Name

```python
def test_search_for_resource_by_name(crud_module, mock_client):
    """Test searching for a resource by name when ID not provided."""
    crud_module.params["name"] = "my_pool"
    # No resource_pool param
    
    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [
        {"resource_pool": "pool-1", "name": "my_pool"},
        {"resource_pool": "pool-2", "name": "other_pool"},
    ]
    mock_client.get.return_value = list_response
    
    result = crud_module._search_for_resource()
    
    assert result is not None
    assert result["resource_pool"] == "pool-1"
    assert result["name"] == "my_pool"
```

#### Test _calculate_resource_diff()

```python
def test_calculate_resource_diff_simple(crud_module):
    """Test diff calculation with simple parameters."""
    current = {"name": "old_name", "description": "desc"}
    desired = {"name": "new_name", "description": "desc"}
    
    diff = crud_module._calculate_resource_diff(current, desired)
    
    assert diff == {"name": {"before": "old_name", "after": "new_name"}}


def test_calculate_resource_diff_nested(crud_module):
    """Test diff calculation with nested parameters."""
    current = {
        "name": "pool",
        "cpu_allocation": {"reservation": 1000, "limit": 2000},
    }
    desired = {
        "name": "pool",
        "cpu_allocation": {"reservation": 1500, "limit": 2000},
    }
    
    diff = crud_module._calculate_resource_diff(current, desired)
    
    assert diff == {
        "cpu_allocation": {
            "reservation": {"before": 1000, "after": 1500}
        }
    }
```

### Step 6: Write Check Mode Tests

Test that check mode reports changes without making HTTP calls:

```python
def test_ensure_present_check_mode_create(crud_module, mock_client):
    """Test creating a resource in check mode."""
    crud_module.params["name"] = "new_pool"
    crud_module.params["parent"] = "parent-1"
    crud_module.module.check_mode = True
    
    with patch.object(crud_module, "_search_for_resource", return_value=None):
        result = crud_module.ensure_present()
    
    assert result["changed"] is True
    # No actual POST should occur in check mode
    mock_client.post.assert_not_called()


def test_ensure_absent_check_mode(crud_module, mock_client):
    """Test deleting a resource in check mode."""
    crud_module.params["resource_pool"] = "pool-1"
    crud_module.module.check_mode = True
    
    existing_resource = {"resource_pool": "pool-1", "name": "my_pool"}
    
    with patch.object(crud_module, "_search_for_resource", return_value=existing_resource):
        result = crud_module.ensure_absent()
    
    assert result["changed"] is True
    # No actual DELETE should occur in check mode
    mock_client.delete.assert_not_called()
```

### Step 7: Write OperationConfig Tests

Test that OperationConfig objects build paths and bodies correctly:

```python
def test_operation_config_build_path():
    """Test that OperationConfig builds paths with parameters."""
    config = OperationConfig(
        name="get",
        uri="/vcenter/resource-pool/{resource_pool}",
        http_method="get",
    )
    
    params = {"resource_pool": "pool-1"}
    path = config.build_path(params)
    
    assert path == "/vcenter/resource-pool/pool-1"


def test_operation_config_build_body_simple():
    """Test that OperationConfig builds request bodies."""
    config = OperationConfig(
        name="create",
        uri="/vcenter/resource-pool",
        http_method="post",
        body_spec={
            "name": {"required": True},
            "parent": {"required": True},
        },
    )
    
    params = {"name": "my_pool", "parent": "parent-1"}
    body = config.build_body(params)
    
    assert body == {"name": "my_pool", "parent": "parent-1"}


def test_operation_config_build_body_nested():
    """Test that OperationConfig builds nested request bodies."""
    config = OperationConfig(
        name="create",
        uri="/vcenter/resource-pool",
        http_method="post",
        body_spec={
            "name": {"required": True},
            "cpu_allocation": {
                "required": False,
                "subspec": {
                    "reservation": {"required": False},
                    "limit": {"required": False},
                },
            },
        },
    )
    
    params = {
        "name": "my_pool",
        "cpu_allocation": {"reservation": 1000, "limit": 2000},
    }
    body = config.build_body(params)
    
    assert body == {
        "name": "my_pool",
        "cpu_allocation": {"reservation": 1000, "limit": 2000},
    }


def test_operation_config_build_query():
    """Test that OperationConfig builds query parameters."""
    config = OperationConfig(
        name="list",
        uri="/vcenter/resource-pool",
        http_method="get",
        query_spec={
            "names": {"required": False},
            "parent_resource_pools": {"required": False},
        },
    )
    
    params = {"names": ["pool1", "pool2"]}
    query = config.build_query(params)
    
    assert query == {"names": ["pool1", "pool2"]}
```

### Step 8: Run and Validate Tests

Execute the unit tests using the Makefile:

```bash
make units
```

**IMPORTANT**: Always use `make units` to run unit tests. Never use `pytest` directly.

**Success criteria**:
- All tests pass
- No failures or errors
- Coverage report shows reasonable coverage

**If tests fail**:
1. **Read the full error message** - it tells you exactly what's wrong
2. Review the failure output carefully
3. Check if it's a test issue (incorrect assertions, wrong mock responses)
4. **Fix the test** - adjust mock responses, add missing calls, correct assertions
5. **Re-run tests with `make units`** until they all pass

## Common Testing Patterns

### Available Shared Fixtures

The following fixtures are available from `conftest.py` and should NEVER be redefined in test files:

- **`mock_client`** - Mock HTTP client (`MagicMock()`)
- **`module_args`** - Dictionary with `CONNECTION_PARAMS`

These are automatically available to all test functions via pytest's fixture discovery.

### Mocking HTTP Responses

```python
# Success response with body
mock_response = MagicMock()
mock_response.status = 200
mock_response.json = {"resource_pool": "pool-1", "name": "my_pool"}
mock_client.get.return_value = mock_response

# Success response without body (204 No Content)
delete_response = MagicMock()
delete_response.status = 204
mock_client.delete.return_value = delete_response

# Created response with ID
create_response = MagicMock()
create_response.status = 201
create_response.json = "pool-1"
mock_client.post.return_value = create_response

# Not found response
not_found_response = MagicMock()
not_found_response.status = 404
mock_client.get.return_value = not_found_response
```

### Using patch.object() for Internal Methods

```python
# Patch internal method to control its return value
with patch.object(crud_module, "_search_for_resource", return_value=None):
    result = crud_module.ensure_present()

# Patch multiple methods
with patch.object(crud_module, "_search_for_resource", return_value=existing):
    with patch.object(crud_module, "_calculate_resource_diff", return_value=diff):
        result = crud_module.ensure_present()
```

## Module Type Specific Test Coverage

### CRUD Module Tests Must Include

1. `ensure_present()` - create new resource
2. `ensure_present()` - update existing resource
3. `ensure_present()` - no changes (idempotent)
4. `ensure_absent()` - delete existing resource
5. `ensure_absent()` - already absent (idempotent)
6. `_search_for_resource()` - by ID
7. `_search_for_resource()` - by name
8. `_calculate_resource_diff()` - simple and nested
9. Check mode for create, update, delete
10. OperationConfig path/body/query building

### Info Module Tests Must Include

1. `get_resource_info()` - get by ID (found)
2. `get_resource_info()` - get by ID (not found/404)
3. `get_resource_info()` - list all
4. `get_resource_info()` - list with filters
5. `get_resource_info()` - empty list
6. `normalize_info_results()` - single resource
7. `normalize_info_results()` - multiple resources
8. Check mode (should execute normally for read-only)
9. OperationConfig path/query building

## Reference Examples

For complete working examples, see:
- `tests/unit/plugins/module_utils/test_crud_module.py` - Base class tests for CRUD modules
- `tests/unit/plugins/module_utils/test_info_module.py` - Base class tests for info modules
- `tests/unit/plugins/module_utils/test_module_base.py` - Base class common functionality
- `.agents/skills/generate-unit-tests/reference/test_vcenter_resourcepool.py` - Full CRUD module example
- `.agents/skills/generate-unit-tests/reference/test_vcenter_resourcepool_info.py` - Full info module example

## Key Differences from Old Pattern

| Aspect | Old Pattern | New Pattern |
|--------|-------------|-------------|
| **Payload definitions** | `PayloadMap` objects | `OperationConfig` with `body_spec` |
| **Path constants** | `LIST_PATH`, `ITEM_PATH` | `LIST_ENDPOINT`, `ITEM_ENDPOINT` |
| **Mapping dictionaries** | `CREATE_BODY_MAPPING`, `UPDATE_BODY_MAPPING` | Embedded in `body_spec` |
| **Test focus** | Module constants and payload maps | Base class methods and operation configs |
| **Test structure** | Mock individual modules | Test base class behavior with configs |
| **Fixtures** | Auto-patch `AnsibleModule` | Create base class instances with configs |

## Remember

- **Use shared fixtures** - `mock_client` and `module_args` are provided by `conftest.py`. Never redefine them in test files.
- **Only define module-specific fixtures** - `mock_module` and module instance fixtures (`crud_module`, `info_module`)
- **Test base class behavior** - Focus on `ensure_present()`, `ensure_absent()`, `get_resource_info()`
- **Mock at boundaries** - Mock the HTTP client, not internal methods (unless testing specific behavior)
- **Use OperationConfig** - Create operation configs in fixtures to match module definitions
- **Test helpers** - Validate `_search_for_resource()`, `_calculate_resource_diff()`, etc.
- **Check mode matters** - Verify no HTTP calls in check mode
- **Be comprehensive** - Cover success, failure, edge cases, and idempotency
- **Use `make units` to run tests** - Never run `pytest` directly
