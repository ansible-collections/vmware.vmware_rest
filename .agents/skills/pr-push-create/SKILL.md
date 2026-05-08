---
name: pr-push-create
description: Stage and commit changes, push to fork, and create or update a GitHub PR against the upstream repo using gh CLI or MCP. ONLY use when the user explicitly asks to create a PR, push a PR, or update a PR. NEVER activate as part of other tasks.
---

# PR Push & Create

Stage and commit changes, push to the user's fork (`origin`), and create or update
a pull request against the upstream (main) repo using `gh` CLI or MCP server.

**Trigger**: only when the user explicitly requests it (e.g. "create a PR",
"push and open PR", "update the PR"). Never auto-activate.

**Commit messages**: follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

## Workflow

### Step 1 -- Pre-checks

Run these checks **before doing anything else**. Stop immediately on failure.

```
1. git diff --staged --stat
   -> If empty: print "Nothing staged." Ask the user if they want to stage changes, or if you should stage all changes.

2. BRANCH=$(git branch --show-current)
   -> If BRANCH is main, master, or develop:
      print "ERROR: refusing to operate on protected branch '$BRANCH'. Create a feature branch first." and STOP.

3. Verify remotes:
   - origin  must exist (user's fork -- push target)
   - upstream must exist (main repo -- PR target)
   -> If either is missing: print which remote is missing and STOP.

4. UPSTREAM_REPO: extract owner/repo from `git remote get-url upstream`
   (strip .git suffix and host prefix, e.g. "https://github.com/org/repo.git" -> "org/repo")

5. If the skill 'pr-review' is defined, use it now. If any critical issues are detected or if required tests fail, STOP.
```

### Step 2 -- Check for existing PR

```bash
PR_NUMBER=$(gh pr list --repo "$UPSTREAM_REPO" --head "$(gh api user --jq .login):$BRANCH" --json number --jq '.[0].number' 2>/dev/null)
```

If `PR_NUMBER` is non-empty, an open PR already exists -- follow **Path B**.
Otherwise follow **Path A**.

### Conventional Commits -- shared (Path A and Path B)

