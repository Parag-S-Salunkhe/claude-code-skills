# Questions & Answers

1. <ins>What's the difference between a skill, CLAUDE.md and memory?</ins>

`CLAUDE.md` is loaded into every session: keep it for always-on rules. **Memory** files hold facts Claude has learned about you and your work. A **skill** is loaded only when a request matches its description, so it can be long and detailed without costing anything the rest of the time.

2. <ins>Where do skills go?</ins>

`~/.claude/skills/<name>/SKILL.md` for you, in every project. `<repo>/.claude/skills/<name>/SKILL.md` for everyone working on that repo.

3. <ins>My skill never loads. Why?</ins>

Almost always the description. Claude chooses from the description alone, so put in the words people actually type, and say what the skill is not for, so it doesn't lose to a similar one. Test it with 10 should-trigger and 10 should-not prompts.

4. <ins>Are skills safe to install from someone else?</ins>

Read them first: a skill is instructions your AI will follow, and scripts it may run. These ones use only the Python standard library and macOS built-ins, make no network calls (except `gh` in `workflow-runner`, which talks to GitHub as you), and never print secrets.

5. <ins>Why are these "generic versions"?</ins>

The skills I use at work name internal systems, hosts and tools. Sanding those off would leave gaps, so these were rewritten from scratch with the same rules and structure and no internal details.

6. <ins>Why does `linkedin-post` refuse to post for me?</ins>

LinkedIn's User Agreement bans bots and automated access, and accounts with automated activity get restricted. The skill drafts, checks and plans; you press Post.

7. <ins>Why does `park-it` add items without asking?</ins>

Because "should I add that to your list?" after every "later" is its own kind of nagging. It adds the item, confirms in one line, and reminds you at most about twice a week.

8. <ins>Do the skills work on Windows or Linux?</ins>

The instructions do. `secrets-guard`'s scripts use the macOS keychain (`security`) and macOS commands. On Linux, use `secret-tool` (libsecret) instead; the rules stay the same.
