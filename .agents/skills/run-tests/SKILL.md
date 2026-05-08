---
name: run-tests
description: Runs and writes tests (lint, sanity, unit, integration) for this Ansible collection using linters and ansible-test. Use when asked to run, check, or write tests for a module or utility. Do not use for PR reviews or questions unrelated to testing.
---

# Skill: run-tests

## Purpose

Run and write tests for this Ansible collection. Covers lint, sanity, unit, and integration tests using `ansible-test` and linters.

References to `NAMESPACE` and `NAME` in this documnent should be replaced with the collection's actual namespace and name values. The `AGENTS.md` describes how those values can be found.

## When to Invoke

TRIGGER when:
- A user asks to run tests, check tests, or verify changes with tests
- A user asks how to test a module or utility
- A user asks to write tests for new or modified code

DO NOT TRIGGER when:
- Reviewing a PR for overall quality (use `.agents/skills/pr-review/SKILL.md` instead)
- The question is about module logic unrelated to testing

## Test Infrastructure

A version of python must be installed. If no virtual environment exists, one will be created.
The `make` command must be available.
The environment should have Docker or Podman installed for tests.


If using the Makefile and `make`, commands should be run out of the project directory.
If using `ansible-test` commands directly, the collection must be installed at `ansible_collections/NAMESPACE/NAME/` (relative to a directory on `ANSIBLE_COLLECTIONS_PATHS`) for imports to resolve correctly and all commands should be run from that directory. The Setup section specifys how to install the collection.

---

## Setup python virtual environment

Use this skill **before doing anything else**: python-virtual-env

## Test Commands

### Install the collection

This is only required when not using the Makefile targets for the other tests.

```bash
make install-integration-reqs
```

### Sanity and Linters

Use this to check style, documentation, and imports for a changed file.

There is a Makefile target, `sanity` and `linters`, and an optional input to specify the file names that should be tested by sanity, `SANITY_TARGETS`

```bash
# With Makefile
make linters
make sanity SANITY_TARGETS=plugins/modules/appliance_access_consolecli_info.py

# Without the Makefile
black --check --diff --color .
ansible-test sanity plugins/modules/appliance_access_consolecli_info.py -v --color --coverage --junit --docker default
```

### Unit

Run unit tests for changed files.

```bash
# With Makefile
make units UNIT_TARGETS=tests/unit/plugins/module_utils/test_mysql.py

# Without the Makefile
ansible-test units tests/unit/plugins/module_utils/test_mysql.py --docker -vvv
```

Unit tests live under `tests/unit/plugins/` and use the **PyTest** framework.

### Integration

Run integration tests against a remote vCenter instance. The user must have the following environment variables set for these tests to work:
- VMWARE_HOSTNAME or VCENTER_HOSTNAME
- VMWARE_USER or VCENTER_USERNAME
- VMWARE_PASSWORD or VCENTER_PASSWORD

If these environment variables are not set, ask the user how they would like to set them. If the user does not want to set them, or cannot set them, you cannot run the integration tests.

Test targets can be found in `tests/integration/targets/<target_name>`. Target names are usually be mapped one to one to the modules they test, but may also test multiple related modules. For example, the vmware_rest_appliance target may cover any appliance_* modules.
If no test targets cover the files the user has changed, ask them if they want to specify the tests to run. Otherwise, do not run integration tests.

```bash
# With Makefile
make eco-vcenter-ci INTEGRATION_TARGETS=vmware_rest_appliance

# Without the Makefile
## Run this in the same directory ansible-test will be run
./tests/integration/generate_integration_config.sh
ansible-test integration vmware_rest_appliance --docker default -vvv
```

---

## When Tests Are Required

| Change type | Sanity | Unit | Integration |
|---|---|---|---|
| New module | yes | yes | yes |
| New parameter | yes | if logic changed | yes |
| Bug fix | yes | yes | yes |
| Refactoring | yes | yes | no |
| Documentation only | yes | no | no |