Before committing, build a proposed message that satisfies [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

#### Infer the commit type

1. **Changelog fragments first**: if staged (or newly added) files exist under
   `changelogs/fragments/` (e.g. `*.yaml`), read them. Map fragment sections to
   types when obvious, for example:
   - `major_changes` / breaking language -> `feat!` or `fix!` with
     `BREAKING CHANGE:` body as required (see below)
   - `minor_changes`, new features -> `feat`
   - `bugfixes` -> `fix`
   - `trivial`, tooling-only with no user impact -> often `chore` or `ci`
   - docs-only fragments -> `docs`
   Prefer the fragment when it clearly indicates intent.

2. **Otherwise infer from the staged diff**: new behavior -> `feat`, defect
   correction -> `fix`, documentation -> `docs`, CI only -> `ci`, dependency or
   build metadata -> `chore`, code move without behavior change -> `refactor`,
   deprecation notices -> `deprecate` (or `feat` with deprecation described in
   body if your tooling prefers), removals of public API -> `remove` or
   breaking flow as appropriate.

3. **If the type is still ambiguous**, use **AskUserQuestion** (or the host's
   equivalent structured user prompt) to ask exactly:

   `What type of change is this for <component>? (feat/fix/docs/chore/refactor/ci/deprecate/remove/breaking)`

   Replace `<component>` with the main area (e.g. collection name, module name,
   or top-level path). After the user answers, use that type (map `breaking` to
   a breaking commit per the rules below).

#### Subject and body rules

- **Format**: `<type>[optional scope]: <description>` then optional body and
  footers per the spec. Use a scope only when it adds clarity (e.g.
  `fix(finding): ...`).
- **Subject line**: at most **72 characters** total (including type, scope, and
  description).
- **After `:` and space**: description must be **lowercase** (except proper
  nouns if unavoidable).
- **No trailing period** on the subject.
- **Imperative mood**: use "add", "fix", "remove", not "added", "fixes",
  "removing".
- **Breaking changes**:
  - Either use `!` after the type or scope (e.g. `feat!: ...`, `feat(api)!: ...`)
    **and/or** include a footer `BREAKING CHANGE: <explanation>`.
  - The body **must** include a blank line after the subject, then
    `BREAKING CHANGE: <explanation>` when you need to spell out the break
    (required when using `!` without enough detail on the subject line; align
    with the spec: the description should convey the break when using `!`
    alone).

Examples:

```
feat: add better prints in finding module
```

```
feat!: drop support for ansible-core <= 2.16

BREAKING CHANGE: ansible-core 2.16 and earlier are no longer supported.
```

#### Confirm before commit

Use **AskUserQuestion** to show the full proposed message (subject and body if
any). Ask exactly:

`Proposed commit \n<message>\n\n\nApprove, or provide an edited message?`

If the UI only supports fixed choices, offer **Approve** and an option such as
**I will paste an edited message in chat**; if they choose the latter, wait for
their next message and use **their text exactly** as the commit message (after
trimming only leading/trailing whitespace on the whole message, not rewriting
content).

**Do not run `git commit` until the user approves or supplies the final message.**

Then commit:

```bash
git commit -m "<subject>"   # if body empty; else use multiple -m or HEREDOC
```

For multi-line messages, prefer `git commit -F <file>` or multiple `-m`
arguments so the body and `BREAKING CHANGE:` footers are preserved.

### Path A -- New PR

1. **Analyze the diff**

   ```bash
   git diff --staged
   ```

   Read the output together with any relevant `changelogs/fragments/*` files to
   infer type and PR content.

2. **Commit** (follow **Conventional Commits -- shared** above).

3. **Push to fork**

   ```bash
   git push -u origin HEAD
   ```

4. **Draft PR structure** (do not create yet)

   Prepare:

   - **Title**: concise; should align with the approved commit subject or a
     short summary of the PR. Prefer staying within typical GitHub title length.

   - **Body** -- Use a template defined for this repo. If one does not exist, fill this template:

     ```
     #### SUMMARY
     - <describe changes: what was added/fixed/changed and why>

     #### ISSUE TYPE
     - <one of: New Module Pull Request | Bug Fix Pull Request | Feature Pull Request | Docs Pull Request | Refactoring Pull Request>

     #### COMPONENT NAME
     - <list each changed file path, one per line, prefixed with "- ">

     #### ADDITIONAL INFORMATION
     - <extra context: test coverage, migration notes, dependencies, etc.>
     ```

   Guidelines for filling the template:
   - SUMMARY: if it is a new module, explain what the module does and its key
     parameters. If it is a bug fix, explain the bug and the fix.
   - ISSUE TYPE: pick the most accurate single type.
   - COMPONENT NAME: list the primary changed files (modules, plugins, tests).
   - ADDITIONAL INFORMATION: mention tests added, backward compatibility, etc.

   Add a disclaimer that this PR body was generated using AI and reviewed by the author.

5. **Approve PR structure before create**

   Use **AskUserQuestion** to present the **proposed PR title** and the **full
   proposed body** (the filled template). Ask whether the user approves this
   structure or wants edits (title/body). **Do not run `gh pr create` until the
   user approves** (or provides an updated title/body to use verbatim).

6. **Create the PR**

   ```bash
   gh pr create \
     --repo "$UPSTREAM_REPO" \
     --title "<approved title>" \
     --body "<approved body from template above>"
   ```

   Use a HEREDOC or file for the body to preserve formatting.

7. **Report** the PR URL to the user.

### Path B -- Existing PR

1. **Analyze the diff**

   ```bash
   git diff --staged
   ```

   Use the same changelog + diff rules as Path A for commit typing.

2. **Commit** (follow **Conventional Commits -- shared** -- confirm message with
   AskUserQuestion, then commit).

3. **Force push to fork**

   ```bash
   git push --force-with-lease origin HEAD
   ```

4. **Report** success and print the existing PR URL:

   ```bash
   gh pr view "$PR_NUMBER" --repo "$UPSTREAM_REPO" --json url --jq '.url'
   ```

   If the user also asked to **update PR title/body**, draft the new title/body,
   get approval with **AskUserQuestion** as in Path A step 5, then:

   ```bash
   gh pr edit "$PR_NUMBER" --repo "$UPSTREAM_REPO" --title "..." --body "..."
   ```

## Hard Rules

- **NEVER push to main/master/develop.** If on a protected branch, refuse and stop.
- **NEVER `git push` to upstream.** All `git push` commands target `origin` (the fork). The upstream remote is read-only.
- **Always open PRs against upstream.** All `gh pr create` commands use `--repo` pointing to the upstream repo, so the PR is created on the main project (not on the fork).
- **NEVER run this skill unless the user explicitly asks.** Do not combine with other tasks.
- **Use --force-with-lease** (not --force) for force pushes.
- **No tool attribution in commits.** Do NOT add "Made-with", "Generated-by", or any tool/AI attribution trailers to commit messages. If the IDE injects such trailers automatically, the user should disable this in Cursor Settings > Agent > Attribution.
- **Conventional Commits** and **user approval** are mandatory: confirm the commit message before `git commit`, and confirm PR title/body structure before `gh pr create` (Path A).
