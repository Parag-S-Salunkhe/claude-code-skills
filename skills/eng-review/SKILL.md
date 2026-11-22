---
name: eng-review
description: >-
  Review code changes before merge (your own, an agent's or a PR) with spec and standards kept as separate axes, plus
  correctness, security, tests and simplicity, each finding with severity and evidence; and handle review feedback
  you receive by verifying it before acting. Use for "review this", "check my diff/PR", "ready to merge?". A dedicated security review goes to eng-security.
---

# Review

## Giving a review

1. Pin the change: base and head commits (`git merge-base`). Before running anything, `git status --short` is empty on
   the reviewed ref; name that ref in the review.
2. Read the whole diff; when output is truncated, read each changed file. List the files.
3. Find the two sources: the spec (issue, plan, design doc) and the standards (CLAUDE.md / AGENTS.md, lint config,
   CONTRIBUTING, ADRs, patterns in nearby code).
4. Tests first: do they check behaviour through public interfaces? Probe one: invert a condition the change adds, run
   the suite, restore the file from a copy. Still green = a missing test, which is a finding.
5. Walk the code:
   - **Spec**: does it do everything asked, and nothing extra?
   - **Correctness**: empty, null and boundary values; error paths; races (check-then-act); off-by-one; time zones;
     state left half-written on failure.
   - **Security**: untrusted input validated at the boundary, output encoded, authorization on every protected action,
     no secrets in code or logs, new dependencies justified and pinned. Deeper review → eng-security.
   - **Simplicity**: could it be fewer lines; does each abstraction pass the deletion test; a conditional bolted onto
     an unrelated flow; feature logic leaking into a shared module; refactor mixed with feature.
   - **Performance**: N+1 queries, unbounded loops or fetches, missing pagination, heavy work in hot paths.
   - **Standards**: conventions, naming, file size (around 1000 lines is a split signal).
6. Check each finding against callers, guards and tests; drop what they rule out. Label bugs that already existed
   before this change separately from ones it adds.
7. Report under two headings, `## Spec` and `## Standards`, kept separate so one axis cannot hide the other. Each
   finding: `file:line` — severity (Critical / Required / Optional / Nit) — problem — evidence — fix, naming the
   restructuring rather than just "too complex". End with the files reviewed and what could not be verified.
   No significant findings → say so. Report only; the user decides what to change.

## Receiving a review

- Restate each point as a technical requirement. Unclear → ask before changing anything.
- Verify against the code and tests before agreeing. Correct → fix it and say what changed. Wrong for this codebase
  (breaks behaviour, unused feature, missing context, conflicts with a user decision) → push back with evidence.
  Architectural → take it to the user.
- Order: blockers, then quick fixes, then the rest; rerun tests after each.
- Your pushback turned out wrong → state the correction plainly and move on.

## Before merge

Keep the change small and focused (split into a stack or vertical slices if large). Description: imperative first line
that stands alone in history; body says what changed and why.

## Credits

Ideas only, no text copied. These links are for people reading this file; Claude doesn't need to open them.

- [addyosmani/agent-skills: code-review-and-quality](https://github.com/addyosmani/agent-skills/tree/HEAD/skills/code-review-and-quality) (MIT): review axes, tests first, severity labels.
- [mattpocock/skills: code-review](https://github.com/mattpocock/skills/tree/HEAD/skills/engineering/code-review) (MIT): spec and standards kept as separate questions.
- [getsentry/skills: find-bugs](https://github.com/getsentry/skills/tree/HEAD/skills/find-bugs) (Apache-2.0): read every changed line, list what wasn't verified, no invented findings.
- [obra/superpowers: receiving-code-review](https://github.com/obra/superpowers/tree/HEAD/skills/receiving-code-review) (MIT): verify feedback before agreeing; push back with evidence.
