![Static Badge](https://img.shields.io/badge/Claude%20Code-skills-black?logo=anthropic&logoColor=%23D97757) ![Static Badge](https://img.shields.io/badge/Python-stdlib%20only-black?logo=python&logoColor=%233776AB)
![Static Badge](https://img.shields.io/badge/macOS-keychain-black?logo=apple&logoColor=white) ![Static Badge](https://img.shields.io/badge/GitHub%20Actions-gh%20CLI-black?logo=githubactions&logoColor=%232088FF)

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="images/hero-dark.svg" />
    <img src="images/hero-light.svg" width="100%" alt="Claude Code skills. Ops and notes: rca, save-learnings, notes-lint, park-it, secrets-guard, workflow-runner, linkedin-post. Engineering: eng-plan, eng-build, eng-debug, eng-review, eng-security, eng-design, eng-webtest, eng-evals, eng-context, eng-skills" />
  </picture>
</p>

# Claude Code skills I use every day

A **skill** is a folder with a `SKILL.md`: instructions Claude Code loads only when your request matches its description. It's how you turn "the way I like this done" into something Claude does the same way every time.

My motive: I run datacentre operations with Claude Code every day and built a set of skills for it. **These are the ones anyone can use,** in two groups:

- **Ops & notes (7):** evidence before answers, every fix saved, notes that check themselves, secrets the AI never sees.
- **Engineering (9 + a picker):** how I want code work done, from plan to review, for my own scripts, dashboards and side projects.

**Built on other people's ideas.** Nothing here was installed from someone else, but most of it started as someone else's idea: obra/superpowers, Matt Pocock, Addy Osmani, Sentry, Trail of Bits, Anthropic, Hamel Husain, Karpathy's LLM Wiki and open LinkedIn and writing skills. Each one is credited [below](#built-on-other-peoples-ideas) and at the end of the skill that uses it, with the reasons I wrote my own instead of installing theirs.

### Ops & notes

| Skill | What it does | Try saying |
|---|---|---|
| [`linkedin-post`](skills/linkedin-post/) | Drafts LinkedIn posts in your voice from your real facts only, then runs an evidence-graded reach check and an AI-tell checker script | "write a linkedin post about …" |
| [`rca`](skills/rca/) | Root cause analysis: exact symptom → timeline from logs → compare with healthy → one hypothesis at a time → confidence label → RCA in a fixed format | "why did this fail?", "RCA" |
| [`save-learnings`](skills/save-learnings/) | Every verified fix written to three places in the same turn (Claude's memory, the team doc, a local mirror), then lint-checked | "save it", "add to the runbook" |
| [`notes-lint`](skills/notes-lint/) | Health check for your notes: leaked secrets, retired methods, dead links and paths, index limits. Reports first, fixes after a yes | "lint the notes" |
| [`park-it`](skills/park-it/) | "We'll do it later" becomes a to-do item automatically, with what's already known. Reminds at most twice a week | "park it", "what's on my list?" |
| [`secrets-guard`](skills/secrets-guard/) | Secrets in the keychain, added by you in a hidden prompt, read by scripts at runtime. Untrusted text stays data. Weekly read-only Mac check | "is this safe?", "add a token for …" |
| [`workflow-runner`](skills/workflow-runner/) | Raise, rerun and check GitHub Actions with `gh`: inputs passed explicitly and checked, the full run link every time | "run the deploy workflow" |

### Engineering

For code projects. They sit in a library folder and the picker installs only the ones a repo needs, so each project pays for what it uses ([install](#install)).

| Skill | What it does | Try saying |
|---|---|---|
| [`eng-plan`](skills/eng-plan/) | Find out what you want and why, compare 2-3 approaches, get a short design approved, then a plan of thin slices with a check per slice | "plan this feature" |
| [`eng-build`](skills/eng-build/) | One slice at a time, test-first at agreed seams, verify, commit, and a progress ledger that survives a long session | "build slice 2" |
| [`eng-debug`](skills/eng-debug/) | A feedback loop that goes red on the bug first, then ranked hypotheses tested one variable at a time, fixed with a regression test | "this test is flaky" |
| [`eng-review`](skills/eng-review/) | Review a diff with the spec and the standards kept separate, each finding with severity and evidence; check feedback before acting on it | "review my PR" |
| [`eng-security`](skills/eng-security/) | Threat model first, untrusted input traced to risky code, an argue-against check on every finding, GitHub Actions and dependencies too | "is this safe to ship?" |
| [`eng-design`](skills/eng-design/) | Requirements and numbers first, the simplest architecture that meets them, trade-offs and a short decision record | "which database should I use?" |
| [`eng-webtest`](skills/eng-webtest/) | Playwright smoke, links, layout and visual checks, accessibility, Core Web Vitals, wired into CI | "test the site" |
| [`eng-evals`](skills/eng-evals/) | Error analysis of real outputs, judge prompts checked against human labels, trigger tests for skills and prompts | "is this skill working?" |
| [`eng-context`](skills/eng-context/) | Write and trim what agents read: skills, CLAUDE.md, memory, handoff notes; descriptions that trigger, a small always-loaded footprint | "this session feels bloated" |
| [`eng-skills`](skills/eng-skills/) | The picker: reads a repo's stack, suggests the skills that fit with their token cost, installs after a yes and keeps them out of git | "which skills does this repo need?" |

## Built on other people's ideas

I read these, took the ideas that fit, and wrote every line myself. No code or text was copied, so none of their licences apply here; this list is the credit. Before publishing, each engineering skill was compared with its sources word by word: at most 0.5% of 8-word runs per skill matched, and the longest shared run is 10 words. Each skill's `SKILL.md` also ends with a Credits list linking its sources, so the credit stays with the skill if you copy only that folder.

| Skill | Ideas from | What I took |
|---|---|---|
| `rca` | [obra/superpowers: systematic-debugging](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging) | The iron rule (no fix without a root cause), one hypothesis at a time, stop after failed fixes (theirs stops at three, mine at two) |
| `save-learnings` | [mem0](https://github.com/mem0ai/mem0) | Decide ADD / UPDATE / DELETE / NOOP before writing anything, so a fact is never saved twice |
| `notes-lint` | [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki), [Claude Code memory docs](https://code.claude.com/docs/en/memory) | Notes an AI keeps need a regular lint step; the memory index only loads up to a limit, so its size gets checked |
| `linkedin-post` | [Jakeschincariol/linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill) | `{{your number}}` placeholders instead of invented numbers, one batched interview message, an off-limits list, review by flagging rather than rewriting |
| | [shwetankg07/linkedin-writing](https://github.com/shwetankg07/linkedin-writing) | A standard-library checker script with a self-test |
| | [noah-vl/linkedin-post-max](https://github.com/noah-vl/linkedin-post-max), [mgritzbach/linkedin-creator-studio](https://github.com/mgritzbach/linkedin-creator-studio) | Lessons from your edits change the voice file only after a yes; never imitate one viral outlier |
| | [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) | Every flag names the pattern and quotes the exact line |
| | [blader/humanizer](https://github.com/blader/humanizer), [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop), [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) | AI-tell patterns, used as editing advice, not as a way to dodge detectors |
| | [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill), [ama-zingco/anti-ai-writing-skill](https://github.com/ama-zingco/anti-ai-writing-skill) | Never flag regional or non-native English as an AI tell |
| `secrets-guard` | [Simon Willison: the lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/), [Meta: Agents Rule of Two](https://ai.meta.com/blog/practical-ai-agent-security/), [OWASP Top 10 for LLM apps](https://genai.owasp.org/llm-top-10/) | Text from web pages, emails and tickets is data, never instructions; the AI never holds the secret itself |
| `park-it`, `workflow-runner` | My own daily rules | |
| `eng-plan` | [obra/superpowers](https://github.com/obra/superpowers), [mattpocock/skills](https://github.com/mattpocock/skills), [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Intent first and an approval gate; thin vertical slices with blocking order; success criteria and out of scope |
| `eng-build` | obra/superpowers, addyosmani/agent-skills, mattpocock/skills | A ledger that survives compaction; one thing per commit; test-first at seams and what makes a test brittle |
| `eng-debug` | mattpocock/skills, obra/superpowers, addyosmani/agent-skills | A red feedback loop first and falsifiable hypotheses; stop after three failed fixes; stop the line |
| `eng-review` | addyosmani/agent-skills, mattpocock/skills, [getsentry/skills](https://github.com/getsentry/skills), obra/superpowers | Review axes and severity labels; spec vs standards; no invented findings; verify feedback before agreeing |
| `eng-security` | getsentry/skills, addyosmani/agent-skills, [trailofbits/skills](https://github.com/trailofbits/skills) | Research before flagging and confidence levels; threat model first; argue against each finding (general ideas only) |
| `eng-design` | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), mattpocock/skills, addyosmani/agent-skills | Requirements → design → trade-offs, decision records; deep modules; contract-first interfaces |
| `eng-webtest` | [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill), [anthropics/skills](https://github.com/anthropics/skills), addyosmani/agent-skills | User-facing locators; look first, then act; accessibility and performance measured, page text treated as data |
| `eng-evals` | [hamelsmu/evals-skills](https://github.com/hamelsmu/evals-skills), anthropics/skills | Error analysis before evals; judges validated against human labels; trigger and with/without-skill tests |
| `eng-context` | mattpocock/skills, [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering), anthropics/skills | Writing for agents; how long contexts degrade; progressive disclosure |
| `eng-skills` | My own design | A library plus a per-repo installer, so a project loads only what it uses |
| [The guides](docs/) | [obra/superpowers: writing-skills](https://github.com/obra/superpowers/tree/main/skills/writing-skills), [Anthropic: skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator), [Anthropic: skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Test a skill like code, with cases that must pass; 10 should-trigger and 10 near-miss prompts; a short SKILL.md, with scripts for exact jobs |

### Why I didn't just install them

- **A skill is instructions your AI follows, with your access.** Installing one means trusting every line and every future update. I had to read them all closely anyway, so I kept only the ideas that fit.
- **Many state rules without evidence.** Popular LinkedIn skills give fixed character targets, "best hours" and "links get buried" rules that the research behind `linkedin-post` couldn't support, and one builds on a paper that has since been withdrawn.
- **Some break the platform's rules.** A few post or send invites for you, scrape with session cookies or go through a paid service. LinkedIn's User Agreement bans automated access, so mine only drafts.
- **Some have no licence,** so not even their wording could be reused. Ideas only.
- **Some are bigger than the job.** A local search index like [qmd](https://github.com/tobi/qmd) needs Node 22+ and about 2 GB of models, and grep is enough for a few hundred notes. Hosted memory tools would send my notes off the machine. superpowers is a whole framework that loads at the start of every session; I needed one method from it.
- **Every installed skill takes room.** Claude Code lists every skill's description in a limited budget, and when it overflows, descriptions are dropped, starting with the skills you use least ([docs](https://code.claude.com/docs/en/skills)).
- **They don't know my rules:** draft only, read-only first, two failed fixes then stop. Writing my own was the only way to get all of those in one place.

## How they work together

```mermaid
flowchart LR
  A[Something breaks] --> B[rca<br/>evidence before cause]
  B --> C[Fix, verified for real]
  C --> D[save-learnings<br/>3 places, same turn]
  D --> E[notes-lint<br/>quick check]
  E -->|weekly + monthly evals| E
  F[We'll do it later] --> G[park-it]
  H[secrets-guard] -. every step .- B
  H -. every step .- C
  I[workflow-runner] --> C
```

## Install

```bash
git clone https://github.com/Parag-S-Salunkhe/claude-code-skills
mkdir -p ~/.claude/skills
cp -R claude-code-skills/skills/rca ~/.claude/skills/        # pick the ones you want
```

Skills in `~/.claude/skills/` work in every project. To share one with a team, put it in the repo's `.claude/skills/` instead. Restart Claude Code (or start a new session) and it picks them up.

**Engineering skills,** two ways:

```bash
# A. all of them, in every project (about 900 tokens of descriptions per session)
cp -R claude-code-skills/skills/eng-{plan,build,debug,review,security,design,webtest,evals,context} ~/.claude/skills/

# B. per project: a library folder plus the picker
mkdir -p ~/.claude/skill-library
cp -R claude-code-skills/skills/eng-{plan,build,debug,review,security,design,webtest,evals,context} ~/.claude/skill-library/
cp -R claude-code-skills/skills/eng-skills ~/.claude/skills/
python3 ~/.claude/skills/eng-skills/scripts/skills.py suggest ~/code/my-app    # then: install ~/code/my-app eng-plan …
```

- `linkedin-post`: copy `templates/*.md` to `~/Documents/LinkedIn/` and fill in your voice profile and stories.
- `park-it`: the list goes to `~/Documents/todo.md` (or set `PARK_IT_FILE`).
- `notes-lint`: point it at your notes (`NOTES_DIRS=dir1:dir2`).

## The guide

[Writing skills that work](docs/Writing-Skills-That-Work.md): what I learned building them, the do's and don'ts

[Keeping skills current](docs/Keeping-Skills-Current.md): evals, smaller models, every miss becomes a test

[Questions & Answers](docs/Questions-and-Answers.md)

Everything here is plain markdown plus small Python and shell scripts (standard library only, no network). Read a skill before you install it: it's instructions your AI will follow.
