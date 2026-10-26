# Reproducible benchmark

## Goal

Test whether `lean-engineer` lowers total input/output tokens and cost per successful task without materially reducing task quality. Treat the skill's target (for example, 30% lower tokens) as a hypothesis, not a promise.

## Experimental design

1. Choose 8–20 representative, independently testable tasks from a repository you are allowed to use. Include bug fixes, small features, refactoring, test additions, and one higher-risk task. Avoid tasks that require external credentials or irreversible actions.
2. Freeze the repository at a known commit. Create a clean worktree or reset to that commit before each run.
3. Use the same agent/model version, reasoning effort, permissions, tool access, environment, and task prompt for both conditions. The only intended difference is whether the skill is installed/invoked.
4. Randomize or alternate run order (baseline/skill, then skill/baseline) to reduce order effects. Do not let one run see the other run's patch or notes.
5. Use separate clean sessions. Do not reuse chat context between tasks.
6. Record provider-reported usage for every run: input tokens, cached input tokens if available, output tokens, tool-call counts if available, cost, duration, completion status, and test results. Use provider data rather than estimating from character counts.
7. Score correctness with task-specific acceptance criteria and automated tests. Have a reviewer who does not know the condition review diffs if feasible.
8. Compare paired results per task, not only aggregate totals. Report median and range; call out failures and outliers.

## Fairness notes

- If the platform automatically loads the skill description, record that overhead. Count it in total usage.
- Keep model settings identical. A model update during the experiment invalidates a strict comparison; rerun both conditions.
- Do not cherry-pick successful runs. Record every attempt and any retries.
- If a task fails, record all tokens/cost consumed up to failure. A low-token failure is not a win.
- Distinguish cached input tokens from total input tokens. Cached tokens may have different prices, but they are still part of context processing.
- Never claim "same quality" based only on a smaller token count. Track acceptance and regression rates.

## Run log

Copy `results-template.csv` to `results.csv` and add one row per task/condition. Suggested fields include task ID, condition, commit, model, input/output tokens, cached tokens, cost, duration, completion, acceptance, tests, and reviewer score.

## Suggested acceptance criteria

Agree on these before testing:
- No material decrease in acceptance rate (e.g. no more than 5 percentage points on a sufficiently large task set).
- No critical security or data-integrity regressions.
- A meaningful reduction in median total tokens and cost per successful task.
- If token savings come with more retries, regressions, or review burden, count that against the skill.

For a small benchmark, confidence is limited. Repeat the benchmark on a second repository or a later task batch before generalizing.
