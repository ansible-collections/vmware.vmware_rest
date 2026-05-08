---
name: release-publish
description: Guides the user through thr publication of a an Ansible collection to Automation Hub and Ansible Galaxy.
---

# Skill: release-publish

## Purpose

Build the collection from a specific release version, and step through how it can be published to Automation Hub and Galaxy.

References to `NAMESPACE` and `NAME` in this documnent should be replaced with the collection's actual namespace and name values. The `AGENTS.md` describes how those values can be found.

## When to Invoke

TRIGGER when:
- A user asks to publish a new release, a collection version, or publish to Galaxy or Hub.
- A user asks about the release process or release checklist

DO NOT TRIGGER when:
- Reviewing a PR (use `pr-review` skill instead)
- Running tests (use `run-tests` skill instead)
- General changelog or versioning questions unrelated to performing a release

## Inputs

- `version` (optional): the target release version, e.g. `2.1.0`. If not provided, the version is automatically determined from changelog fragments (see Step 1).

## Prerequisites

- `ansible-core` installed (`pip install ansible-core`)

## Release Publish Steps


### Step 1 — Read collection context and determine version

Extract collection identity from `galaxy.yml`:

```bash
grep -E '^(namespace|name|version):' galaxy.yml
```

Use the extracted values as `NAMESPACE`, `NAME`, and `VERSION` (if the user did not provide a target version) in all subsequent steps.

### Step 2 — Pre-flight checks

```bash
git checkout main
git pull --rebase upstream main
git fetch --tags
git status
```

Verify before continuing:
- Working tree is clean (no uncommitted changes)
- Changelog fragments exist: `ls changelogs/fragments/`
- The file tests/integration/integration_config.yml does not exist
- A tag matching `VERSION` does not already exist

### Step 3 — Tag and push

**CONFIRM:** Ask the human to confirm before creating and pushing the tag. This action is irreversible.

```bash
git tag -a VERSION -m "NAMESPACE.NAME: VERSION"
git push upstream VERSION
```

### Step 4 — Create GitHub release

```bash
gh release create VERSION --title "VERSION" --notes "See [CHANGELOG.rst](https://github.com/NAMESPACE/NAME/blob/main/CHANGELOG.rst) for details."
```

### Step 5 — Build the collection

```bash
ansible-galaxy collection build .
```

### Step 6 — Check the contents of the built tar

Ensure the tar file does not contain sensitive files, such as tests/integration/integration_config.yml, or bloat, such as .venv/

```bash
tar -tf NAMESPACE-NAME-VERSION.tar.gz
```

### Step 7 - Conclude this phase

At this point, the a new Github release has been created and a corresponding tag exists on the repository. The user has a tar of the built collection that they can upload to Galaxy or Hub.

Community content should only go to Galaxy.
Certified content should go to both Galaxy and Hub.
Validated content should only go to Hub.
