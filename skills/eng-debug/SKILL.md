---
name: eng-debug
description: >-
  Debug code: build a tight feedback loop that goes red on the bug, reproduce and shrink it, rank 3-5 falsifiable
  hypotheses, probe one variable at a time, fix with a regression test. Use for a bug, failing or flaky test, error,
  crash or slowdown in a code project. Incidents outside the code (hosts, devices, pipelines) and written RCAs go to rca.
---

# Debug

No theory before a loop that goes red.

## 0. Redact

Show commands and output with secrets replaced by `<REDACTED>`; pass credentials through env vars.

## 1. Feedback loop (most of the effort)

Build one command that runs the real code path and asserts the user's exact symptom. Options, roughly in order:

1. Failing test at the closest seam (unit, integration, end-to-end).
2. `curl` script against the running dev server.
3. CLI run with a fixture input, diffed against known-good output.
4. Headless browser script (Playwright) asserting on DOM, console or network.
5. Replay of a captured request, payload or log through the code path.
6. Minimal harness: one service, dependencies stubbed, one call.
7. Property or fuzz loop for "sometimes wrong" output.
8. `git bisect run` between a known-good and known-bad commit.
9. Differential run: old vs new version, or two configs, diffing output.
10. Last resort: a script that walks the human through the clicks and captures what they see.

Tighten it: faster (skip unrelated setup), sharper (assert the symptom, not "did not crash"), deterministic (pin time,
seed randomness, stub network). Flaky bug → raise the failure rate (loop it 100×, run in parallel, add load) until it
fails often enough to work with.

Done when there is one command, already run and shown (redacted), that is red on this bug, gives the same verdict
every run, takes seconds, and runs unattended. If a loop is impossible, say so, list what you tried, and ask for
access, a captured artifact (log, HAR, recording with times) or permission to add temporary logging.

## 2. Reproduce and shrink

- Confirm it fails with the user's symptom, not a neighbouring failure.
- Cut inputs, config and steps one at a time, rerunning after each cut; keep only what keeps it red.

## 3. Hypotheses

- Write 3-5, ranked, each with a prediction: "If X is the cause, changing Y makes it disappear / changing Z makes it
  worse." A hypothesis without a prediction gets sharpened or dropped.
- Share the ranked hypotheses before probing: the user may already know one is ruled out.

## 4. Probe

- One variable per probe, each tied to a prediction. Debugger or REPL first, then targeted logs at the boundary that
  separates two hypotheses.
- Tag temporary logs `[DBG-<4 chars>]` so cleanup is one grep.
- Slowness: take a baseline measurement (timer, profiler, query plan) first, then bisect; fix second.
- Three fixes failed → stop, question the assumptions or the design, tell the user.

## 5. Fix

- Turn the shrunk repro into a regression test at a seam that exercises the real pattern. Watch it fail, apply the
  fix, watch it pass, rerun the original loop.
- No such seam → that is a finding (the design blocks testing); report it.
- Fix the cause, then grep for the same pattern elsewhere.

## 6. Clean up

- [ ] Original loop is green
- [ ] Regression test passes, or the missing seam is reported
- [ ] `grep -r "DBG-"` finds nothing
- [ ] Throwaway scripts removed
- [ ] Commit or PR message names the confirmed cause

## Credits

Ideas only, no text copied. These links are for people reading this file; Claude doesn't need to open them.

- [mattpocock/skills: diagnosing-bugs](https://github.com/mattpocock/skills/tree/HEAD/skills/engineering/diagnosing-bugs) (MIT): a feedback loop that goes red first, ranked falsifiable hypotheses, tagged debug logs.
- [obra/superpowers: systematic-debugging](https://github.com/obra/superpowers/tree/HEAD/skills/systematic-debugging) (MIT): stop after three failed fixes and question the approach.
- [addyosmani/agent-skills: debugging-and-error-recovery](https://github.com/addyosmani/agent-skills/tree/HEAD/skills/debugging-and-error-recovery) (MIT): stop the line when something breaks.
