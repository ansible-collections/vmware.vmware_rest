---
name: release-pr
description: Creates a release PR for an Ansible collection following the upstream process (without release branches). Automatically determines the next version from changelog fragments. Use when asked to create a new release, a new collection version, or create a release PR.
---

# Skill: release-pr

## Purpose

Create a release PR for an Ansible collection. This skill is collection-generic — it derives namespace, name, and current version from `galaxy.yml`, and automatically determines the next version from changelog fragment categories.

This skill is the first phase of the release process. The second phase is captured in the `release-publish` skill.

References to `NAMESPACE` and `NAME` in this documnent should be replaced with the collection's actual namespace and name values. The `AGENTS.md` describes how those values can be found.

## When to Invoke

TRIGGER when:
- A user asks to create a new release, a new collection version, or create a release PR.
- A user asks about the release process or release checklist.

DO NOT TRIGGER when:
- Reviewing a PR (use `pr-review` skill instead)
- Running tests (use `run-tests` skill instead)
- General changelog or versioning questions unrelated to performing a release

## Inputs

- `version` (optional): the target release version, e.g. `2.1.0`. If not provided, the version is automatically determined from changelog fragments (see Step 1).

## Prerequisites

- Use this skill **before doing anything else**: python-virtual-env
- `antsibull-changelog` installed (`pip install antsibull-changelog`)
- `gh` CLI installed and authenticated, or a Github MCP server setup
- An origin and an upstream remote. The origin remote should be a fork of the upstream owned by the user


## Release PR Steps

### Step 1 — Read collection context and determine version

Extract collection identity from `galaxy.yml`:

```bash
grep -E '^(namespace|name|version):' galaxy.yml
```

Use the extracted values as `NAMESPACE`, `NAME`, and `CURRENT_VERSION` in all subsequent steps.

#### Determine next version

If the user did not provide a target version, determine it automatically:

1. Scan all YAML files in `changelogs/fragments/` and collect the top-level keys (category names) from each file.
2. Determine the version bump using the highest-severity category found:

| Bump  | Fragment categories                                      |
|-------|----------------------------------------------------------|
| Major | `breaking_changes`, `removed_features`, `major_changes`  |
| Minor | `minor_changes`, `deprecated_features`                   |
| Patch | `bugfixes`, `security_fixes`, `known_issues`, `trivial`  |

3. Apply the bump to `CURRENT_VERSION` (e.g. `2.0.0` + minor → `2.1.0`). When bumping major, reset minor and patch to 0. When bumping minor, reset patch to 0.

Use the resulting version as `VERSION`.

**CONFIRM:** Present the extracted `NAMESPACE`, `NAME`, `CURRENT_VERSION`, the detected fragment categories, the determined bump type, and the resulting `VERSION` to the human. Ask them to confirm these values are correct before proceeding. The human may override the version at this point.

### Step 2 — Pre-flight checks

```bash
git status
git checkout main
git pull --rebase upstream main
```

Verify before continuing:
- Working tree is clean (no uncommitted changes)
- Changelog fragments exist: `ls changelogs/fragments/`

### Step 3 — Create release branch

```bash
git checkout -b release/VERSION
```

### Step 4 — Update galaxy.yml version

If `CURRENT_VERSION` in `galaxy.yml` does not match `VERSION`, update it:

```bash
sed -i "s/^version: .*/version: VERSION/" galaxy.yml
```


### Step 5 — Generate changelog

Determine the release type from `VERSION` and suggest a release summary using this template:

- **Major** (`X.0.0`): `This is a major release of the ``NAMESPACE.NAME`` collection.`
- **Minor** (`X.Y.0`): `This is a minor release of the ``NAMESPACE.NAME`` collection.`
- **Patch** (`X.Y.Z`): `This is a patch release of the ``NAMESPACE.NAME`` collection.`

Followed by:
`This changelog contains all changes to the modules and plugins in this collection that have been made after the previous release.`

**CONFIRM:** Present the suggested release summary and the list of changelog fragments that will be included. Ask the human to approve or edit the text before writing the fragment.

Create the release summary fragment:

```bash
cat > changelogs/fragments/VERSION.yml << 'EOF'
release_summary: |-
  This is a <major/minor/patch> release of the ``NAMESPACE.NAME`` collection.
  This changelog contains all changes to the modules and plugins in this collection
  that have been made after the previous release.
EOF
```

Generate the changelog:

```bash
antsibull-changelog release --reload-plugins
```

**CONFIRM:** Show the human the generated `CHANGELOG.rst` diff and ask them to confirm the content is correct before continuing.

### Step 6 — Commit and push release branch

```bash
git add -A
git commit -m "Release VERSION"
git push origin release/VERSION
```

### Step 7 — Create pull request

```bash
gh pr create --title "Release VERSION" --body "Release VERSION of NAMESPACE.NAME."
```

### Step 8 - Conclude this phase

At this point, the human must have someone review their PR and merge it. Once that is done, they can ask to continue the release via the `release-publish` skill.
