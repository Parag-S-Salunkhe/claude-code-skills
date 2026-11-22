---
name: park-it
description: >-
  The user's to-do list of things parked for later (todo.md). Add an item yourself, without asking, whenever the user
  says "later", "we will do it later", "do it later", "park it", "not now", "keep it for later", "add to todo" or
  "remind me" about a task or idea; tick it off when it is done; show the list when asked ("what's on my list",
  "todo", "what did we park"). Reminds at most about twice a week, never every session.
---

# park-it: parked work, without the nagging

The list lives in one file, newest first: `~/Documents/todo.md` (or the path in the `PARK_IT_FILE` environment
variable). Use the script, so a long list never has to be read in full:

```bash
python3 <skill dir>/scripts/todo.py list          # titles + dates (also counts as a reminder)
python3 <skill dir>/scripts/todo.py item 3        # one item's notes
python3 <skill dir>/scripts/todo.py remind        # prints one line only when a reminder is due
python3 <skill dir>/scripts/todo.py add "Title" "goal" "what's known" "context"
python3 <skill dir>/scripts/todo.py done 3
```

## Add an item (automatically)

1. Trigger: the user defers something. Don't ask whether to save it: save it in the same turn.
2. One item: **bold title** + `(added YYYY-MM-DD)`, the goal in one or two lines (in their words where possible),
   what's already known (decisions, open choices, commands discussed) so the next session doesn't redo the thinking,
   and one `Context:` line. No secrets, no passwords.
3. Same item already there → update it instead of adding a duplicate.
4. Confirm in one short line: "Added to your to-do list: <title>." Nothing more.

## Done or dropped

- Done → `todo.py done <N>` (moves it to `## Done` with the date).
- Dropped by the user → delete it.
- If the work produced a verified learning, save it with `save-learnings`. A to-do list is not a runbook.

## Reminders

- Never remind in every session or every reply.
- At the start of a session's first real task, run `todo.py remind`. It prints nothing unless due (5+ days since the
  last reminder, or 3-4 days with a 50% chance) and records the date itself.
- A printed line goes at the end of a reply as-is: "Parked: <n> items on your to-do list (<two titles>)."

## Credits

My own daily rules, no outside source.
