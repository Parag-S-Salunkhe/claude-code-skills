# Writing skills that work

What I learned building skills I use every day for real operations work.

## ✅ Do

1. **Write the description as a trigger list.** Claude decides whether to load a skill from its `description` alone. Put the real phrases people type in it ("RCA", "why did it fail", "save it"), plus what it is NOT for. A good skill with a vague description never loads.
2. **Put the hard rules first.** "Never invent a number", "draft only", "no fix without a root cause". Rules at the top survive; rules buried in step 7 get skipped.
3. **Give a checklist to copy and tick** for anything with more than four steps. It stops the model jumping from step 2 to step 6.
4. **Name the exact command.** `gh run view <id> --log-failed`, not "check the logs". A small model can follow an exact command; it guesses at a vague one.
5. **Move deterministic work into a script.** Counting characters, linting files, finding a reminder that's due: a script gets it right every time and costs no tokens.
6. **Say what "done" means.** "The database row shows active", not "the job is green".
7. **Keep `SKILL.md` short** and put the long material in `references/` files that are read only when needed.
8. **Write for the smallest model you'll use.** If a smaller model gets it right, the bigger ones will too (see [Keeping skills current](Keeping-Skills-Current.md)).

## ❌ Don't

1. **Don't put secrets, hostnames or customer names in a skill.** Skills get copied, shared and pasted. Name the keychain item instead.
2. **Don't let a skill post, send or delete on its own.** Draft, then let a person press the button.
3. **Don't load the same skill twice in a session.** It stays in context; re-loading it costs the whole file again. Re-read only the part you need.
4. **Don't stack fixes.** One hypothesis, one cheap check, then the next. Two failed fixes means stop and report.
5. **Don't add a "make it sound human" pass to writing skills.** In a study it made text look *more* like AI. Add a real detail instead.
6. **Don't let notes drift.** If a fact lives in three places, update all three in the same turn or it will be wrong in one of them next week.

## Patterns that kept paying off

- **Evidence labels:** Proven / Likely / Unknown on every cause. It makes "I don't know yet" an acceptable answer.
- **Placeholders, not guesses:** `{{your number: what it measures}}` plus a "fill before posting" list.
- **Read-only first:** look before you touch. Anything that restarts, erases or costs money waits for a yes.
- **One line per item in an index,** with the detail in the topic file. Indexes have load limits; detail beyond them is invisible.
- **Every miss ends with a check:** a wrong answer gets fixed, then guarded (a lint pattern, an eval question) so it can't come back.
