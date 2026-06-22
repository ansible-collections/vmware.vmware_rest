# API Compatibility Reference

## Spec file resolution

Specs live under `config/api_specifications/<version>/`.

### OpenAPI 3 (vSphere 9.x)

| Module prefix | Spec file | Path prefix |
| --- | --- | --- |
| `vcenter` | `automation/vcenter.json` | `/vcenter/...` (no `/api`) |
| Other | Search all `*.json` under the version directory | varies |

### Swagger 2 (vSphere 6.7–8.x)

Map the module name prefix (text before the first `_`) to a spec file:

| Prefix | Spec file |
| --- | --- |
| `appliance` | `appliance.json` |
| `vcenter` | `vcenter.json` if present, else `api.json` |
| `content` | `content.json` |
| `cis` | `cis.json` |
| `esx` | `esx.json` |
| `stats` | `stats.json` |
| `vapi` | `vapi.json` |
| `hvc` | `hvc.json` |
| `session` | `session.json` |

Prefer paths under `/api/` over deprecated `/rest/` equivalents when both exist.

## Path normalization

When searching `paths` in a spec JSON file, try these variants in order:

1. Path as extracted from the module (e.g. `/vcenter/vm/{vm}/tools`)
2. With `/api` prefix (e.g. `/api/vcenter/vm/{vm}/tools`) — Swagger 2
3. Hyphenated last segments if not found (e.g. `resourcepool` → `resource-pool`)

Module code uses paths **without** host/scheme. The HTTP client adds
`https://{host}/api` when needed.

### Action endpoints (`?action=`)

Swagger 2 specs (vSphere 6.7–8.x) declare action operations as separate
paths, for example `/api/appliance/shutdown?action=poweroff`. When comparing
operations, match the **full path including the query string** before falling
back to the base path without query.

Modules pass actions via `query={"action": "..."}` on `POST` requests. The
batch script `.agents/scripts/validate_api_compatibility.py` resolves these
correctly.

## Batch validation script

Run compatibility checks across all LLM-generated modules:

```bash
# Report only
python3 .agents/scripts/validate_api_compatibility.py --target 7.0.3 --dry-run

# Validate and add notes to compatible modules
python3 .agents/scripts/validate_api_compatibility.py --target 8.0.2

# Single module
python3 .agents/scripts/validate_api_compatibility.py --target 7.0.3 appliance_networking
```

The script skips modules generated from the same major version as the target
and modules that already document support for the target version.

## Breaking changes

A module is **incompatible** with the target API version when any of the
following apply to a path + method the module uses:

| Category | Condition |
| --- | --- |
| **Missing endpoint** | Path not found in target spec `paths` (after normalization) |
| **Missing method** | Path exists but target has no operation for the HTTP method |
| **Path structure change** | Path template differs (parameter names, segment count, or segment names) |
| **Required body field added** | Target operation requires a request property the module never sends |
| **Body field removed or renamed** | Module sends a property via `PAYLOAD_FORMAT` that is absent or renamed in target request schema |
| **Parameter type change** | A body or query parameter the module uses changed type incompatibly (e.g. `string` → `object`) |
| **Enum mismatch** | Module `choices` includes a value not accepted by target schema `enum` |
| **Operation removed** | Target spec marks the operation deprecated/removed and no equivalent exists |

## Non-breaking changes (do not block compatibility)

- Description or summary text changes
- New optional request or response properties in target
- New HTTP response codes
- Additional enum values in target (module does not use them)
- Stricter validation that the module already satisfies

## Comparing request schemas

For each HTTP method the module uses:

1. Locate `requestBody` (OpenAPI 3) or `parameters` with `in: body` (Swagger 2)
   in **both** specs.
2. Resolve `$ref` schemas under `components/schemas` (OpenAPI 3) or
   `definitions` (Swagger 2).
3. Compare only properties the module sends (from `PAYLOAD_FORMAT` body mapping
   and `build_payload` usage).
4. Check `required` arrays: every target-required property must be mappable from
   module params.

## Comparing response schemas

Response shape differences are **informational only** for this skill unless the
module parses a field that was removed or renamed in the target — in that case
report as a breaking change under **Body field removed or renamed**.

## Report template (incompatible)

```markdown
## Compatibility result: INCOMPATIBLE

**Module:** `<module_name>`
**Generated from:** vSphere API `<source_version>`
**Target:** vSphere API `<target_version>`

### Breaking changes

1. **[Missing endpoint]** `PATCH /vcenter/vm/{vm}/storage/policy`
   — path not present in `config/api_specifications/<target_version>/` spec.

2. **[Enum mismatch]** `POST /vcenter/vm/{vm}/tools` — module sends
   `upgrade_policy: MANUAL`; target enum only allows `AUTOMATIC`.

### Recommendation

Regenerate the module from the target API spec or adjust module logic to match
the target operation definitions.
```

## Report template (compatible)

```markdown
## Compatibility result: COMPATIBLE

**Module:** `<module_name>`
**Generated from:** vSphere API `<source_version>`
**Target:** vSphere API `<target_version>`

Compared N operation(s) across M path(s). No breaking changes found.

Added note: `Has support for vSphere API <target_version>.`
```
