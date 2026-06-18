---
name: validate-module-api-compatibility
description: >-
  Validates whether an LLM-generated vmware.vmware_rest module is compatible
  with a vSphere API version other than its generation spec. Compares endpoints
  and HTTP methods used by the module against OpenAPI specs in
  config/api_specifications/. Updates module DOCUMENTATION notes when compatible.
  Use when asked to validate, check, or confirm module compatibility with a
  vSphere or API version (e.g. "will module X work with API version 8").
---

# Validate Module API Compatibility

Check whether an LLM-generated module in `plugins/modules/` is compatible with
a target vSphere API version, then annotate the module or report breaking changes.

## Inputs

| Input | Required | Example |
| --- | --- | --- |
| `module_name` | Yes | `vcenter_vm_storage_policy` |
| `target_api_version` | Yes | `8`, `8.0.2`, `vSphere 9` |

Resolve `target_api_version` to a directory under `config/api_specifications/`:

1. Strip non-numeric prefixes (`vSphere`, `API`, `version`).
2. If only a major version is given (e.g. `8`), pick the highest matching
   directory (e.g. `8.0.2` over `8.0.1`).
3. If no matching directory exists, stop and tell the user to fetch the spec
   with the `fetch-vsphere-openapi-spec` subagent.

## Workflow

```
Task Progress:
- [ ] Step 1: Load module and run pre-checks
- [ ] Step 2: Extract API usage from module
- [ ] Step 3: Compare source and target specs
- [ ] Step 4: Update notes or report breaking changes
```

### Step 1: Pre-checks (stop early when applicable)

Read `plugins/modules/<module_name>.py`.

**1a. LLM-generated gate**

The module must be LLM-generated. Confirm **both**:

- File header contains `This module is generated using LLM agents`
- `notes:` in `DOCUMENTATION` contains a line matching:
  `Generated from vSphere API spec <version>.`

If either is missing, tell the user the module was not LLM-generated and **stop**.
Do not compare specs or modify the file.

**1b. Source version**

Parse the generation version from the `Generated from vSphere API spec` note
(e.g. `9.1.0`). This is the **source spec version**.

**1c. Same major version**

If the source spec shares the same major version as the target (e.g. source
`9.1.0`, target `9.0.1`), tell the user the module is already generated against
that major version and **stop**.

**1d. Already annotated**

If `notes:` already contains a line matching
`Has support for vSphere API <version>.` where the version matches the resolved
target spec, tell the user compatibility is already documented and **stop**.

**1e. Source spec available**

Confirm `config/api_specifications/<source_version>/` exists. If not, stop and
ask the user to fetch it.

### Step 2: Extract API usage from module

Collect every REST operation the module performs:

| Source in module | What to extract |
| --- | --- |
| `PATH = "..."` or `*_PATH = "..."` constants | API path templates |
| `self.client.get/post/put/patch/delete(...)` | HTTP method per path |
| `PAYLOAD_FORMAT` | Request body fields sent per method |
| `argument_spec` / `choices` | Enum values the module may send |

Normalize paths to the form used in OpenAPI 3 specs (no `/api` prefix), e.g.
`/vcenter/vm/{vm}/storage/policy`.

Deduplicate path + method pairs. Ignore session/auth paths under `/rest/`.

### Step 3: Compare specs

Load specs from:

- **Source:** `config/api_specifications/<source_version>/`
- **Target:** `config/api_specifications/<target_version>/`

Use the spec resolution rules in [reference.md](reference.md) to pick the correct
JSON file per module prefix and normalize paths for Swagger 2 vs OpenAPI 3.

For each path + method pair from Step 2, compare the operation in both specs.
Apply the breaking-change criteria in [reference.md](reference.md).

Track every breaking change with: path, method, category, and a one-line
explanation the user can act on.

### Step 4: Outcome

**Compatible (no breaking changes):**

1. Add one line to the `notes:` list in `DOCUMENTATION` (do not remove existing
   notes):
   ```
   - Has support for vSphere API <target_version>.
   ```
   Use the resolved directory name exactly (e.g. `8.0.2`, not `8`).
2. Modify **only** the `notes:` section. Do not change module logic, `EXAMPLES`,
   or `RETURN`.
3. Summarize what was compared and that compatibility was confirmed.

**Incompatible (one or more breaking changes):**

1. Do **not** modify the module file.
2. Report each breaking change using the template in [reference.md](reference.md).
3. State that the module cannot be marked compatible until the breaking changes
   are resolved (regenerate from the target spec or adjust module logic).

## Write scope

- **May modify:** `notes:` entries inside `DOCUMENTATION` in
  `plugins/modules/<module_name>.py` — only when Step 4 confirms compatibility.
- **Must not modify:** module logic, `argument_spec`, tests, or any other file.

## Examples

**Request:** "Validate if `vcenter_vm_storage_policy` will work with API version 8"

1. Module notes say `Generated from vSphere API spec 9.1.0.` → proceed.
2. Resolve target to `8.0.2`.
3. Module uses `GET` and `PATCH` on `/vcenter/vm/{vm}/storage/policy`.
4. Path missing in `8.0.2` spec → breaking change, do not update notes.

**Request:** "Check `vcenter_datacenter` for vSphere 8 compatibility"

1. Module has no `Generated from vSphere API spec` note → stop, not LLM-generated.

## Additional resources

- [reference.md](reference.md) — spec file mapping, path normalization, breaking-change criteria, report template
- `.agents/subagents/generate-ansible-modules.md` — API spec resolution (authoritative for file layout)
- `.agents/references/vcf-spec-versions.yaml` — which vSphere majors have Broadcom-published specs
