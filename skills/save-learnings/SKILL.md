---
name: save-learnings
description: >-
  Save a new, verified learning (a fix, a gotcha, a workflow input, a rule from the user) so later sessions and
  teammates can find it. Decides where it goes, writes it to all three places in the same turn (Claude's memory
  runbook, the shared team doc, and the local markdown mirror), then lint-checks what changed. Use when the user says
  "save", "save it", "add to notes", "update the doc", "add to the runbook", "remember this", "log the fix", "note
  this", or when a fix or run has turned up something new.
---

# save-learnings: every verified fix, three places, same turn

Knowledge that lives only in one chat is lost at the next session. Knowledge that lives in three places that drift
apart is worse: someone follows the stale copy. So every save writes all three, in the same turn, and checks them.

## The three places

| Place | Who reads it | Example |
|---|---|---|
| **Memory runbook** | Claude, every session | `~/.claude/projects/<project>/memory/reference_<topic>.md` |
| **Team doc** | teammates | the shared doc for that topic (Google Doc, Notion, Confluence, Claude Doc) |
| **Local mirror** | you, offline, grep | `~/Documents/<team>-runbooks/<topic>.md` |

Keep a small **doc map** at the top of this file once you have one: topic → memory file → doc → mirror.

## Steps

1. **Is it verified?** Only save what was proven: the fix worked and the real outcome was checked (the database row,
   the host state, the healthy status), not just a green job. Unverified → say so and don't save.
2. **Decide: ADD / UPDATE / DELETE / NOOP.**
   - Search all three places for the exact error text or key phrase first.
   - Same fact already there → **NOOP** (say where it is).
   - Older or wrong version there → **UPDATE** it in place; never add a second copy.
   - A method that no longer works → **DELETE** it and add it to the lint's retired patterns (see `notes-lint`).
3. **Write it the same way everywhere:**
   - Keyed by the **exact error text or task name**, so a grep finds it.
   - One line of symptom, the fix as commands, how to verify, and the date (`(verified 2026-11-17)`).
   - **No secrets** (use the name of the environment variable or keychain item instead), no customer data, no
     one-off incident details. Record the method, not the incident.
4. **Write all three in this turn.** If one place can't be reached (doc tool down), say which one is behind.
5. **Point to it.** A new runbook file → add one line to the memory index and to any router or table of contents.
6. **Lint what changed:** run the `notes-lint` quick check on the changed files. Fix any FIX it reports now.
7. **Report in one line:** what was saved, the action (ADD / UPDATE / DELETE), and where.

## Every miss ends with a check

When a saved fact turns out to be wrong or stale: fix it in all three places, then add the guard that would have
caught it (a retired pattern, an eval question, a canary test) and one row in a changelog: date, what was wrong, what
guards it now.
