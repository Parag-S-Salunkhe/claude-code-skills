---
name: eng-context
description: >-
  Write and trim what agents read: skills, CLAUDE.md / AGENTS.md, memory files, handoff notes and prompts, with
  descriptions that trigger correctly, progressive disclosure, a small always-loaded footprint and no stale or
  duplicated facts. Use when creating or editing a skill or CLAUDE.md, when a session feels bloated or the agent
  confuses facts, or to cut per-session tokens. Saving a learning to your notes goes to save-learnings, notes health checks to notes-lint.
---

# Agent context

Always-loaded text costs tokens and attention on every turn; the human pays to remember what exists. Spend the first
only on lines that change behaviour.

## Always-loaded text (skill descriptions, CLAUDE.md, memory indexes)

- A description is a pointer: what the material is, plus the distinct cases that should reach it. Lead with the key
  word. One trigger per case; synonyms of one case count as one. Name the close neighbour it is not for.
- Cut: identity the body already holds; instructions the model follows by default (test: does the line change
  behaviour?); copies of what the environment already says (package.json, `--help`, config) unless the lookup is
  expensive.
- One meaning, one place. Copies drift apart and inflate a rule's weight.

## Structure

- Two kinds of content: steps (ordered actions, each ending on a checkable completion criterion such as "every changed
  model listed") and reference (rules and facts used on demand).
- Progressive disclosure: SKILL.md under ~500 lines; rarely used branches move to files reached by a pointer that says
  when to read them; scripts do deterministic work without being read.
- Keep a concept's definition, rules and caveats under one heading.
- Split a file only when the split pays: later steps tempting the agent to rush the current one, or a different
  trigger.
- Leading words: name a behaviour with one compact word the model already knows (tight loop, tracer bullet, red, fog)
  and reuse it instead of re-explaining.
- Say what to do. A prohibition pulls the forbidden thing into attention; keep prohibitions for real hazards and pair
  each with the alternative.
- Give the reason in a clause; models generalise from reasons.

## Memory and facts

- Each stored fact carries the date learned, its source, and when it stops being true (if known).
- A newer contradicting fact replaces the old one; never keep both side by side.
- A miss caused by a stale fact: fix it everywhere it lives and add a check that catches the pattern.
- Index files: one short line per entry; detail lives in the entry.

## Long sessions

Failure modes: lost in the middle (key fact buried mid-context), poisoning (an early wrong fact reused), distraction
(irrelevant bulk), clash (contradicting facts). Moves:

- Write: offload to files (plans, ledgers, scratch notes).
- Select: load only what the current step needs, when it needs it.
- Compress: summarise tool output once used; keep error details while still debugging.
- Isolate: a subagent or fresh session for independent work, worth it from about three independent subtasks.

Compaction summaries go stale: check them against files and git before trusting them. A handoff note holds the goal,
current state, decisions with reasons, files, next step, open questions and how to verify.

## Check

- Rough cost: characters ÷ 4 ≈ tokens; `/context` in a fresh session shows the real total.
- Trigger and behaviour tests → eng-evals, branch B.
- Third-party skills: scan before reading or adopting, with
  `python3 -I <eng-skills folder>/scripts/scan_skill.py <dir>`, then rewrite in your own words.

## Credits

Ideas only, no text copied. These links are for people reading this file; Claude doesn't need to open them.

- [mattpocock/skills: writing-for-agents](https://github.com/mattpocock/skills/tree/HEAD/skills/productivity/writing-for-agents) (MIT): pointers over copies, leading words, pruning, completion criteria.
- [muratcankoylan/Agent-Skills-for-Context-Engineering: context-degradation](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/HEAD/skills/context-degradation) (MIT): how long contexts fail.
- [muratcankoylan/Agent-Skills-for-Context-Engineering: context-optimization](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/HEAD/skills/context-optimization) (MIT): write, select, compress, isolate.
- [muratcankoylan/Agent-Skills-for-Context-Engineering: memory-systems](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/HEAD/skills/memory-systems) (MIT): facts carry a date; newer replaces older.
- [anthropics/skills: skill-creator](https://github.com/anthropics/skills/tree/HEAD/skills/skill-creator) (no licence file): progressive disclosure, explain the why (ideas only).
