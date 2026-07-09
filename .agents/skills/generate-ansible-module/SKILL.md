---
name: generate-ansible-module
description: >
  Generate or regenerate Ansible modules for the vmware.vmware_rest collection.
  Use when creating a new module or updating an existing module from API specifications.
category: "code-generation"
subcategory: "ansible"
---

# Generate Ansible Module

This skill generates or regenerates Ansible modules for the vmware.vmware_rest collection from VMware vSphere API specifications. It orchestrates the complete generation workflow from bare-bones module creation through documentation enrichment, formatting, and sanity checks.

## Overview

Module generation is a multi-step process that:
1. Generates the module skeleton from API specifications
2. Enriches and validates documentation
3. Formats code to collection standards
4. Runs sanity tests to catch issues

This skill coordinates these steps and reports any issues that require user intervention.

## When to Use

**Use this skill when:**
- Creating a new module from scratch
- Regenerating an existing module after API spec updates
- Updating a module to use new base classes or patterns

**Prerequisites:**
- The module name must correspond to a valid vSphere API endpoint
- API specification files must be available in the expected location
- The module name must follow the collection naming pattern (e.g., `vcenter_resourcepool`, `vcenter_datacenter_info`)

## Required Parameters

### module_name (required)

The name of the module to generate. Must follow these conventions:
- Use snake_case format
- Start with the API namespace (typically `vcenter_`, `appliance_`, etc.)
- For info modules, end with `_info` suffix
- Match an existing API endpoint path

**Examples:**
- `vcenter_resourcepool` - CRUD module for resource pools
- `vcenter_resourcepool_info` - Info module for resource pools
- `vcenter_datacenter` - CRUD module for datacenters
- `appliance_monitoring_query` - Action module for monitoring queries

### spec_version (optional)

The vSphere API specification version to use. Defaults to `9.1.0` if not specified.

**Available versions:**
- `9.1.0` (default)
- `9.0.0`
- `8.0.2`
- `8.0.1`
- Earlier versions may be available

**When to specify:**
- Targeting a specific API version for compatibility
- Testing against older API specifications
- Working with modules for specific vSphere versions

## Step-by-Step Workflow

**Important:** Steps 1 and 2 can be run from any directory, but Steps 3 and 4 should be run from the project root directory.

## Multiple Module Generation

**When generating multiple modules**, complete each step for ALL requested modules before proceeding to the next step:

1. **Step 1 (Generate Base Modules)**: Generate base modules for ALL requested modules first
2. **Step 2 (Enrich Documentation)**: Enrich documentation for ALL modules
3. **Step 3 (Format Modules)**: Format ALL modules with black
4. **Step 4 (Run Sanity Tests)**: Run sanity tests ONCE (tests all modules in the collection)

This workflow ensures:
- Dependencies between modules are handled correctly
- Batch operations are more efficient
- Sanity tests validate the entire collection state at once

**Example for multiple modules:**
```bash
# Step 1: Generate all base modules
python generate_module.py vcenter_resourcepool --spec-version 9.1.0
python generate_module.py vcenter_datacenter --spec-version 9.1.0
python generate_module.py vcenter_vm_info --spec-version 9.1.0

# Step 2: Enrich documentation for all modules (invoke skill for each)
# Step 3: Format all modules
black plugins/modules/vcenter_resourcepool.py plugins/modules/vcenter_datacenter.py plugins/modules/vcenter_vm_info.py

# Step 4: Run sanity tests once for the entire collection
make sanity
```

### Step 1: Generate Base Module

Run the module generation script (can be run from `content_generation/` directory or project root):

```bash
# From content_generation directory
cd content_generation
python generate_module.py <module_name> [--spec-version <version>]

# OR from project root
python content_generation/generate_module.py <module_name> [--spec-version <version>]
```

**Example:**
```bash
cd content_generation
python generate_module.py vcenter_resourcepool --spec-version 9.1.0
```

**For Multiple Modules:** Generate ALL requested modules in this step before proceeding to Step 2. Run the generation script once for each module.

