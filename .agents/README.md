# AI agent definitions

This directory contains subagent definitions and reference scaffolds for
generating `vmware.vmware_rest` Ansible modules from vSphere OpenAPI
specifications.

## Quick start

Ask the AI:

> Generate `vcenter_resourcepool` modules from vSphere API 9.

The **`orchestrate-module-generation`** subagent coordinates the full pipeline.

## Pipeline

| Step | Subagent | Output |
| --- | --- | --- |
| 1. Fetch spec | `fetch-vsphere-openapi-spec` | `config/api_specifications/<version>/` |
| 2. Generate modules | `generate-ansible-modules` | `plugins/modules/<name>.py` |
| 2b. Validate docs (structural) | `validate-module-documentation` | read-only report |
| 3. Phase 1 — unit gate | `generate-unit-tests` (`mode: generate`) | `tests/unit/plugins/modules/test_<name>.py` |
| 4. Iterate Phase 1 | orchestrator relays `module_error` → step 2 | until unit tests pass |
| 5. Phase 2 — integration | `generate-integration-tests` | `tests/integration/targets/<name>/` |
| 5b. Validate docs (integration) | `validate-module-documentation` | EXAMPLES/RETURN vs tests |
| 6. Iterate Phase 2 | orchestrator relays `module_error` / `doc_corrections_needed` → step 2 → step 5 | until integration pass |
| 7. Phase 3 — regression | `generate-unit-tests` (`mode: verify`) | re-run `make units` |
| 8. Next batch | repeat for next resource (≤2 modules per batch) | |

## Subagents

| Name | Definition | Write scope |
| --- | --- | --- |
| `orchestrate-module-generation` | [subagents/orchestrate-module-generation.md](subagents/orchestrate-module-generation.md) | coordinates only |
| `fetch-vsphere-openapi-spec` | [subagents/fetch-vsphere-openapi-spec.md](subagents/fetch-vsphere-openapi-spec.md) | `config/api_specifications/` |
| `generate-ansible-modules` | [subagents/generate-ansible-modules.md](subagents/generate-ansible-modules.md) | `plugins/modules/` |
| `generate-unit-tests` | [subagents/generate-unit-tests.md](subagents/generate-unit-tests.md) | `tests/unit/` |
| `generate-integration-tests` | [subagents/generate-integration-tests.md](subagents/generate-integration-tests.md) | `tests/integration/` |
| `validate-module-documentation` | [subagents/validate-module-documentation.md](subagents/validate-module-documentation.md) | read-only |

Cursor copies live in `.cursor/agents/`.

## Reference scaffolds

| Path | Purpose |
| --- | --- |
| `references/modules/info.py` | Info module template |
| `references/modules/crud.py` | CRUD module template |
| `references/tests/unit_module.py` | Unit test template |
| `references/tests/integration_target/` | Integration target template (MockServer + prepare_simulator) |
| `references/vcf-spec-versions.yaml` | vSphere major → VCF spec mapping |

## Iteration loop

When unit tests fail, the test subagent classifies each failure:

- **test_error** — fixed by the test subagent (syntax, mocks, assertions)
- **module_error** — reported to the orchestrator, which re-invokes the module
  subagent with `correction_feedback`

The API spec is the source of truth. Tests reflect the spec; modules are fixed
to match the spec, not the other way around.

## Running tests manually

From the repository root:

```bash
make units
```

Single unit test file:

```bash
make units UNIT_TARGETS='tests/unit/plugins/modules/test_<module_name>.py'
```

Integration target (MockServer simulator):

```bash
make integration INTEGRATION_TARGETS=<target_name>
```

First-time integration setup:

```bash
make install-integration-reqs
```

The `integration` target installs the collection, sets `ANSIBLE_ROLES_PATH`, and
runs `ansible-test integration` — do not run those steps manually unless
`make` is unavailable.
