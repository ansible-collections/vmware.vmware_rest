# Example Module Analysis

This document shows what to look for when analyzing a module for integration test generation.

## Example: vcenter_datacenter Module

### File Location
`plugins/modules/vcenter_datacenter.py`

### Module Type
**CRUD Module** - Has `state` parameter with `present` and `absent` choices

### Key Constants

```python
MOID_ATTRIBUTE_NAME = "datacenter"
LIST_PATH = "/vcenter/datacenter"
ITEM_PATH = "/vcenter/datacenter/{datacenter}"
```

**Interpretation**:
- Resource identifier field: `datacenter`
- List endpoint: `/vcenter/datacenter`
- Item endpoint: `/vcenter/datacenter/{datacenter}` (has path parameter)

### Supported Operations

```python
GET_PAYLOAD_MAP = PayloadMap(
    operation="get", uri=ITEM_PATH, path=Mappings({"datacenter": "datacenter"})
)

LIST_PAYLOAD_MAP = PayloadMap(
    operation="list",
    uri=LIST_PATH,
    query=Mappings({"names": "name"}),
)

CREATE_PAYLOAD_MAP = PayloadMap(
    operation="create", uri=LIST_PATH, body=CREATE_BODY_MAPPING
)

DELETE_PAYLOAD_MAP = PayloadMap(
    operation="delete",
    uri=ITEM_PATH,
    path=Mappings({"datacenter": "datacenter"}),
)
```

**Interpretation**:
- ✅ GET operation supported
- ✅ LIST operation supported
- ✅ CREATE operation supported
- ❌ UPDATE operation NOT supported
- ✅ DELETE operation supported

### Module Parameters

From `create_module_argument_spec()`:

```python
module_args["state"] = {
    "type": "str",
    "choices": ["present", "absent"],
    "default": "present",
}
module_args["datacenter"] = {"type": "str"}  # Resource ID
module_args["name"] = {"type": "str"}        # Resource name
module_args["folder"] = {"type": "str"}      # Parent folder
```

**Interpretation**:
- `datacenter`: Resource identifier (MOID)
- `name`: Resource name (used for creation and lookup)
- `folder`: Required for creation, used for name-based lookup
- `state`: Controls create vs delete

### Operation IDs

Based on the LIST_PATH `/vcenter/datacenter`:
- List: `Vcenter.Datacenter_list`
- Get: `Vcenter.Datacenter_get`
- Create: `Vcenter.Datacenter_create`
- Delete: `Vcenter.Datacenter_delete`

### Test Files to Create

Based on the analysis:
1. ✅ `tasks/info.yml` - Tests LIST and GET operations
2. ✅ `tasks/create.yml` - Tests CREATE operation
3. ❌ `tasks/update.yml` - NOT needed (no UPDATE operation)
4. ✅ `tasks/delete.yml` - Tests DELETE operation

### Mock Files Needed

Based on supported operations:
1. ✅ `default.json` - Empty state
2. ✅ `created.json` - Resource exists
3. ✅ `list_multiple.json` - Multiple resources
4. ❌ `updated.json` - NOT needed (no UPDATE operation)

### Example Test Parameters

For create tests:
```yaml
- name: Create a datacenter
  vmware.vmware_rest.vcenter_datacenter:
    name: my_datacenter
    folder: group-d1
    state: present
```

For delete by ID:
```yaml
- name: Delete a datacenter by ID
  vmware.vmware_rest.vcenter_datacenter:
    datacenter: datacenter-1001
    state: absent
```

For delete by name (requires folder for lookup):
```yaml
- name: Delete a datacenter by name
  vmware.vmware_rest.vcenter_datacenter:
    name: my_datacenter
    folder: group-d1
    state: absent
```

## Example: vcenter_datacenter_info Module

### File Location
`plugins/modules/vcenter_datacenter_info.py`

### Module Type
**Info Module** - Read-only, no `state` parameter, ends with `_info`

### Key Constants

```python
MOID_ATTRIBUTE_NAME = "datacenter"
LIST_PATH = "/vcenter/datacenter"
ITEM_PATH = "/vcenter/datacenter/{datacenter}"
```

### Supported Operations

```python
GET_PAYLOAD_MAP = PayloadMap(
    operation="get", uri=ITEM_PATH, path=Mappings({"datacenter": "datacenter"})
)

LIST_PAYLOAD_MAP = PayloadMap(
    operation="list",
    uri=LIST_PATH,
    query=Mappings({
        "datacenters": "datacenters",
        "names": "names",
        "folders": "folders",
    }),
)
```