**Expected Outcome:**
- Module file created at `plugins/modules/<module_name>.py`
- Module contains all operation configurations
- Documentation sections have PLACEHOLDER text
- Code is syntactically valid Python

**If Errors Occur:**

Generation errors at this stage are **NOT EXPECTED** and indicate one of:
- Invalid module name (no matching API endpoint)
- Missing or corrupt API specification files
- Bug in the generation script

**DO NOT attempt to fix these errors.** Instead:
1. Stop immediately
2. Report the exact error message to the user
3. Ask for guidance on how to proceed

The generation script should handle all valid module names without errors. If it fails, the user needs to investigate the root cause.

### Step 2: Enrich Module Documentation

Use the `ansible-module-doc-review` skill to improve the module documentation:

```bash
# This is done by invoking the skill, not running a command
```

The skill will:
- Replace PLACEHOLDER text with meaningful descriptions
- Create realistic usage examples
- Complete the RETURN documentation
- Ensure all option descriptions are clear

**For Multiple Modules:** Enrich documentation for ALL modules in this step before proceeding to Step 3. Invoke the skill once for each module.

**What Gets Updated:**
- `DOCUMENTATION.short_description` - Concise module purpose
- `DOCUMENTATION.description` - Detailed explanation
- `DOCUMENTATION.options` - Clear parameter descriptions
- `EXAMPLES` - Realistic usage demonstrations
- `RETURN` - Complete return value documentation

**Validation:**
After the skill completes, verify:
- No PLACEHOLDER text remains
- Examples are valid YAML
- RETURN section matches module type (INFO vs CRUD)

### Step 3: Format the Module

Apply the `black` Python formatter using the exact version from `linters.requirements.txt`:

```bash
# First, check the required black version
cat linters.requirements.txt | grep black

# Format the module (use full path or ensure you're in project root)
black plugins/modules/<module_name>.py
# OR
black /full/path/to/vmware.vmware_rest/plugins/modules/<module_name>.py
```

**For Multiple Modules:** Format ALL modules in this step. You can format multiple files in a single black command:
```bash
black plugins/modules/vcenter_resourcepool.py plugins/modules/vcenter_datacenter.py plugins/modules/vcenter_vm_info.py
# OR format all modules at once
black plugins/modules/
```

**Expected Outcome:**
- Code is formatted to PEP 8 standards
- Consistent indentation and spacing
- Line lengths within limits
- Black reports "X file(s) reformatted" or "X file(s) left unchanged"

**Note:** Black version must match the version in `linters.requirements.txt` to ensure consistent formatting across the project. Currently: `black>=24.0`

### Step 4: Run Sanity Tests

Execute Ansible's sanity test suite from the project root directory:

```bash
# Ensure you're in the project root
cd /path/to/vmware.vmware_rest

# Run sanity tests
make sanity
```

**Important:** The `make sanity` command must be run from the project root directory where the `Makefile` is located, not from subdirectories like `content_generation/` or `plugins/modules/`.

**For Multiple Modules:** Sanity tests only need to be run **once** after completing Steps 1-3 for all modules, as the command validates all modules in the entire collection.

**What This Tests:**
- Module imports cleanly
- Documentation structure is valid
- Code follows Ansible development guidelines
- No common Python errors
- All modules in the collection pass validation

**Expected Outcome:**
- All sanity tests pass
- No errors or warnings reported

**If Sanity Tests Fail:**

Sanity test failures are **COMMON** and usually indicate:
- Documentation formatting issues
- Missing or incorrect metadata
- Import problems
- Code style violations

**DO NOT attempt to fix sanity test failures automatically.** Instead:
1. Capture the complete error output
2. Report the failures to the user with:
   - The specific tests that failed
   - The exact error messages
   - The file and line numbers if provided
3. Ask the user how they want to proceed

Common sanity failures might include:
- `validate-modules` - Documentation structure errors
- `import` - Module import failures
- `compile` - Python syntax errors
- `pep8` - Style violations (should be rare after black formatting)

## Success Criteria

The module generation is complete and successful when:

