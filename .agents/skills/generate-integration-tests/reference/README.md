# Reference Files for Integration Test Generation

This directory contains reference patterns and examples for generating integration tests.

## Files

### Test Patterns

These YAML files show the standard test patterns for each operation type. Use them as templates when creating integration tests:

- **`info_tests_pattern.yml`** - Pattern for info module tests (LIST and GET operations)
- **`create_tests_pattern.yml`** - Pattern for CREATE operation tests
- **`update_tests_pattern.yml`** - Pattern for UPDATE operation tests
- **`delete_tests_pattern.yml`** - Pattern for DELETE operation tests

Each pattern includes:
- Placeholder syntax (e.g., `<module_name>`, `<resource_id>`)
- Mock state management
- Assertion examples
- Check mode test scenarios

### Examples

- **`example_module_analysis.md`** - Shows how to analyze module files to determine:
  - Module type (CRUD vs Info)
  - Supported operations
  - Module parameters
  - Operation IDs
  - What test files to create
  - Includes examples for different module types

- **`complete_example.md`** - Complete working example showing:
  - All generated files for vcenter_datacenter
  - Complete file contents
  - Test results
  - Coverage summary

## Usage

When generating integration tests:

1. **Start with analysis**: Read `example_module_analysis.md` to understand what to look for in the module files

2. **Use patterns**: Copy the appropriate pattern files and replace placeholders with actual values from your module

3. **Reference complete example**: Check `complete_example.md` to see how everything fits together

4. **Validate**: Compare your generated tests against the patterns to ensure consistency

## Quick Reference

### Placeholder Conventions

- `<module_name>` - Base module name (e.g., `vcenter_datacenter`)
- `<resource_plural>` - Plural form of resource (e.g., `datacenters`)
- `<moid_attribute>` - Resource identifier field (e.g., `datacenter`)
- `<resource_id>` - Example resource ID (e.g., `datacenter-1001`)
- `<OperationId>` - API operation ID prefix (e.g., `Vcenter.Datacenter`)
- `<param_*>` - Module parameters
- `<field_*>` - Resource fields returned by API

### Common Operation IDs

- List: `<OperationId>_list`
- Get: `<OperationId>_get`
- Create: `<OperationId>_create`
- Update: `<OperationId>_update`
- Delete: `<OperationId>_delete`

### Mock States

- `default.json` - Empty state, no resources exist
- `created.json` - Resource exists
- `list_multiple.json` - Multiple resources exist
- `updated.json` - Resource updated (if UPDATE supported)
