# lean-engineer: Installation and Usage Guide

`lean-engineer` is a portable coding-agent skill for Claude Code and Codex. It helps an agent reduce unnecessary token and tool usage while preserving correctness, security, maintainability, and appropriate verification.

## Prerequisites

- A local copy of this repository, or the repository contents extracted from GitHub.
- Claude Code or Codex.
- Python 3.9 or newer only if you want to use the optional helper scripts.
- No third-party Python packages are required.

## Installation

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

## Verify the installation

Confirm that the target file exists:

```bash
test -f .agents/skills/lean-engineer/SKILL.md && echo "Codex skill installed"
test -f .claude/skills/lean-engineer/SKILL.md && echo "Claude Code skill installed"
```

The two platform copies should be identical:

```bash
diff -u .claude/skills/lean-engineer/SKILL.md \
  .agents/skills/lean-engineer/SKILL.md
```

No output from `diff` means the files match.

## Usage

Invoke the skill by name in a coding task, for example:

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

Then verify with `diff` as shown above.

## Troubleshooting

### The skill is not detected

Check that the path is exactly `.claude/skills/lean-engineer/SKILL.md` for Claude Code or `.agents/skills/lean-engineer/SKILL.md` for Codex. Reload or restart the agent after copying the file.

### The two copies have diverged

Treat `skills/lean-engineer/SKILL.md` as canonical, copy it to both platform paths, and run `diff` again.

### A helper script fails

Check that Python 3.9+ is being used and that the command is run from the repository root. For test summarization, confirm that the log path exists and retain the original log for diagnosis.