1. ✅ Module file exists at `plugins/modules/<module_name>.py`
2. ✅ No PLACEHOLDER text in documentation
3. ✅ Examples section has valid, realistic examples
4. ✅ RETURN section is complete and accurate
5. ✅ Code is formatted with black
6. ✅ All sanity tests pass

If all criteria are met, report success to the user with:
- The module file location
- A summary of what was generated
- Confirmation that all tests passed

## Error Handling

### Generation Script Errors

**Symptoms:**
- Script exits with non-zero status
- Error message about missing endpoints, invalid spec, or generation failure

**Action:**
1. **STOP** - Do not proceed to next steps
2. Report the error to the user verbatim
3. Ask for guidance - these are unexpected errors

**Do Not:**
- Attempt to fix the generation script
- Try alternative approaches
- Modify API specification files

### Documentation Skill Issues

**Symptoms:**
- Skill cannot determine module type
- Cannot find appropriate examples
- Unclear what documentation to write

**Action:**
1. Review the generated module to understand its structure
2. Report specific issues to the user
3. Ask for clarification on module purpose or expected behavior

### Formatting Errors

**Symptoms:**
- Black reports syntax errors
- Black cannot parse the file

**Action:**
1. This indicates a generation bug - the module should be valid Python
2. Report the syntax error to the user
3. Ask whether to proceed with sanity tests anyway

### Sanity Test Failures

**Symptoms:**
- `make sanity` exits with non-zero status
- One or more sanity tests report failures

**Action:**
1. Capture the complete output
2. Report all failures to the user
3. **DO NOT** attempt fixes
4. Ask how the user wants to proceed

Common fixable issues (user may want you to fix):
- Missing newline at end of file
- Trailing whitespace
- Minor documentation formatting

Complex issues (user should investigate):
- Import failures
- Invalid documentation structure
- Module metadata problems

## Example: Complete Generation

**User Request:**
> Generate the vcenter_resourcepool module

**Agent Workflow:**

```bash
# Navigate to project root
cd /home/mimorenc/git/vmware.vmware_rest

# Step 1: Generate base module
cd content_generation
python generate_module.py vcenter_resourcepool --spec-version 9.1.0
# ✅ Success: Module created at plugins/modules/vcenter_resourcepool.py

# Step 2: Enrich documentation
# Invoke ansible-module-doc-review skill
# ✅ Success: Documentation completed, no PLACEHOLDER text

# Step 3: Format code
cd /home/mimorenc/git/vmware.vmware_rest
black plugins/modules/vcenter_resourcepool.py
# ✅ Success: 1 file reformatted

# Step 4: Run sanity tests (from project root)
make sanity
# ✅ Success: All tests passed

# Report to user
```

**Agent Response:**
> Successfully generated the vcenter_resourcepool module at plugins/modules/vcenter_resourcepool.py.
>
> Completed steps:
> - ✅ Generated base module from API spec 9.1.0
> - ✅ Enriched documentation (no placeholders remain)
> - ✅ Formatted with black 24.0
> - ✅ All sanity tests passed
>
> The module is ready for review and use.

## Example: Generation with Error

**User Request:**
> Generate the vcenter_invalid_resource module

**Agent Workflow:**

```bash
# Step 1: Generate base module
python content_generation/generate_module.py vcenter_invalid_resource --spec-version 9.1.0
# ❌ Error: No endpoints found for module vcenter_invalid_resource
```

**Agent Response:**
> The module generation failed with the following error:
>
> ```
> Error: No endpoints found for module vcenter_invalid_resource
> ```
>
> This error indicates that 'vcenter_invalid_resource' does not correspond to a known vSphere API endpoint in spec version 9.1.0.
>
> This is an unexpected error at the generation stage. How would you like me to proceed?
>
> Possible next steps:
> - Verify the module name is correct
> - Check if the endpoint exists in a different API version
> - Check if the API specification files are up to date

## Example: Sanity Test Failure

**Agent Workflow:**

```bash
# Steps 1-3 complete successfully
# Step 4: Run sanity tests
make sanity
# ❌ Failed with errors
```