**Interpretation**:
- ✅ GET operation supported
- ✅ LIST operation supported with filter parameters
- ❌ CREATE operation NOT supported (info module)
- ❌ UPDATE operation NOT supported (info module)
- ❌ DELETE operation NOT supported (info module)

### Module Parameters

```python
module_args["datacenter"] = {"type": "str"}
module_args["datacenters"] = {"type": "list", "elements": "str", "aliases": ["filter_datacenters"]}
module_args["names"] = {"type": "list", "elements": "str", "aliases": ["filter_names"]}
module_args["folders"] = {"type": "list", "elements": "str", "aliases": ["filter_folders"]}
```

**Interpretation**:
- `datacenter`: Get specific datacenter by ID
- `datacenters`: Filter list by IDs
- `names`: Filter list by names
- `folders`: Filter list by folders

### Return Values

```python
RETURN = r"""
value:
  description: Read details from a specific datacenter
  returned: When a single datacenter is retrieved
  sample:
    name: my_datacenter
    datastore_folder: group-s5
    host_folder: group-h4
    network_folder: group-n6
    vm_folder: group-v3
  type: dict

datacenters:
  description: List of datacenter objects
  returned: On success
  type: list
```

**Interpretation**:
- `value`: Returned when getting single datacenter
- `datacenters`: Returned when listing
- Check specific fields: `name`, `datastore_folder`, `host_folder`, `network_folder`, `vm_folder`

### Test Files to Create

Based on the analysis:
1. ✅ `tasks/info.yml` - Tests LIST and GET operations
2. ❌ `tasks/create.yml` - NOT needed (info module)
3. ❌ `tasks/update.yml` - NOT needed (info module)
4. ❌ `tasks/delete.yml` - NOT needed (info module)

**Note**: Info module tests go in the same target directory as the CRUD module (`vcenter_datacenter`), not in a separate `vcenter_datacenter_info` directory.

## Example: vcenter_vm_tools_installer_info Module

### File Location
`plugins/modules/vcenter_vm_tools_installer_info.py`

### Module Type
**Info Module** - Read-only, no list operation (only GET)

### Key Constants

```python
MOID_ATTRIBUTE_NAME = "vm"
ITEM_PATH = "/vcenter/vm/{vm}/tools/installer"
```

**Note**: No `LIST_PATH` defined - this is a GET-only module

### Supported Operations

```python
GET_PAYLOAD_MAP = PayloadMap(
    operation="get", uri=ITEM_PATH, path=Mappings({"vm": "vm"})
)
```

**Interpretation**:
- ✅ GET operation supported
- ❌ LIST operation NOT supported
- ❌ CREATE operation NOT supported
- ❌ UPDATE operation NOT supported
- ❌ DELETE operation NOT supported

### Operation IDs

Based on the nested ITEM_PATH `/vcenter/vm/{vm}/tools/installer`:
- Get: `Vcenter.Vm.Tools.Installer_get` (note the dots for nested paths)

### Mock Files Needed

For GET-only modules:
1. ✅ `default.json` - Default GET response
2. ❌ `created.json` - NOT needed (no creation)
3. ❌ `list_multiple.json` - NOT needed (no list operation)
4. ❌ `updated.json` - NOT needed (no update)

May need additional state files for different response scenarios (e.g., `not_connected.json` for different installer states).

### Test Structure

GET-only modules have simpler tests:
```yaml
- name: Get VM tools installer info
  vmware.vmware_rest.vcenter_vm_tools_installer_info:
    vm: vm-1001
  register: installer_info

- name: Assert installer details
  ansible.builtin.assert:
    that:
      - installer_info.value is defined
      - installer_info.value.is_connected is defined
```

## Key Takeaways

1. **CRUD modules** have `state` parameter and multiple operations
2. **Info modules** end with `_info`, are read-only, have GET and/or LIST
3. **Check for `*_PAYLOAD_MAP` constants** to determine supported operations
4. **Operation IDs follow the pattern**: `Vcenter.ResourceName_operation`
5. **Nested resources** use dots in operation IDs: `Vcenter.Vm.Tools.Installer_get`
6. **Test files created** should match supported operations
7. **Mock files generated** should match operation types
8. **Module parameters** determine what test scenarios are possible
9. **Return values** guide what assertions to write
