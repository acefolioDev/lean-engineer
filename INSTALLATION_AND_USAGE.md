# lean-engineer: Installation and Usage Guide

`lean-engineer` is a portable coding-agent skill/rule for Claude Code, Codex, and Cursor. It helps an agent reduce unnecessary token and tool usage while preserving correctness, security, maintainability, and appropriate verification.

## Prerequisites

- A local copy of this repository, or the repository contents extracted from GitHub.
- Claude Code, Codex, Cursor, or Antigravity.
- Cursor, if you want to use the Cursor project rule.
- Python 3.9 or newer only if you want to use the optional helper scripts.
- No third-party Python packages are required.

## Installation

### Single-command project installation

From the root of the project where you want the rule installed, run:

```bash
curl -fsSL https://raw.githubusercontent.com/acefolioDev/lean-engineer/main/scripts/install.sh | bash
```

The installer asks whether you use Codex, Claude Code, Cursor, Antigravity, or all four, then installs only the selected integration. To install every integration without prompting:

```bash
curl -fsSL https://raw.githubusercontent.com/acefolioDev/lean-engineer/main/scripts/install.sh | bash -s -- --all
```

To install into another directory:

```bash
curl -fsSL https://raw.githubusercontent.com/acefolioDev/lean-engineer/main/scripts/install.sh | bash -s -- --target /path/to/project
```

For user-level installation, the installer supports Claude Code, Codex, and Antigravity global rules:

```bash
curl -fsSL https://raw.githubusercontent.com/acefolioDev/lean-engineer/main/scripts/install.sh | bash -s -- --user
```

After installation, use this prompt in Claude Code, Codex, Cursor, or Antigravity:

```text
Use the lean-engineer skill/rule for this task.
```

### Project-level installation (recommended)

Run these commands from the root of the project where you want the skill available:

```bash
mkdir -p .claude/skills/lean-engineer .agents/skills/lean-engineer
cp /path/to/lean-engineer/skills/lean-engineer/SKILL.md \
  .claude/skills/lean-engineer/SKILL.md
cp /path/to/lean-engineer/skills/lean-engineer/SKILL.md \
  .agents/skills/lean-engineer/SKILL.md
```

Replace `/path/to/lean-engineer` with the directory containing this repository. For example:

```bash
cp ~/src/lean-engineer/skills/lean-engineer/SKILL.md \
  .agents/skills/lean-engineer/SKILL.md
```

Install the Claude Code copy, the Codex copy, or both according to the agents your project uses. Commit the project-level files when the whole team should share the same instructions.

Restart or reload the agent if the skill does not appear immediately.

### User-level installation

User-level installation makes the skill available across projects for one user:

```bash
mkdir -p ~/.claude/skills/lean-engineer ~/.agents/skills/lean-engineer
cp /path/to/lean-engineer/skills/lean-engineer/SKILL.md \
  ~/.claude/skills/lean-engineer/SKILL.md
cp /path/to/lean-engineer/skills/lean-engineer/SKILL.md \
  ~/.agents/skills/lean-engineer/SKILL.md
```

Use project-level installation when repository-specific, version-controlled behavior is preferred. Use user-level installation for a personal default across repositories.

### Cursor project-rule installation

Cursor project rules are version-controlled `.mdc` files under `.cursor/rules`. This repository includes a ready-to-use rule:

```bash
mkdir -p .cursor/rules
cp /path/to/lean-engineer/.cursor/rules/lean-engineer.mdc \
  .cursor/rules/lean-engineer.mdc
```

Open the project in Cursor and use the rule from Agent/Rules when needed. The included rule is configured as agent-requested (`alwaysApply: false`), so Cursor can select it for relevant coding tasks without adding it to every conversation. To apply it to every task, change `alwaysApply` to `true` in the target project's copy.

Cursor also supports a simple `AGENTS.md` alternative, but `.cursor/rules/lean-engineer.mdc` is the recommended project-rule format because it supports rule metadata and scoping.

### Antigravity project-rule installation

Antigravity discovers workspace rules from `.agents/rules/*.md`. This repository includes `.agents/rules/lean-engineer.md` with the required `trigger: model_decision` frontmatter. The installer copies it automatically when you choose Antigravity or All.

For a global Antigravity rule, the installer writes to `~/.gemini/config/rules/lean-engineer.md` when run with `--user`. Antigravity may also load workspace rules from `AGENTS.md` or `GEMINI.md`.

## Verify the installation

