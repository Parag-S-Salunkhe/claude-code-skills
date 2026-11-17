# Keeping skills current

Skills rot the same way docs do: a method gets replaced, a tool changes its flags, a rule gets an exception. Here is the routine that keeps mine honest.

| When | What runs | Why |
|---|---|---|
| Every save | `notes-lint` quick check on the changed files | no secret, dead link or retired method gets in |
| Every miss | fix it in all three places, add the guard, add a changelog row | the same mistake can't happen twice |
| Every retired method | one line in `retired_patterns.txt` | the lint finds every old copy, including forgotten ones |
| Weekly | full `notes-lint`, plus `secrets-guard`'s Mac check | drift and new launch agents get noticed |
| Monthly | evals re-run on a smaller model | skills shouldn't depend on the biggest model |

## Evals: how to test a skill

Each skill can have an `evals/evals.md` with:

1. **Behaviour cases:** a prompt, what the answer **must** do, and what it **must not** do. A case passes only if every "must" holds. Example from `linkedin-post`: "Write a post: I cut build time at work" (no numbers given) → must use `{{your number}}` placeholders; must not invent minutes or percentages.
2. **Trigger tests:** 10 prompts that should load the skill and 10 near misses that shouldn't. This tunes the description.
3. **A results log:** date, models, pass/fail, what was changed afterwards.

Run the cases with a fresh session per model: a small, a medium and a large one. My first `linkedin-post` run caught three things the large model never did: the small model used serif bold letters, the medium model asked 7 interview questions instead of 5, and the small model padded drafts with placeholders. Each became a rule or a checker test.

## Every miss becomes a test

When Claude gives a wrong answer from the notes (a stale fact, a retired method):

1. Fix the fact everywhere it lives.
2. Add the guard that would have caught it: a retired pattern, an eval question with the right answer, or a canary test.
3. Log one row: date, what was wrong, what guards it now.

The point isn't to never be wrong. It's to never be wrong the same way twice.
