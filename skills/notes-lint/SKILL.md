---
name: notes-lint
description: >-
  Health-checks a notes system (Claude memory files and their MEMORY.md index, runbooks, team-doc mirrors): leaked
  secrets, retired methods, dead links and paths, index size and line length, missing frontmatter, oversized files,
  line-number references. Reports everything; fixes only proven issues after the user's yes. Use when the user says
  "lint", "lint the notes", "health check", "check the docs", "are the notes in sync", "audit secrets", "clean up
  memory", "is anything stale", and run its quick mode after every save-learnings save.
---

# notes-lint: notes that check themselves

One read-only script does the mechanical checks; you do the judgement calls. Never print a secret value.

## Quick check (after every save)

```bash
python3 <skill dir>/scripts/lint_notes.py --files <each file you changed>
```

Any `FIX` → correct it in the same turn. A secret → replace it with the name of its environment variable or keychain
item, and tell the user to rotate it if it was ever shared.

## Full check

Copy and tick:
```
- [ ] 1 Run the script   - [ ] 2 Doc vs mirror   - [ ] 3 Judge every CHECK   - [ ] 4 Report   - [ ] 5 Fix after a yes
```

1. `python3 <skill dir>/scripts/lint_notes.py ~/.claude/projects/<project>/memory ~/Documents/<team>-runbooks`
   (or set `NOTES_DIRS=dir1:dir2`).
2. **Doc vs mirror.** Export each team doc to markdown and diff it with its local mirror. The newest dated text wins;
   fix the stale side.
3. **Judge each CHECK.** What makes a fix "proven":
   - *Long index line:* every fact in it is also in the topic file → shorten the line. A fact is missing → move it into
     the topic file first, dated, then shorten.
   - *Index past its load limit:* anything past the limit is invisible to Claude. Shorten lines first, then group
     entries into per-area index files with one line each.
   - *Line-number reference:* replace `file:12-17` with a grep key (a heading or an exact phrase) that survives edits.
   - *Path not found:* a typo, a moved file, or a path from another machine. Fix or mark it as an example.
   - *Big file (> 400 lines):* split by area; the old file becomes a short index.
4. **Report, short:** the counts line, each FIX with file:line and the fix you propose, each CHECK with your verdict
   (proven fix / needs the user / leave).
5. **Apply** only FIX items and CHECK items proven in step 3, after the user's yes. Secrets and dead links are always
   proven. Re-run step 1 and confirm `FIX 0`.

## Keeping it current (the learning loop)

- **Every save:** save-learnings picks ADD / UPDATE / DELETE / NOOP and runs the quick check, so there are no
  duplicates and no drift.
- **Every retired method:** one line in `scripts/retired_patterns.txt` (`regex<TAB>what to use instead`), so the lint
  flags every old copy, including ones you forgot about.
- **Every real miss:** the question and the right answer go into an evals file; the next eval run tests it.
- **Weekly:** a full check. **Monthly:** re-run the evals on a smaller model. If the score drops or the run gets
  slower, the notes got worse: fix that before adding more.

## Rules

- Report everything; change nothing until the user says yes. Never delete a memory file or doc section without a yes.
- Don't "fix" open questions in the notes: they are real gaps in knowledge. List them so the user can answer them.

## Credits

Ideas only, no text copied. These links are for people reading this file; Claude doesn't need to open them.

- [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki): notes an AI keeps need a regular lint step.
- [Claude Code memory docs](https://code.claude.com/docs/en/memory): the memory index only loads up to a limit.
