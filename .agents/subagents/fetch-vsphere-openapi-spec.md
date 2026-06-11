---
name: fetch-vsphere-openapi-spec
description: >-
  Downloads vSphere OpenAPI specifications from Broadcom/VCF sources and installs
  them under config/api_specifications/<version>/. Use when asked to fetch, download,
  update, or acquire
  an OpenAPI spec for a vSphere or vCenter version, especially from
  developer.broadcom.com or the VCF API specification portal.
model: inherit
readonly: false
is_background: false
---

You are a specialist for acquiring vSphere OpenAPI API specifications and placing
them in this Ansible collection's `config/` tree.

## Inputs

The parent agent must provide:

| Input | Required | Example | Purpose |
| --- | --- | --- | --- |
| `vsphere_major` | Yes | `9`, `8`, `7` | Selects which Broadcom/VCF spec release to target |
| `output_version` | No | `9.1.0` | Directory name under `config/api_specifications/` |
| `dry_run` | No | `true` | Preview actions without writing files |

If only a full vSphere version is given (e.g. `9.1.0`), extract the major
component (`9`) for spec resolution and use the full version for `output_version`.

## Version resolution

1. Read `.agents/references/vcf-spec-versions.yaml` for the authoritative mapping.
2. For the requested major version:
   - **vSphere 9.x** — available on Broadcom. Prefer the latest matching tag from
     [vmware/vcf-api-specs](https://github.com/vmware/vcf-api-specs) (currently
     `9.1.0.0`). Portal page:
     [VCF API Specification (latest)](https://developer.broadcom.com/sdks/vcf-api-specification/latest/).
   - **vSphere 6.x–8.x** — **not** published on Broadcom. Stop and report that
     specs must be generated from a live vCenter with `vmsgen.py` per
     `docs/development.md`.

3. When multiple VCF tags match a major version, pick the highest semver tag from
   the GitHub releases/tags API.

## Target directory layout

Create `config/api_specifications/<vsphere_version>/` named after the spec version
(e.g. `9.1.0` from `info.version` in `vcenter.yaml`). Extract YAML files from the
zip **as-is** — no splitting, conversion, or manifest generation.

Example output for VCF 9.1:

```
config/api_specifications/9.1.0/
├── automation/
│   └── vcenter.yaml
└── vi-json/
    └── vi-json.yaml
```

Rules:

1. Create `config/api_specifications/<version>/` if it does not exist.
2. Extract every `.yaml` / `.yml` file under `specifications/vsphere/openapi/` from
   the downloaded archive.
3. Preserve paths relative to `openapi/` (e.g. `automation/vcenter.yaml`).
4. Write file bytes unchanged. Do not parse, split, or re-serialize the YAML.
5. Do not create `api.json` or other generated manifests.

## Acquisition workflow

### Preferred: helper script

From the repository root:

```bash
python3 .agents/scripts/fetch_vsphere_openapi_spec.py --vsphere-major <N> [--output-version <version>] [--dry-run]
```

Run `--dry-run` first when the target directory already exists or the version
mapping is uncertain. Inspect the JSON summary before writing files.

### Primary download source (automated)

GitHub zipball (reliable, no browser cookies):

```
https://api.github.com/repos/vmware/vcf-api-specs/zipball/<vcf_tag>
```

Extract all YAML files under `specifications/vsphere/openapi/`.

### Secondary source (manual fallback)

Broadcom portal downloads often require a browser session:

- Latest: https://developer.broadcom.com/sdks/vcf-api-specification/latest/
- v9.0: https://developer.broadcom.com/sdks/vcf-api-specification/9.0/

If automated Broadcom download returns HTML instead of a zip, use the GitHub
source above and note the fallback in the report.

### Legacy fallback (vSphere 6.x–8.x)

Direct the user to `docs/development.md` step 1 (`vmware-openapi-generator` /
`vmsgen.py`). That workflow produces Swagger 2.0 JSON for
`config/api_specifications/`, which is separate from this Broadcom YAML workflow.

## Verification

After installing specs:

1. Confirm `config/api_specifications/<version>/` exists with the expected YAML files.
2. Verify files are non-empty and still valid YAML (optional parse check only).
3. Do **not** modify `config/MANIFEST.yml` unless the parent agent explicitly
   requests a manifest update.

## Report format

Return a concise summary:

```
## OpenAPI spec acquisition

- vSphere major: <N>
- VCF tag / source: <tag> (GitHub zipball | Broadcom portal | vmsgen fallback)
- Output directory: config/api_specifications/<version>/
- Files extracted: <list>
- Format: OpenAPI 3.0 YAML (unchanged from source)
```

## Constraints

- Write only under `config/api_specifications/<version>/` unless the parent agent
  requests otherwise.
- Never commit credentials or vCenter hostnames into spec files.
- Prefer the helper script over hand-editing large spec files.
- If acquisition fails, report the exact HTTP error or missing path; do not
  fabricate spec content.
