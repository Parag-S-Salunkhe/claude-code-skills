#!/usr/bin/env python3
"""park-it: a to-do list in one markdown file, read without loading the whole file. Standard library only.

  todo.py list                         titles + added dates (also records a reminder)
  todo.py item N                       one open item with its notes
  todo.py remind                       one line only when a reminder is due (5+ days, or 3-4 days at 50%)
  todo.py add TITLE [GOAL] [KNOWN] [CONTEXT]
  todo.py done N                       move item N to "## Done" with today's date
File: $PARK_IT_FILE or ~/Documents/todo.md (created on first add).
"""
import datetime
import os
import random
import re
import sys

PATH = os.path.expanduser(os.environ.get("PARK_IT_FILE", "~/Documents/todo.md"))
TODAY = datetime.date.today().isoformat()
SKELETON = "# To-do (parked work)\n\nLast reminded: never\n\n## Open\n\n## Done\n"


def load():
    try:
        return open(PATH, encoding="utf-8").read()
    except FileNotFoundError:
        return SKELETON


def save(text):
    tmp = PATH + ".tmp"
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, PATH)


def items(text):
    """Open items as (start, end, block) between '## Open' and '## Done'."""
    open_at = text.find("## Open")
    done_at = text.find("## Done")
    body_end = done_at if done_at != -1 else len(text)
    out, starts = [], [m.start() for m in re.finditer(r"(?m)^- \[ \] ", text) if open_at < m.start() < body_end]
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else body_end
        out.append((s, e, text[s:e].rstrip() + "\n"))
    return out


def title(block):
    m = re.match(r"- \[ \] \*\*(.+?)\*\*(.*)", block)
    return (m.group(1) + m.group(2).split("\n")[0]) if m else block.split("\n")[0][6:]


def mark_reminded(text):
    return re.sub(r"(?m)^Last reminded: .*$", f"Last reminded: {TODAY}", text, count=1)


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "list"
    text = load()
    its = items(text)
    if cmd == "list":
        if not its:
            print("Nothing parked.")
        for n, (_, _, b) in enumerate(its, 1):
            print(f"{n}. {title(b)}")
        if its:
            save(mark_reminded(text))
    elif cmd == "item":
        n = int(argv[2])
        print(its[n - 1][2] if 0 < n <= len(its) else "no such item")
    elif cmd == "remind":
        m = re.search(r"(?m)^Last reminded: (\d{4}-\d{2}-\d{2})", text)
        days = (datetime.date.today() - datetime.date.fromisoformat(m.group(1))).days if m else 99
        due = days >= 5 or (days >= 3 and random.random() < 0.5)
        if its and due:
            names = ", ".join(title(b).split(" (added")[0] for _, _, b in its[:2])
            print(f"Parked: {len(its)} items on your to-do list ({names}).")
            save(mark_reminded(text))
    elif cmd == "add":
        t, goal, known, ctx = (argv[2:] + ["", "", "", ""])[:4]
        if any(t.lower() in title(b).lower() for _, _, b in its):
            print("already on the list - update that item instead")
            return 1
        block = f"- [ ] **{t}** (added {TODAY})\n"
        block += "".join(f"  - {label}{v}\n" for label, v in (("Goal: ", goal), ("Known: ", known), ("Context: ", ctx)) if v)
        at = text.find("\n", text.find("## Open")) + 1
        text = text[:at] + "\n" + block + text[at:]
        save(text)
        print(f"Added to your to-do list: {t}.")
    elif cmd == "done":
        n = int(argv[2])
        if not 0 < n <= len(its):
            print("no such item")
            return 1
        s, e, b = its[n - 1]
        text = text[:s] + text[e:]
        line = f"- [x] {title(b).split(' (added')[0]} (done {TODAY})\n"
        at = text.find("\n", text.find("## Done")) + 1 if "## Done" in text else len(text)
        text = text[:at] + line + text[at:]
        save(text)
        print(f"Done: {title(b).split(' (added')[0]}")
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
