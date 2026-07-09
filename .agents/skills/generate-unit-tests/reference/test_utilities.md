# Test Utilities Reference

This document describes the test utilities available in `tests/unit/common/utils.py` for writing unit tests.

## Exception Classes

### AnsibleExitJson

Exception raised when a module calls `exit_json()`.

**Usage:**
```python
from ...common.utils import AnsibleExitJson

with pytest.raises(AnsibleExitJson) as exc:
    module_under_test.main()

result = exc.value.kwargs
assert result["changed"] is True
```

**Purpose:** Allows tests to catch and inspect the results returned by `module.exit_json()`.

### AnsibleFailJson

Exception raised when a module calls `fail_json()`.

**Usage:**
```python
from ...common.utils import AnsibleFailJson

with pytest.raises(AnsibleFailJson) as exc:
    module_under_test.main()

result = exc.value.kwargs
assert "msg" in result
```

**Purpose:** Allows tests to verify error handling and failure scenarios.

## Helper Functions

### exit_json(*args, **kwargs)

Mock function that raises `AnsibleExitJson` with provided kwargs.

**Usage:**
```python
from ...common.utils import exit_json

mock_module.exit_json.side_effect = exit_json
```

**Purpose:** Used as side effect for `mock_module.exit_json` to convert successful module execution into a catchable exception.

### fail_json(*args, **kwargs)

Mock function that raises `AnsibleFailJson` with provided kwargs.

**Usage:**
```python
from ...common.utils import fail_json

mock_module.fail_json.side_effect = fail_json
```

**Purpose:** Used as side effect for `mock_module.fail_json` to convert module failures into catchable exceptions.

### _response(status, body)

Creates a mock Response object for HTTP client mocking.

**Parameters:**
- `status` (int): HTTP status code (200, 201, 204, 404, etc.)
- `body` (dict, list, str, or None): Response body

**Returns:** `Response` object with the given status and JSON-encoded body

**Usage:**
```python
from ...common.utils import _response

# Success response with body
mock_client.get.return_value = _response(200, {"name": "value"})

# Created response with ID
mock_client.post.return_value = _response(201, "resource-1009")

# No content response
mock_client.delete.return_value = _response(204, None)

# Not found response
mock_client.get.return_value = _response(404, None)

# List response
mock_client.get.return_value = _response(200, [
    {"resource": "res-1", "name": "name1"},
    {"resource": "res-2", "name": "name2"},
])
```

**Special cases:**
- `status == 204` or `status >= 400`: Empty body even if `body` is provided
- `body == None` and not 204/4xx: JSON-encodes `None` as `"null"`
- Otherwise: JSON-encodes the body

### set_module_args(args)

Merges test arguments with connection parameters.

**Parameters:**
- `args` (dict): Test-specific module arguments

**Returns:** Dict with connection parameters + test arguments

**Usage:**
```python
from ...common.utils import set_module_args

module_args.update({
    "state": "present",
    "name": "my_resource",
})
mock_module.params = set_module_args(module_args)
```

**Purpose:** Ensures all tests have required connection parameters without repeating them.

## Fixtures

### mock_client (fixture)

Provides a MagicMock object representing the HTTP client.

**Usage:**
```python
def test_something(mock_client):
    # Configure mock responses
    mock_client.get.return_value = _response(200, {"data": "value"})
    
    # Use in test
    ...
```

**Available methods:**
- `get(path, query=None)` - GET request
- `post(path, body, query=None)` - POST request
- `patch(path, body, query=None)` - PATCH request
- `delete(path, query=None)` - DELETE request

### module_args (fixture)

Provides a dict with connection parameters pre-filled.

**Usage:**
```python
def test_something(module_args):
    # Add test-specific parameters
    module_args.update({
        "state": "present",
        "name": "test_resource",
    })
    
    mock_module.params = set_module_args(module_args)
```

**Pre-filled parameters:**
- `vcenter_hostname`: "vcenter.example.com"
- `vcenter_username`: "admin"
- `vcenter_password`: "secret"
- `vcenter_port`: None
- `vcenter_validate_certs`: False
- `vcenter_rest_log_file`: None
- `session_timeout`: None

## Common Test Patterns

### Standard Test Setup

```python
def test_operation(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test description."""
    # Inject mock client
    patch_create_client.return_value = mock_client
    
    # Create mock module
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    
    # Set module parameters
    module_args.update({"param": "value"})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False
    
    # Configure mock responses
    mock_client.get.return_value = _response(200, {"data": "value"})
    
    # Execute module and catch result
    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()
    
    # Verify result
    result = exc.value.kwargs
    assert result["changed"] is True
```

### Multiple HTTP Responses

When the module makes multiple HTTP calls:

```python
# Configure sequence of responses
mock_client.get.side_effect = [
    _response(200, list_response),
    _response(200, get_response),
]

# Execute module
with pytest.raises(AnsibleExitJson) as exc:
    module_under_test.main()

# Both GET calls will return in order
```

### Verifying API Calls

```python
# Verify call was made
mock_client.post.assert_called_once()

# Verify call was NOT made
mock_client.post.assert_not_called()

# Extract call arguments
call_args = mock_client.post.call_args

# Get path (first positional arg)
path = call_args[0][0]

# Get body (second positional arg or 'json' keyword arg)
if len(call_args.args) > 1:
    body = call_args.args[1]
else:
    body = call_args.kwargs.get("data") or call_args.kwargs.get("json")

# Verify details
assert path == "/vcenter/resource"
assert body["name"] == "expected_value"
```

### Testing Check Mode

```python
def test_check_mode(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test operation in check mode."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    
    module_args.update({"param": "value"})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = True  # Enable check mode
    
    # Configure mock responses (for lookups)
    mock_client.get.return_value = _response(200, {"exists": True})
    
    # Execute module
    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()
    
    result = exc.value.kwargs
    assert result["changed"] is True
    
    # Verify no write operations occurred
    mock_client.post.assert_not_called()
    mock_client.delete.assert_not_called()
```

## Response Status Codes

Common HTTP status codes used in tests:

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, LIST, UPDATE operations |
| 201 | Created | Successful CREATE operation |
| 204 | No Content | Successful DELETE operation |
| 404 | Not Found | Resource doesn't exist |
| 400 | Bad Request | Invalid parameters (error testing) |
| 401 | Unauthorized | Authentication failed (error testing) |
| 403 | Forbidden | Permission denied (error testing) |
| 500 | Internal Server Error | Server error (error testing) |

## Example: Complete Test Function

```python
def test_create_datacenter(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a new datacenter."""
    # Setup: Inject mock client
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    # Setup: Configure module parameters
    module_args.update({
        "state": "present",
        "name": "my_datacenter",
        "folder": "group-d1",
    })
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Setup: Mock HTTP response
    create_response = "datacenter-1009"
    mock_client.post.return_value = _response(201, create_response)

    # Execute: Run the module
    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    # Verify: Check exit_json was called
    mock_module.exit_json.assert_called_once()
    
    # Verify: Check result values
    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "datacenter-1009"
    
    # Verify: Check API call was made
    mock_client.post.assert_called_once()
```

## Tips

1. **Always set `exit_json.side_effect`** - Otherwise the module won't raise `AnsibleExitJson`

2. **Use `side_effect` for multiple calls** - When the module makes multiple HTTP requests:
   ```python
   mock_client.get.side_effect = [response1, response2, response3]
   ```

3. **Check both positive and negative** - Test both `assert_called_once()` and `assert_not_called()`

4. **Extract call arguments carefully** - Different call styles use different argument positions

5. **Mock before execute** - Set up all `mock_client` responses before calling `module_under_test.main()`
