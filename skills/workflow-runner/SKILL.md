---
name: workflow-runner
description: >-
  Raise, rerun and check GitHub Actions workflows with the gh CLI, and always hand back the full run link. Use when the
  user says "run the workflow", "trigger", "dispatch", "rerun", "rerun failed jobs", "is the run done", "why did the
  run fail", "approve", or asks for a run link or a workflow's status.
---

# workflow-runner: every run, verified inputs, a link every time

## Rules

1. **The full run link, every time.** Whenever a run is raised or rerun, put
   `https://github.com/<owner>/<repo>/actions/runs/<id>` in the reply, on its own line, ready to copy. Every later
   reply about that run (waiting, approved, done, failed) repeats the full link, never just the number. People forward
   these links to approvers.
2. **Inputs are exactly what the user asked for.** Many workflows ship with example default inputs (a sample ID, a
   test host). An input you leave out falls back to that default. Pass every input explicitly, and after the run
   starts, check the run's own "print inputs" step or the job log before anyone approves it.
3. **The right account.** If `gh` has several accounts, check `gh auth status` first; switch with
   `gh auth switch --user <name>` when the repo needs the other one, and switch back if the user asked you to.
4. **Read-only checks are free; changes need a yes.** Viewing runs and logs: go ahead. Dispatching, rerunning,
   cancelling or approving: only what the user asked for.
5. **Green isn't done.** A successful run means the job finished. Check the real outcome too (the record in the
   database, the deployed version, the host state) before calling it done.

## Commands

```bash
# raise
gh workflow run <workflow.yml> -R <owner>/<repo> --ref main -f input1=value -f input2=value
sleep 3; gh run list -R <owner>/<repo> --workflow <workflow.yml> --limit 1 --json databaseId,url,status,createdAt

# watch / inspect
gh run watch <id> -R <owner>/<repo> --exit-status
gh run view <id> -R <owner>/<repo> --log-failed        # only the failing steps
gh run view <id> -R <owner>/<repo> --json jobs -q '.jobs[] | "\(.name): \(.conclusion)"'

# rerun
gh run rerun <id> -R <owner>/<repo> --failed           # only the failed jobs
gh run rerun <id> -R <owner>/<repo>                    # everything

# waiting for approval (environments)
gh api repos/<owner>/<repo>/actions/runs/<id>/pending_deployments
```

## Why did it fail?

1. `--log-failed` first: the exact error line, not a summary.
2. Did the inputs match the request? (Rule 2.)
3. Compare with the last green run of the same workflow: inputs, ref, runner, timing.
4. A flaky step (network, a runner image) → one rerun of the failed jobs. Fails the same way twice → it's not flaky;
   use the `rca` skill.

## Report format

```
Raised: <workflow> on <repo> (<key inputs>)
https://github.com/<owner>/<repo>/actions/runs/<id>
Status: queued / waiting for approval / in progress / success / failed at <step>
```

## Credits

My own daily rules, no outside source.
