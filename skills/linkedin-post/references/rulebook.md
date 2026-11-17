# Reach rulebook (graded)

Source: a deep-research pass (Nov 2026) over LinkedIn engineering and policy pages, peer-reviewed studies and large
vendor datasets. Re-check yearly: platforms change.

## Grades

- **Definitive (LinkedIn):** first-party LinkedIn document. Proves a signal or policy exists, never its weight.
- **Definitive (general):** strong peer-reviewed evidence from other platforms; direction holds, size on LinkedIn unknown.
- **Reported:** LinkedIn executives quoted by the press.
- **Moderate:** large vendor datasets with partly disclosed methods (all sell LinkedIn tools), or preprints.
- **Folklore:** unsourced, contradicted, or traced only to blogs and repos. Follow only when it is free.

## How the feed works (confirmed, 2025-2026)

- Retrieval: an LLM turns each post (text + author name, headline, company, industry + engagement percentile) into an
  embedding and matches it against members' profiles and engagement history. About 2,000 candidates per member, from
  the network and from strangers in one pool. New posts are indexed in about a minute; engagement percentiles refresh
  within about 30 minutes. (arXiv 2510.14223; LinkedIn Engineering, 12 Mar 2026)
- Ranking: a transformer predicts click, skip, long dwell, like, comment and share, combined with private weights.
  Skips lower a post's score. (LinkedIn Engineering 2020 dwell post; 2026 feed post; Feed-SR arXiv 2602.12354)
- Withdrawn, do not cite: LiGR (arXiv 2502.03417) and 360Brew (arXiv 2501.16450).

## Rules

| # | Rule | Grade |
|---|---|---|
| 1 | Make the opening worth stopping for; a skipped post is penalised | Definitive (LinkedIn) |
| 2 | Topic (specific domain nouns), a person and a real number in roughly the first 40 words | Definitive mechanism; Moderate on "40" |
| 3 | Keep the profile headline concrete about your topics (it is embedded with every post) | Definitive (LinkedIn) |
| 4 | No bait, no pods, no reciprocal-like deals, no automated actions | Definitive (LinkedIn) |
| 5 | First-hand insight beats recycled generic advice | Definitive (LinkedIn), stated direction |
| 6 | Lead with a person in a specific situation; concern or awe over sadness or "excited to announce"; put the useful payload inside the story | Definitive (general) |
| 7 | Plain, common words | Definitive (general) |
| 8 | Never invent; include one detail only the author could know | Definitive (general) + preprint |
| 9 | Fix evidence-backed AI tells (see ai-tells.md Part A) | Definitive (general), as reader cues |
| 10 | AI edits, never authors; nothing auto-generated reaches the feed | Reported |
| 11 | Don't open with a question | Moderate |
| 12 | Default visual: one real photo, portrait if possible; video is not a reach tool; documents are not a reach trick under 5k followers | Moderate |
| 13 | If a link is needed, put the URL in the body; avoid the link-preview card as the only visual (about -35%) | Moderate |
| 14 | Reply substantively to genuine comments (about +30% engagement, same account) | Moderate (association) |
| 15 | Avoid posts under about 400 characters or 50 words | Moderate |
| 16 | Posting more per week does not raise reach per post | Moderate |
| 17 | Closing question optional and specific; never "Thoughts?" | Moderate |
| 18 | Avoid em-dash overuse, "It's not X, it's Y", heavy Unicode bold, emoji bullets | Folklore, cheap to follow |
| 19 | 0-3 relevant hashtags | Folklore, a precaution |
| 20 | Don't edit a link card into a post after publishing | Folklore, a precaution |

## Dropped claims (do not repeat)

- "+50% reach for faces on LinkedIn": unsourced. Only Instagram 2014 data (+38% likes, +32% comments).
- "1,300-2,500 characters is the peak": only the ~400-character floor is safe; the length studies contradict each other.
- "Link in first comment": no measurable difference (-2%); LinkedIn doesn't count comment-link clicks.
- "Reply within the first hour" / "golden hour": no study measured reply speed; LinkedIn never used the term.
- "Post Tue-Thu mornings": studies disagree on the hour; weekday vs weekend about 7% for personal profiles.
- "0 vs 3-5 hashtags": no usable evidence either way.
- "Hook must fit 140 characters": no study measures the "see more" cut. Short first lines did best (0-40 chars).
- "Comments are worth 15x likes", "links cut reach 60%", "edits reset distribution": no primary source.

## Your own data

Keep your results in `post-log.md` and compare new posts with **your** baseline, not with anyone else's numbers.
Story posts with a real person and stakes often beat technical updates by a wide margin; check whether that holds for you.