**Agent Response:**
> Module generation completed through formatting, but sanity tests failed with the following errors:
>
> ```
> ERROR: plugins/modules/vcenter_resourcepool.py:0:0: invalid-documentation:
>        DOCUMENTATION.options.parent.description must be a list
>
> ERROR: plugins/modules/vcenter_resourcepool.py:0:0: validate-modules:missing-required-return-doc:
>        Missing return documentation for: id
> ```
>
> These sanity test failures need to be addressed before the module is complete. The issues are:
>
> 1. The 'parent' option description should be a list, not a string
> 2. The 'id' return value is missing from RETURN documentation
>
> How would you like me to proceed? I can:
> - Fix these specific issues if you'd like
> - Leave them for you to review and fix manually
> - Investigate further to understand the root cause

## Common Module Patterns

### INFO Module
- Name ends with `_info`
- Generates `GET_OPERATION` and `LIST_OPERATION`
- RETURN includes: `id`, `value`, `info` (Hint: is the module name states with `appliance_`, the `id` value will never be returned)
- No `state` parameter

### CRUD Module
- Name does not end with `_info`
- May generate: `GET_OPERATION`, `LIST_OPERATION`, `CREATE_OPERATION`, `UPDATE_OPERATION`, `DELETE_OPERATION`
- RETURN includes: `id` (Hint: is the module name states with `appliance_`, the `id` value will never be returned)
- Has `state` parameter with choices: `present`, `absent`, and possibly actions

### Action Module
- Has additional action endpoints beyond standard CRUD
- Generates `ACTION_OPERATIONS` dictionary
- State choices include action names (e.g., `clone`, `relocate`)

## Files and Locations

| Path | Purpose |
|------|---------|
| `content_generation/generate_module.py` | Module generation script |
| `plugins/modules/<module_name>.py` | Generated module output |
| `linters.requirements.txt` | Required formatter versions |
| `.agents/skills/ansible-module-doc-review/` | Documentation enrichment skill |
| API spec files | Source of endpoint and parameter definitions |

## Troubleshooting

### "Module name too generic"
Some module names might conflict with Ansible's reserved words or common terms. Add specificity (e.g., use `vcenter_vm_info` instead of `vm_info`).

### "Cannot find API spec file"
Verify the module name matches the API structure. The script determines which spec file to use based on the module name pattern.

### "Documentation skill cannot find module"
Ensure Step 1 completed successfully and the module file exists at the expected path.

### "Black version mismatch"
Verify you're using the black version specified in `linters.requirements.txt`. Install it with:
```bash
pip install -r linters.requirements.txt
```

### "make: *** No rule to make target 'sanity'"
This error means you're not in the project root directory. The `make sanity` command requires the `Makefile` which is only in the project root:
```bash
# Navigate to project root first
cd /path/to/vmware.vmware_rest
# Then run sanity tests
make sanity
```

## Best Practices

1. **Always specify spec version explicitly** even if using the default - this makes regeneration reproducible
2. **Review generated documentation** before proceeding to formatting - it's easier to fix issues in the text than after formatting
3. **Run sanity tests** even if you expect them to fail - the output provides valuable feedback
4. **Report all errors to the user** - don't hide or try to work around unexpected failures
5. **Keep the user informed** at each step - generation can take time, and users appreciate progress updates

## Limitations

- Can only generate modules for API endpoints that exist in the spec
- Cannot generate custom logic beyond what the base classes provide
- Documentation quality depends on API spec quality
- Some edge cases may require manual code adjustments after generation

## Next Steps After Generation

Once a module is successfully generated:

1. **Review the code** - Ensure operation configs are correct
2. **Test manually** - Try the module against a real or mock vSphere instance
3. **Generate integration tests** - Use the `generate-integration-tests` skill
4. **Add to git** - Commit the new module
5. **Update changelog** - Document the new module in the collection changelog

## Resources

- **Module Generation Script**: `content_generation/generate_module.py`
- **Base Module Classes**: `plugins/module_utils/_crud_module.py`, `plugins/module_utils/_info_module.py`
- **Operation Configs**: `plugins/module_utils/_operation_configs.py`
- **Existing Modules**: Browse `plugins/modules/` for examples
- **API Specifications**: Check what versions are available in the spec directory
