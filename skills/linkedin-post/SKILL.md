---
name: linkedin-post
description: >-
  Drafts and reviews the user's own personal LinkedIn feed posts. Interviews them for one true story, drafts in their
  voice from their real facts only, then runs an evidence-graded reach check and AI-tell check with a local checker
  script and gives a posting plan. Use when the user asks to write, draft, rewrite, polish, shorten, check or review a
  LinkedIn post (including "Part 2" of one). Not for LinkedIn job posts, profile headline or About text, comments on
  other people's posts, Slack, email, or work documents.
disallowed-tools: WebFetch
---

# linkedin-post: write or review a LinkedIn post

## Hard rules (never break; read these first)

1. **Draft only.** This skill never opens LinkedIn and never posts, comments, likes, reacts or schedules anything.
   The user copies the text and posts it themselves. (LinkedIn's User Agreement bans bots and automated access.)
2. **Never invent anything:** no fact, number, date, person, quote, feeling or anecdote. If a needed fact is missing,
   write `{{your number: what it measures}}` (or `{{your detail: ...}}`) and list it under "Fill before posting".
   Facts may come only from: what the user says in this chat, `story-bank.md`, or a file they name.
3. **Work facts come only from the story bank.** Never pull post material from work notes, runbooks, memory files,
   databases or servers. Never name customers, hostnames, IPs, internal tool or repo names, fleet sizes, incident
   data or secrets. Name a person only if the story bank says they agreed.
4. **No engagement bait or pods:** no "Comment YES", "Agree?", "Thoughts?", "tag someone", "like for Part 2", and never
   suggest asking friends or colleagues to engage at a set time.
5. **No "written with AI" label.** AI as the topic is fine. The post must be the user's voice and perspective.
6. **Every draft carries at least one detail only the user could know** (a scene, a number, an opinion from their own
   experience). This matters more than any wording polish.
7. **Never run a "make it sound human" rewrite pass.** In a preregistered study that prompt made posts look MORE like
   AI; adding one genuine idea raised trust. Fix substance, not surface.

## Files

Personal notes live in `~/Documents/LinkedIn/` (or the folder in the `LINKEDIN_NOTES` environment variable). Start from
the blank files in `templates/`.

| File | What it holds |
|---|---|
| `voice-profile.md` | How the user writes, house style, banned words, learned edits |
| `story-bank.md` | True stories and facts, consent, what is off-limits |
| `post-log.md` | Every post: time, type, format, results |
| `past-posts.md` | Published posts, verbatim, with type and impressions (style examples) |
| `references/rulebook.md` | Reach rules with evidence grades and sources |
| `references/ai-tells.md` | Evidence-backed AI tells (fix) vs folklore (avoid cheaply) |
| `scripts/check.py` | Deterministic checker (`--selftest` available) |

If a personal file is missing, say so once and continue with what the user gives in chat.

## Mode: write (default)

1. **Load** voice-profile.md, story-bank.md and the last 5 rows of post-log.md. Pick **2-3 examples** from
   past-posts.md of the same type as the new post (story, technical, advice). Match their structure, rhythm,
   formatting and tone. Never copy a sentence or a fact from them, and don't imitate an outlier post more than the rest.
2. **Interview in ONE batched message**, asking only what is missing (skip anything the story bank already answers):
   - What happened, to whom, and when?
   - What number shows it, and how was it measured?
   - What went wrong or surprised you?
   - Who is this for?
   - Is there a real photo of the person or moment, and do they agree?
   At most 5 questions, most important first. If answers are still thin, draft anyway with `{{...}}` placeholders.
   Never add slots or bullets just to hold placeholders.
3. **Shape it.**
   - Line 1: a person in a specific situation, or a concrete number. Short (aim under ~40 characters; max ~120).
     **Never a question.**
   - Topic, the person and one real number within roughly the first 40 words.
   - Then: why it mattered → what happened / what was found (a numbered list is fine) → what was done → result with
     real numbers → one honest reflection or lesson.
   - Close: a reflection, or ONE specific question a reader can answer from experience. P.S. only for a real
     follow-up (e.g. "Part 2: ...").
   - Plain, common words. At least 400 characters; hard cap 3,000 (UTF-16 count, Unicode bold letters count as 2).
   - Hashtags: 0-3 relevant ones at the end. Links only if needed, as a URL in the body.
   - Visual: one real photo (portrait if possible) of the person or moment, with consent. Video is not a reach tool.
4. **Draft in their voice** (voice-profile.md). Mark every unfilled fact with `{{...}}`. For Unicode styling use only
   sans-serif bold 𝗔𝗕𝗖 (digits 𝟭𝟮𝟯) and sans-serif italic 𝘈𝘉𝘊, never serif bold 𝐀𝐁𝐂; the checker flags others.
5. **Self-review before showing anything:**
   - Substance: is the only-the-user detail there? Is every number from them or the story bank?
   - Run the checker on the draft (write it to a temp file first): `python3 <skill dir>/scripts/check.py draft.txt`.
     Fix every BLOCK. Fix each WARN unless it is a deliberate house style (voice-profile.md says which).
   - AI tells: rewrite Part A tells from `references/ai-tells.md`; avoid Part B cheaply; never call Part B "proof".
6. **Present:** the post in one code block, ready to paste; the UTF-16 count out of 3,000; the "Fill before posting"
   list; the checker result (blocks fixed, warnings left and why); the posting plan below.
7. **Iterate on their edits.** When an edit shows a lasting preference, OFFER to add it to voice-profile.md under
   "Learned from edits". Never edit voice-profile.md or story-bank.md without a yes.
8. **After they say it is posted:** offer to add a row to post-log.md. Results come later from LinkedIn's export file.

## Mode: review (they paste their own draft)

- Run the checker and read the draft against `references/rulebook.md` and `references/ai-tells.md`.
- Every flag must **name the pattern and quote the exact line**. Group flags as: Must fix / Should fix / Optional.
- Keep their wording. Suggest minimal edits; rewrite whole sections only if asked.
- Fix grammar and typos without flattening the voice. Regional English is fine and must not be flagged as AI.

## Posting plan (give with every final draft)

- **When:** a time when the main audiences are awake and the user can be around for a couple of hours. Timing is a
  small lever (weekday vs weekend about 7%); log what they pick.
- **Replies:** answer genuine comments substantively the same day.
- **First comment:** only if it adds real context. Never as a link trick (no measurable difference).
- **Edits:** typos any time. Avoid big rewrites in the first hours. Never add a link card later.
- **Spacing:** at most 1-3 posts a week; a second post the same day competes with the first.
- **Expectations:** compare with their own baseline in post-log.md; never promise numbers.

## What never to claim

LinkedIn publishes no ranking weights. Never state reach multipliers as facts. When explaining why a choice helps,
use the grade from `references/rulebook.md` (Definitive / Moderate / Folklore).
