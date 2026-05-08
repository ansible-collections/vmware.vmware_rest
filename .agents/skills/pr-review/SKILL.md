---
name: pr-review
description: Reviews pull requests and code changes in this Ansible collection against project standards and the Ansible Collection Review Checklist. Use when asked to review a PR, patch, diff, or set of code changes. Do not use for GitHub Issues or general Q&A.
---

# Skill: pr-reviewer

## Purpose

Review pull requests and code changes in this Ansible collection.

References to `NAMESPACE` and `NAME` in this documnent should be replaced with the collection's actual namespace and name values. The `AGENTS.md` describes how those values can be found.

## When to Invoke

TRIGGER when:
- A user asks to review a PR, patch, diff, or set of code changes
- A user asks to review the changes on their current branch
- Validating changes against project standards before merge

DO NOT TRIGGER when:
- Reviewing GitHub Issues (not PRs/code changes)
- General Q&A, documentation lookup, or debugging unrelated to a changeset

## Inputs

- `target` (optional): PR number, branch name, commit hash, or file path.
  - If omitted, review the current working changes via `git diff HEAD`.

## Approach

### Step 1 — Gather the changeset

Obtain the diff using the appropriate method:
- PR number provided → read changed files and their diffs
- Branch or commit reference → run `git diff <base>..<ref>` or `git show <ref>`
- File path provided → read the file and review it in full
- No target → run `git diff HEAD` to capture all current changes

Read every changed file completely before forming any judgment.

### Step 2 — Run all review checks in parallel

Execute all checks in the checklist below concurrently. Collect findings per category. For categories not listed below, apply the rules from the corresponding sections in `AGENTS.md`.

### Step 3 — Report

Produce the structured report described in the **Output Format** section.

---

## Review Checklist

Architecture, check_mode, and Type Conversion categories are fully covered by `AGENTS.md` — apply those sections directly.

### Collection Metadata

- `galaxy.yml`: `version`, `description`, `tags`, `dependencies` are accurate and up to date.
- `meta/runtime.yml`: `requires_ansible` minimum version reflects any new Ansible features used.
- New Python dependencies added to both `requirements.txt` and `meta/ee-requirements.txt` if it exists.

### Module Documentation

- Every public parameter has a `description`, `type`, and `required` or `default`.
- The `EXAMPLES` block is present, valid YAML, and covers the primary use cases.
- The `RETURN` block accurately describes every key returned by the module.
- Module short description (`short_description`) is concise and accurate.
- `author` field is present and correctly formatted.

### Naming and Style

- No abbreviations that reduce readability.

### Idempotency

- `result['changed']` is `False` when no real change is made.
- Repeated runs with the same arguments produce the same outcome with no spurious changes.

### Sensitive Data

- All sensitive parameters (passwords, tokens, secrets) set `no_log=True`.
- No sensitive data appears in `executed_statements` or module return values in plaintext.

### Error Handling

- All errors call `module.fail_json(msg=...)` with a descriptive, actionable message — no bare `raise` or `sys.exit()`.

### Testing

- The run-tests skill can be used, if one is defined. Sanity and linters should always be run and must pass.
- New integration tests cover both the happy path and idempotency (running the same task twice).
- New integration tests cover the `state: absent` path where applicable.

### Backwards Compatibility

- No existing parameters are removed or renamed without a deprecation notice.
- No existing return values are removed or their types changed.
- Breaking changes are flagged explicitly and justified.
- Deprecations use the Ansible deprecation mechanism (`module.deprecate()`).

### Changelog Fragment

- Fragment content is concise, written in past tense, and references the module name.

### Code Quality

- No dead code, commented-out blocks, or debug statements left in.
- No feature flags or backwards-compatibility shims for hypothetical future use.
- No premature abstractions (helpers/utilities created for a single use case).
- No security vulnerabilities: no shell injection, no unvalidated external input passed to queries, no hardcoded credentials.

---

## Output Format

Structure the review as follows:

```
## PR Review: <target or "Current Changes">

### Summary
<One-paragraph overall assessment: scope of the change, general quality, primary concerns.>

### Findings

#### Blockers (must fix before merge)
- [CATEGORY] <File>:<line> — <description of the issue>

#### Warnings (should fix, not strictly blocking)
- [CATEGORY] <File>:<line> — <description of the issue>

#### Suggestions (optional improvements)
- [CATEGORY] <File>:<line> — <description of the issue>

### Checklist Status
| Category | Status | Notes |
|---|---|---|
| Collection Metadata | PASS / FAIL / N/A | ... |
| Module Documentation | PASS / FAIL / N/A | ... |
| Naming and Style | PASS / FAIL / N/A | ... |
| Architecture | PASS / FAIL / N/A | ... |
| Idempotency | PASS / FAIL / N/A | ... |
| check_mode | PASS / FAIL / N/A | ... |
| Sensitive Data | PASS / FAIL / N/A | ... |
| Error Handling | PASS / FAIL / N/A | ... |
| Type Conversion | PASS / FAIL / N/A | ... |
| Testing | PASS / FAIL / N/A | ... |
| Backwards Compatibility | PASS / FAIL / N/A | ... |
| Changelog Fragment | PASS / FAIL / N/A | ... |
| Code Quality | PASS / FAIL / N/A | ... |

### Verdict
APPROVE / REQUEST CHANGES / COMMENT

<One sentence justifying the verdict.>
```

Use `N/A` for categories that do not apply to the changeset (e.g., type conversion for a docs-only PR). Be specific: always reference the file and line number when citing a finding.
