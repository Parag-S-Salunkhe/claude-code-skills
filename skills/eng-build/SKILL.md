---
name: eng-build
description: >-
  Build from an approved plan in thin tested slices: one slice at a time, test-first at agreed seams, verify, commit,
  and keep a progress ledger that survives compaction. Use when implementing a feature, fix or refactor in a code
  project, or when resuming half-finished work.
---

# Build

## Setup

- Read the plan and design doc; note their constraints. No plan and the work touches several files → eng-plan first.
- Work on a feature branch (or git worktree). Building on main needs the user's yes.
- Find the project's own commands (package.json scripts, Makefile, pyproject, README): test, build, typecheck, lint,
  dev server. Use those instead of guessing.
- Ledger: `docs/plans/<plan-name>.progress.md`, first line names the plan. After each slice add
  `Slice N: done — <commit sha> — <check result in one line>`. After compaction trust the ledger and `git log` over
  memory: a slice with a done line is done.

## Slice loop

1. Take the next slice whose blockers are done.
2. Seams: name the public interface the tests will go through. A new seam gets confirmed with the user, one line each:
   what it catches, what it misses.
3. Red: write one failing test at that seam for the next behaviour; run it; see it fail for the expected reason.
4. Green: the least code that passes. Simplest thing that works; three similar lines beat a premature abstraction.
5. Run the slice check plus the existing suite, build, typecheck and lint. Rerun a command only after code changed.
6. Commit one logical change; message says what and why.
7. Add the ledger line, then the next slice.

Tests worth keeping:

- Behaviour through the public interface. A test that breaks when internals change but behaviour does not is coupled
  to the implementation.
- Expected values come from the spec, never recomputed the way the code computes them (tautology).
- One test, then its code, per cycle. Writing all tests first tests imagined behaviour.
- No sensible seam (pure layout, config) → the check is a command or a browser test (eng-webtest), named in the plan.

## Scope

- Touch only what the slice needs. Improvements you notice go in a "Noticed" list in the ledger, not in the diff.
- Refactor and feature in separate commits. Each commit can be reverted alone; migrations ship with a rollback.
- A user-visible feature that is not finished stays behind a flag or unmerged.

## Rulings

- Small gap or conflict in the plan → decide, log `Ruling: <decision> — <why> — <cost if wrong>`, keep going.
- Stop and ask for: destructive or irreversible steps; security-sensitive changes (auth, secrets, permissions);
  anything that leaves the repo (push, deploy, publish, paid API calls); a plan so broken every path is a guess.
- Unexpected failure → stop the line: eng-debug until green before the next slice.

## Finish

- Full suite and build pass; each success criterion from the design checked with real output.
- Review the whole diff with eng-review before asking to push or merge.
- Report: slices done, checks run and their results, rulings, "Noticed" items, and anything not verified.

## Credits

Ideas only, no text copied. These links are for people reading this file; Claude doesn't need to open them.

- [obra/superpowers: executing-plans](https://github.com/obra/superpowers/tree/HEAD/skills/executing-plans) (MIT): a progress ledger that survives compaction, and when to stop and ask.
- [addyosmani/agent-skills: incremental-implementation](https://github.com/addyosmani/agent-skills/tree/HEAD/skills/incremental-implementation) (MIT): one thing per commit, scope discipline, easy rollback.
- [mattpocock/skills: tdd](https://github.com/mattpocock/skills/tree/HEAD/skills/engineering/tdd) (MIT): test-first at seams; what makes a test tautological or brittle.
