---
name: eng-design
description: >-
  System and software design: requirements and numbers first, simplest architecture that meets them, 2-3 options with
  explicit trade-offs, deep modules behind small interfaces, decisions recorded as short ADRs; also reviews an
  existing codebase that has become hard to change. Use for "design X", "how should we architect", "which database /
  hosting / framework", "review this design".
---

# Design

Mode: new system → 1-5. Choosing between options (database, hosting, framework) → 1, 5, then an ADR. Existing
codebase that is hard to change → "Review a codebase".

## 1. Requirements

- Functional: who uses it, main flows.
- Non-functional, with numbers: users and requests, data size, latency, availability, cost ceiling, privacy.
- Constraints: deadline, team size (often one person), existing stack, hosting, what is worth learning vs. reusing.
- Unknown number → write an assumption and mark it as one.

## 2. High-level design

- Components, data flow, where state lives, external services, trust boundaries — as a text or Mermaid diagram.
- Simplest design that meets the numbers: static beats server, one service beats five, managed beats self-hosted,
  unless learning is a stated goal.

## 3. Deep dive (only where it matters)

- Data model and its invariants; API contracts; caching; queues and events; failure handling (timeouts, retries with
  idempotency keys, what the user sees when it breaks).
- Interfaces: contract first; one error shape everywhere; validate at the boundary, trust inside; extend by adding
  (new optional field or endpoint) rather than changing. Every observable behaviour ends up depended on, so expose
  little.

## 4. Scale and operations

Load estimate against capacity; the first thing that breaks at 10×; single points of failure; backups plus a restore
test; monitoring that tells you before a user does; deploy and rollback; cost at expected and 10× load.

## 5. Trade-offs

2-3 options, each with what it costs (money, effort, complexity, lock-in), what it buys, and when you would pick it.
Recommend one, and name what you would revisit as it grows.

## Module design (code level)

- Deep module: a lot of behaviour behind a small interface. The interface is everything a caller must know: types,
  invariants, ordering, errors, config, performance.
- Deletion test: delete the module in your head. If complexity vanishes, it was a pass-through; if it reappears in
  every caller, it earns its place.
- Seams: one implementation is a hypothetical seam, two make it real. Add a seam only where something varies.
- Testable shape: take dependencies as parameters, return results instead of mutating, keep the surface small.

## ADR

`docs/decisions/NNNN-<title>.md`, or the project's existing convention: Status, Date, Context (forces and
constraints), Options (pros and cons each), Decision, Consequences (good and bad), Revisit when. One decision per
file; superseded records stay, marked as superseded.

## Review a codebase

- Scope by pain: the area the user names, otherwise hot spots from `git log --stat` (files that change most).
- Look for friction: one concept spread over many small files; shallow modules whose interface is as complex as the
  implementation; tight coupling across seams; code that is untested or hard to test.
- Present candidates: files, problem, proposed change, benefit (change lands in one place; callers get more per
  interface), before/after sketch, strength (strong / worth exploring / speculative). Ask which one to pursue before
  proposing interfaces. Respect existing ADRs unless the friction justifies reopening one.

## Output

Design doc or ADR with a diagram, explicit assumptions, trade-offs and open questions; saved in the repo.

## Credits

Ideas only, no text copied. These links are for people reading this file; Claude doesn't need to open them.

- [anthropics/knowledge-work-plugins: system-design](https://github.com/anthropics/knowledge-work-plugins/tree/HEAD/engineering/skills/system-design) (Apache-2.0): requirements, then high-level design, deep dive, scale, trade-offs.
- [anthropics/knowledge-work-plugins: architecture](https://github.com/anthropics/knowledge-work-plugins/tree/HEAD/engineering/skills/architecture) (Apache-2.0): short decision records.
- [mattpocock/skills: codebase-design](https://github.com/mattpocock/skills/tree/HEAD/skills/engineering/codebase-design) (MIT): deep modules, the deletion test, testable shape.
- [mattpocock/skills: improve-codebase-architecture](https://github.com/mattpocock/skills/tree/HEAD/skills/engineering/improve-codebase-architecture) (MIT): hot spots from git history, ask before proposing.
- [addyosmani/agent-skills: api-and-interface-design](https://github.com/addyosmani/agent-skills/tree/HEAD/skills/api-and-interface-design) (MIT): contract first, add rather than change, validate at boundaries.
