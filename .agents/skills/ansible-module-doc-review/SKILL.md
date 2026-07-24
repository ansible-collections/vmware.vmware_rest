---
name: ansible-module-doc-review
description: >
  Review and enrich Ansible module documentation to ensure completeness and quality.
  Use when a module needs documentation improvements or validation.
category: "documentation"
subcategory: "ansible"
---

# Ansible Module Documentation Review

Ansible modules require comprehensive documentation in specific sections (DOCUMENTATION, EXAMPLES, RETURN) to help users understand what the module does and how to use it. This skill validates completeness and helps fill in missing or placeholder content.

## When to Apply

**Apply this technique when:**
- A module has PLACEHOLDER text in its documentation
- Creating a new module that needs documentation
- Reviewing an existing module for documentation quality
- Updating a module after API changes

**Skip this technique when:**
- The module already has complete, validated documentation
- Working on internal/utility modules not exposed to users
- Making code-only changes that don't affect the module's behavior

## Documentation Requirements

### Required Sections

All modules must have these documentation sections properly filled out:

| Section | Purpose |
|---------|---------|
| **short_description** | 1-2 sentences describing what the module does |
| **description** | 2-5 sentences with more detail about module functionality |
| **EXAMPLES** | Valid YAML showing how to use the module in Ansible tasks |
| **RETURN** | YAML dictionary documenting values returned by the module |

### Section Details

#### DOCUMENTATION.short_description

A concise 1-2 sentence summary of what the module does.

**Examples:**
- "Manage vCenter resource pools."
- "Gather information about appliance monitoring."

#### DOCUMENTATION.description

A list of 2-5 sentences describing the module in more detail. Should cover:
- What the module manages or queries
- Key capabilities or operations
- Important context about the resource type

#### DOCUMENTATION.options

Review all option descriptions to ensure they:
- Explain in plain terms what the option does or means
- Avoid technical jargon where possible
- Clearly state the purpose and effect of the option
- Include relevant API context where helpful

#### EXAMPLES Section

Must be valid YAML showing Ansible tasks that demonstrate module usage.

**Requirements:**
- Use fully qualified module name: `vmware.vmware_rest.<module_name>`
- Show different options and use cases
- Comply with option requirements and types
- Be executable examples that would actually work

**For INFO modules:**
- Show a minimal example
- Show an example with more parameters

**For CRUD modules:**
- Showcase different states (present, absent)
- Show a simple example
- Show a more complex example with additional options

**Example structure:**
```yaml
- name: Create a resource pool
  vmware.vmware_rest.vcenter_resourcepool:
    name: my-resource-pool
    parent: resgroup-1001
    state: present

- name: Delete a resource pool
  vmware.vmware_rest.vcenter_resourcepool:
    resource_pool: resgroup-1009
    state: absent
```

**Note:** Do not include connection parameters (vcenter_hostname, vcenter_username, vcenter_password) in examples - they are implied through the connection_params documentation fragment.

#### RETURN Section

Must be a valid YAML dictionary documenting return values.

**Do NOT document:**
- The `changed` key (standard Ansible return value)
- The `diff` key (standard Ansible return value)

**Each return value must have:**
- **description**: A sentence about what the return value represents
- **returned**: When the value is returned (e.g., "On success", "When state is present")
- **type**: Python type (str, dict, list, int, bool)
- **sample**: Example output (consult API spec for realistic samples)

**For INFO modules:**

(Hint: is the module name states with `appliance_`, the `id` value will never be returned)

The return structure for info modules always includes:

```yaml
id:
  description: MOID of the queried resource
  returned: When only one resource, with a MOID, was queried
  sample: resgroup-1009
  type: str

value:
  description:
    - Detailed information about a single resource.
    - Dict if only one item was found, list otherwise
    - Maintained for backwards compatibility. Use the info return value if possible.
  returned: On success
  sample:
    description: ntpd.service
    state: STARTED
  type: dict

info:
  description: A list of detailed information about resources
  returned: On success
  sample:
    - description: ntpd.service
      state: STARTED
  type: list
```

**For CRUD modules:**

(Hint: is the module name states with `appliance_`, the `id` value will never be returned)

```yaml
id:
  description: MOID of the managed resource
  returned: When state is present, or when a resource is deleted, or when state is set to a supported action
  sample: resgroup-1009
  type: str
```

## Step-by-Step Review Process

### Step 1: Identify the Module Type

Determine if the module is:
- **INFO module**: Gathers information (ends with `_info`)
- **CRUD module**: Creates/updates/deletes resources (has `state` parameter)

This determines the expected RETURN structure.

### Step 2: Review DOCUMENTATION Section

Check and complete:

1. **short_description**: Should be concise and clear
2. **description**: Should be 2-5 sentences providing detail
3. **options**: Each option should have a clear, plain-language description
4. Are all lines 160 characters or less?

Look for:
- PLACEHOLDER text
- Vague or unclear descriptions
- Missing context about what options do

### Step 3: Review EXAMPLES Section

Verify the examples:

