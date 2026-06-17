This directory contains trimmed OpenAPI specs used by MockServer during integration tests.

Each JSON file defines API responses for a specific test scenario. Playbooks load
expectations via `PUT http://localhost:1080/mockserver/openapi` before exercising
modules.

Use the **same** `info.title` in every mock file for a target so MockServer
replaces prior expectations when switching scenarios. Paths match the vSphere
9.x REST API layout (`/api/vcenter/...`).

Run tests from the repository root:

```bash
make integration INTEGRATION_TARGETS=vcenter_vm_storage_policy
```