Confirm that the target file exists:

```bash
test -f .agents/skills/lean-engineer/SKILL.md && echo "Codex skill installed"
test -f .claude/skills/lean-engineer/SKILL.md && echo "Claude Code skill installed"
test -f .cursor/rules/lean-engineer.mdc && echo "Cursor rule installed"
test -f .agents/rules/lean-engineer.md && echo "Antigravity rule installed"
```

The two platform copies should be identical:

```bash
diff -u .claude/skills/lean-engineer/SKILL.md \
  .agents/skills/lean-engineer/SKILL.md
```

No output from `diff` means the files match.

For Cursor, check the MDC frontmatter and rule file separately:

```bash
sed -n '1,8p' .cursor/rules/lean-engineer.mdc
```

## Usage

Invoke the skill/rule by name in a coding task, for example:

```text
Use the lean-engineer skill to fix the failing validation test in this repository.
```

You can also ask the agent to apply it implicitly to a software-engineering task:

```text
Apply lean-engineer practices while adding this endpoint. Inspect the repository first, make the smallest coherent change, run focused tests, and summarize the verification.
```

The skill guides the agent to:

1. Classify the risk and scope of the task.
2. Inspect the working tree and the nearest repository instructions.
3. Retrieve only the code and configuration relevant to the task.
4. Make the smallest coherent change.
5. Run proportional tests or static checks.
6. Review the diff for regressions, secrets, and unrelated changes.
7. Report what changed and what was actually verified.

The skill does not replace project instructions, tests, security review, or human judgment. It also does not guarantee a fixed token reduction or identical behavior across models.

In Cursor, select or reference `lean-engineer` from the Agent rules context. The project rule applies to both Cursor Agent and Inline Edit when Cursor includes it in the active context.

In Antigravity, the `model_decision` rule is made available automatically when the task matches its description. You can also explicitly mention the rule in the agent conversation.

## Optional helper scripts

Run the repository inventory script to get a compact map without reading source contents:

```bash
python3 scripts/repo_map.py . --max-files 80
python3 scripts/repo_map.py . --max-files 80 --json
```

Summarize a saved test log without deleting or replacing the original log:

```bash
pytest -q 2>&1 | tee /tmp/test.log
python3 scripts/summarize_tests.py /tmp/test.log
```

Always inspect the original log when the summary is incomplete or ambiguous. The summarizer is a convenience tool, not proof that tests passed.

## Benchmarking

To evaluate whether the skill helps a workflow, read [`benchmark/README.md`](benchmark/README.md) first. Compare baseline and skill-enabled runs using the same tasks, model/version, reasoning settings, repository commit, and equivalent tool permissions. Alternate run order where possible, and use multiple tasks rather than a single example.

## Updating the skill

The canonical file is:

```text
skills/lean-engineer/SKILL.md
```

After editing it, copy it to both platform locations so they remain synchronized:

```bash
cp skills/lean-engineer/SKILL.md .claude/skills/lean-engineer/SKILL.md
cp skills/lean-engineer/SKILL.md .agents/skills/lean-engineer/SKILL.md
```

Update the Cursor and Antigravity rules separately when their metadata or concise wording needs to change:

```bash
cp .cursor/rules/lean-engineer.mdc /path/to/target-project/.cursor/rules/lean-engineer.mdc
cp .agents/rules/lean-engineer.md /path/to/target-project/.agents/rules/lean-engineer.md
```

Then verify the Claude Code and Codex copies with `diff` as shown above, and confirm that the Cursor copy retains valid `.mdc` frontmatter.

## Troubleshooting

### The skill is not detected

Check that the path is exactly `.claude/skills/lean-engineer/SKILL.md` for Claude Code or `.agents/skills/lean-engineer/SKILL.md` for Codex. Reload or restart the agent after copying the file.

For Cursor, check that the file ends in `.mdc`, is directly under `.cursor/rules`, and contains frontmatter with `description` and `alwaysApply`. Plain `.md` files in `.cursor/rules` are ignored by Cursor's project-rule system.

For Antigravity, check that the file is directly under `.agents/rules`, ends in `.md`, and contains valid frontmatter with `trigger` and `description`.

### The two copies have diverged

Treat `skills/lean-engineer/SKILL.md` as canonical, copy it to both platform paths, and run `diff` again.

### A helper script fails

Check that Python 3.9+ is being used and that the command is run from the repository root. For test summarization, confirm that the log path exists and retain the original log for diagnosis.
