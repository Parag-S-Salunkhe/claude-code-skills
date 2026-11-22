---
name: eng-plan
description: >-
  Plan software work before building it: find out what the user wants and why, compare 2-3 approaches, get a short
  design approved, then write a plan of thin vertical slices with blocking order and a check command per slice. Use
  for a new feature, page, tool, project or refactor that spans several steps or sessions; skip for one-line fixes. Architecture and technology choices go to eng-design.
---

# Plan

Nothing gets built until the user approves a design. The plan then holds only the decisions a builder could not make
alone.

## 1. Look before you ask

- Read what exists: the repo, files or docs the user pointed at, earlier decisions (`docs/decisions/`, `docs/plans/`,
  README). Never ask what the project already answers or reopen what the user already decided.
- Everything needed is in the request and the change is small → do it, say what you did; this skill ends here.
- Something that changes what gets built is still open → step 2.

## 2. Find the intent

- First ask why they want it and what success looks like: one open question in their words, no menu of answers.
- After that, ask only questions whose answer changes what gets built, one at a time, saying what the answer would
  change. Everything else is your call: state it as a proposal with its reason so they can correct it.
- Territory to cover, never read out as a script: who it is for; goals, non-goals and anti-goals (works, but still a
  failure); constraints (time, money, stack, hosting); what exists today; examples they like or dislike.
- Play back each part you understand in a short paragraph. Mark what you filled in as your proposal. End with
  "what's wrong or missing?"
- "Just do it" → state each main how-choice (platform, language, hosting) in one line, then build.

## 3. Approaches

- In a message of its own: 2-3 real ways to build it, grounded in the current code, each with its cost, effort, risk
  and lock-in. Recommend one and say why. If only one way makes sense, say why the others do not fit.
- Something visual → sketch it in text. A quick throwaway spike is fine with a yes; it stays labelled throwaway, and
  keeping it is a new request.

## 4. Design doc

- Size it: small change = 5-10 lines; project = full doc.
- Contents: intent and why; goals, non-goals, anti-goals; constraints; approaches considered, the chosen one and why;
  decisions (mark the user's and your calls separately); success criteria that can be checked; out of scope; open
  questions.
- Location: `docs/plans/YYYY-MM-DD-<topic>-design.md`, unless the project has its own convention or the user names one.
- Builder check: reread it as a builder who never saw the conversation. Questions only the user can answer go back in
  one message, most important first; settle the rest yourself and mark them as your calls.
- Gate: explicit approval of the doc before any code, scaffolding or install. Reading and exploring are fine.

## 5. Plan (after approval)

- File map first: files created or changed, one responsibility each, following existing patterns.
- Slices are tracer bullets: a thin end-to-end path (data → logic → UI → test) that can be shown working on its own.
  Riskiest or least certain slice first. Prefactor first: make the change easy, then make the easy change.
- Each slice: what it delivers (as the user sees it), blocked by, files, acceptance check (the command and the output
  that means pass).
- Steps decide things: exact names and signatures, the test's name and expected values, the verify command. A step
  that decides nothing ("handle edge cases", "add validation", "TBD") is a gap; a full function body that the
  signature and test already determine is a transcript. Both get fixed.
- Self-review: every requirement maps to a slice; names match across slices; every failure mode in the design has a
  test; the plan is shorter than the code it describes.
- Work bigger than one session: keep a map at the top of the plan with Destination, Decisions so far (one line each),
  Fog (known unknowns, not ticketed yet), Out of scope. Resolve one open decision at a time; fog becomes slices as it
  clears.
- Save as `docs/plans/YYYY-MM-DD-<topic>-plan.md`, link it, ask the user to review it, then build with eng-build.

Done when: the design doc is approved, the plan is saved, and every slice has a check command.

## Credits

Ideas only, no text copied. These links are for people reading this file; Claude doesn't need to open them.

- [obra/superpowers: brainstorming](https://github.com/obra/superpowers/tree/HEAD/skills/brainstorming) (MIT): intent first, 2-3 approaches, approval before any code.
- [obra/superpowers: writing-plans](https://github.com/obra/superpowers/tree/HEAD/skills/writing-plans) (MIT): a plan holds decisions, not code; self-review before handing over.
- [mattpocock/skills: to-tickets](https://github.com/mattpocock/skills/tree/HEAD/skills/engineering/to-tickets) (MIT): thin vertical slices with blocking order, refactor first.
- [mattpocock/skills: wayfinder](https://github.com/mattpocock/skills/tree/HEAD/skills/engineering/wayfinder) (MIT): a map for multi-session work: decided, still foggy, out of scope.
- [addyosmani/agent-skills: spec-driven-development](https://github.com/addyosmani/agent-skills/tree/HEAD/skills/spec-driven-development) (MIT): success criteria and an explicit out-of-scope list.