1. Are they valid YAML?
2. Do they use the fully qualified module name?
3. Do they demonstrate different use cases appropriately?
4. For CRUD modules: Do they show different states?
5. For INFO modules: Do they show both simple and complex queries?
6. Are the examples realistic and executable?

### Step 4: Review RETURN Section

Check return value documentation:

1. For INFO modules: Verify `id`, `value`, and `info` are documented (Hint: is the module name states with `appliance_`, the `id` value will never be returned)
2. For CRUD modules: Verify `id` is documented (Hint: is the module name states with `appliance_`, the `id` value will never be returned)
3. Ensure each return value has description, returned, type, and sample
4. Verify samples are realistic (check API spec if needed)

### Step 5: Consult API Endpoints

For context and validation:

1. Review the module's operation config definitions in `plugins/module_utils/_operation_configs.py`
2. Check API endpoint specifications for:
   - Available parameters and their meanings
   - Expected return value structures
   - Sample response data

### Step 6: Make Improvements

Apply improvements to the module documentation:

1. Replace PLACEHOLDER text with meaningful content
2. Clarify unclear option descriptions
3. Add or improve examples
4. Complete or fix RETURN documentation
5. Ensure consistency with collection standards

### Step 7: Validate Documentation

Validate that the documentation is syntactically correct and follows formatting standards:

1. **Run ansible-doc validation**: From the repository root, run:
   ```bash
   PAGER=cat ansible-doc -t module -M plugins/modules/ <module_name>
   ```
   This command should exit with code 0, indicating the documentation is valid YAML and can be parsed correctly.

2. **Check for errors**: If the command exits with a non-zero code, it indicates:
   - Invalid YAML syntax in DOCUMENTATION, EXAMPLES, or RETURN
   - Malformed documentation structure
   - Missing required sections

   Review the error output and fix any issues before proceeding.

3. **Verify line length**: Ensure all lines in the DOCUMENTATION, EXAMPLES, and RETURN sections are 160 characters or less. Long lines should be wrapped appropriately while maintaining YAML validity.

## Common Patterns

### Pattern: Reviewing Option Descriptions

**Situation:** Option descriptions are too technical or unclear

**Before:**
```yaml
parent:
  description:
  - Parent of the created resource pool.
  - When clients pass a value of this schema as a parameter...
```

**After:**
```yaml
parent:
  description:
  - The parent resource pool under which to create this resource pool.
  - Must be the MOID (managed object identifier) of an existing ResourcePool.
```

### Pattern: Creating Realistic Examples

**Situation:** Need to show both simple and complex usage

**For CRUD module:**
```yaml
# Simple example - create with minimal options
- name: Create a basic resource pool
  vmware.vmware_rest.vcenter_resourcepool:
    name: my-pool
    parent: resgroup-1001
    state: present

# Complex example - create with resource limits
- name: Create resource pool with CPU and memory limits
  vmware.vmware_rest.vcenter_resourcepool:
    name: limited-pool
    parent: resgroup-1001
    cpu_allocation:
      reservation: 1000
      limit: 4000
    memory_allocation:
      reservation: 512
      limit: 2048
    state: present
```

**Note:** Connection parameters are omitted from examples as they are implied.

## Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Copying API docs verbatim | API docs are too technical for Ansible users | Translate to plain language explaining what users accomplish |
| Leaving PLACEHOLDER text | Users can't understand what module does | Write clear descriptions based on module purpose |
| Examples without fully qualified names | Users don't know which collection | Always use `vmware.vmware_rest.module_name` |
| Including connection params in examples | Creates clutter, params are implied | Omit vcenter_hostname, vcenter_username, vcenter_password |
| Missing `state` in CRUD examples | Examples won't work | Always include `state: present` or `state: absent` |
| No sample data in RETURN | Users don't know what to expect | Provide realistic sample output from API |
| Incomplete RETURN "returned" for CRUD | Unclear when id is returned | Use "When state is present, or when a resource is deleted, or when state is set to a supported action" |

## Validation Checklist

Before considering documentation complete, verify:

- [ ] No PLACEHOLDER text remains
- [ ] short_description is 1-2 clear sentences
- [ ] description has 2-5 detail sentences
- [ ] All option descriptions are clear and user-friendly
- [ ] EXAMPLES section has valid YAML
- [ ] EXAMPLES use fully qualified module names
- [ ] EXAMPLES demonstrate appropriate use cases for module type
- [ ] RETURN section matches module type (INFO vs CRUD)
- [ ] All return values have description, returned, type, and sample
- [ ] Sample data in RETURN is realistic
- [ ] `PAGER=cat ansible-doc -t module -M plugins/modules/ <module_name>` exits with code 0
- [ ] All documentation lines are 160 characters or less in length

## Resources

### Internal Files

- **plugins/module_utils/_operation_configs.py**: Operation configurations showing API endpoints used by modules
- **plugins/modules/*.py**: Existing modules with documentation examples
- Module type determination: Check for `_info` suffix or `state` parameter

### API References

- vSphere API documentation for understanding resource types and operations
- OpenAPI/Swagger specs for endpoint details and response schemas

### Ansible Documentation Standards

- [Ansible Module Documentation](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html)
- Ansible documentation fragment reuse (see `extends_documentation_fragment` in modules)
