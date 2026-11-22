---
name: eng-evals
description: >-
  Evals for AI behaviour: error analysis of real outputs into failure categories, code checks and binary LLM-judge
  prompts validated against human labels, and trigger plus with/without-skill tests for skills, prompts and
  CLAUDE.md. Use when adding an AI feature, after a prompt or model change, or to check "is this skill/prompt working?".
---

# Evals

Measure the failures that actually happen, not generic quality scores.

Branch: an AI feature inside an app (chatbot, summariser, agent) → A. A skill, prompt or CLAUDE.md → B (plus A when
its output quality is the question).

## A. AI feature

1. Collect traces: input, every model and tool call, retrieved context, output. Real usage first; otherwise synthetic
   inputs varied along what matters (user type, task, difficulty, edge cases).
2. Read them with the user: pass or fail per trace. For a fail, note the first thing that went wrong (later errors
   cascade from it), as an observation ("ignored the date range"), not a theory.
3. After 30-50 traces, group the notes into 5-10 named categories, one-line definition each. Categories come from what
   you read, never from a ready-made list; split look-alikes with different causes.
4. Label every trace per category, compute rates, start with the most frequent and costly.
5. Per category, try the plain fix first: the prompt never asked for it, a tool is missing, an ordinary bug. Build an
   evaluator only for failures that persist and matter.
6. Evaluator:
   - Objective → code check (schema, regex, contains a link, length).
   - Needs judgment → LLM judge: one failure mode per judge; binary Pass/Fail with written definitions; few-shot
     examples from a training split only; structured output (reasoning, then verdict); give it only the context it
     needs.
   - Validate the judge: ~50 pass and ~50 fail human labels, split train / dev / test; iterate on dev until TPR and
     TNR are both above 0.9; measure once on test; read every disagreement.
   - Pass rate on unlabelled traces: θ = (p_obs + TNR − 1) / (TPR + TNR − 1), clipped to [0, 1].
7. Rerun after every prompt, model or feature change. Stop collecting traces when the last ~20 show no new failure type.

Judge design that misleads: 1-5 scales, one judge for "overall quality", judges built before the plain fixes,
few-shot examples taken from the test set.

## B. Skill, prompt or CLAUDE.md

- Trigger set, ~20 realistic queries with real-sounding detail: 8-10 that should load the skill, 8-10 near-misses that
  share its words but need another skill or none. Run each in a fresh non-interactive session (`claude -p`) and record
  whether the skill loaded. Adjust the description and rerun until near-misses stay at zero.
- Behaviour set, 3-5 realistic tasks: run with and without the skill on the model actually used (and a cheaper model
  if the skill must work there). Grade against written assertions; read the transcripts too, since wasted steps show
  what to cut.
- Files under `evals/` beside the skill: `triggers.json`, `cases.json`, `results.csv` (date, model, pass rates).
- A change to a skill should first fail one case (red), then pass it (green).

## Cost

Every run spends tokens or API money. State the estimate and get a yes before large batches or paid APIs; API keys
only from env vars or the keychain.

## Credits

Ideas only, no text copied. These links are for people reading this file; Claude doesn't need to open them.

- [hamelsmu/evals-skills: error-analysis](https://github.com/hamelsmu/evals-skills/tree/HEAD/skills/error-analysis) (MIT): read real outputs and sort failures into categories before writing any eval.
- [hamelsmu/evals-skills: write-judge-prompt](https://github.com/hamelsmu/evals-skills/tree/HEAD/skills/write-judge-prompt) (MIT): binary pass/fail judge prompts.
- [hamelsmu/evals-skills: validate-evaluator](https://github.com/hamelsmu/evals-skills/tree/HEAD/skills/validate-evaluator) (MIT): check a judge against human labels before trusting it.
- [anthropics/skills: skill-creator](https://github.com/anthropics/skills/tree/HEAD/skills/skill-creator) (no licence file): trigger tests and with/without-skill comparisons (ideas only).
