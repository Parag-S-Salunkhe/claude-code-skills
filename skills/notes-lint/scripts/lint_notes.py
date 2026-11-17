#!/usr/bin/env python3
"""Read-only health check for a folder of markdown notes (Claude memory, runbooks, docs). Standard library only.

  lint_notes.py [DIR ...]                  full check (default: $NOTES_DIRS, colon-separated)
  lint_notes.py --files a.md b.md          quick check of just the files you changed
Levels: FIX (must fix now) and CHECK (needs a judgement). Exit 1 if any FIX. Never prints a secret value.

Checks: secrets and tokens, retired methods (retired_patterns.txt next to this script: one `regex<TAB>use instead`
per line), dead relative links, missing local paths, missing frontmatter in memory files, an index (MEMORY.md) past
its load limit, long index lines, very large files, and line-number references that break on the next edit.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SECRET = re.compile(
    r"(BEGIN [A-Z ]*PRIVATE KEY|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|xox[abpsr]-[A-Za-z0-9-]{10,}"
    r"|sk-ant-[A-Za-z0-9-]{10,}|(?i:(password|passwd|secret|token|api[_-]?key)\s*[:=]\s*['\"]?[^\s'\"$<{]{6,}))")
LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(#[^)]*)?\)")
PATH = re.compile(r"(?<![\w/.])(~/[\w./@+-]+|/Users/[\w./@+-]+)")
LINEREF = re.compile(r"\b[\w./-]+\.(md|py|sh|txt):\d+(-\d+)?\b")
INDEX_MAX_LINES, INDEX_LINE_MAX, BIG_FILE = 200, 200, 400


def retired():
    rules = []
    try:
        for line in open(os.path.join(HERE, "retired_patterns.txt"), encoding="utf-8"):
            if line.strip() and not line.startswith("#"):
                pat, _, use = line.rstrip("\n").partition("\t")
                rules.append((re.compile(pat), use or "see notes"))
    except FileNotFoundError:
        pass
    return rules


def lint(path, rules, out):
    try:
        text = open(path, encoding="utf-8").read()
    except (OSError, UnicodeDecodeError):
        return
    lines = text.splitlines()
    name = os.path.basename(path)
    base = os.path.dirname(path)
    for i, line in enumerate(lines, 1):
        if SECRET.search(line):
            out.append(("FIX", path, i, "possible secret (value not shown): replace it with the name of its env var or keychain item"))
        for pat, use in rules:
            if pat.search(line):
                out.append(("FIX", path, i, f"retired method `{pat.pattern}`: use {use}"))
        for m in LINK.finditer(line):
            target = m.group(1)
            if "://" in target or target.startswith("mailto:"):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, target))):
                out.append(("FIX", path, i, f"dead link: {target}"))
        for m in PATH.finditer(line):
            p = os.path.expanduser(m.group(1).rstrip(".,;:)"))
            if "<" not in p and not os.path.exists(p):
                out.append(("CHECK", path, i, f"path not found on this machine: {m.group(1)}"))
        if LINEREF.search(line):
            out.append(("CHECK", path, i, "line-number reference breaks on the next edit: use a grep key (a heading or exact phrase)"))
    if name == "MEMORY.md":
        if len(lines) > INDEX_MAX_LINES:
            out.append(("FIX", path, 0, f"index has {len(lines)} lines; only the first {INDEX_MAX_LINES} are loaded"))
        for i, line in enumerate(lines, 1):
            if len(line) > INDEX_LINE_MAX:
                out.append(("CHECK", path, i, f"index line is {len(line)} chars: move detail into the topic file"))
    elif "/memory/" in path and name.endswith(".md") and not text.startswith("---"):
        out.append(("CHECK", path, 0, "memory file has no frontmatter (name / description / type)"))
    if len(lines) > BIG_FILE:
        out.append(("CHECK", path, 0, f"{len(lines)} lines: consider splitting by topic with a short index file"))


def main(argv):
    if "--files" in argv:
        files = argv[argv.index("--files") + 1:]
    else:
        dirs = argv[1:] or [d for d in os.environ.get("NOTES_DIRS", "").split(":") if d]
        if not dirs:
            print(__doc__)
            return 2
        files = [os.path.join(r, f) for d in dirs for r, _, fs in os.walk(os.path.expanduser(d)) for f in fs if f.endswith(".md")]
    rules, out = retired(), []
    for f in files:
        lint(os.path.expanduser(f), rules, out)
    for lvl, p, i, msg in sorted(out, key=lambda x: (x[0] != "FIX", x[1], x[2])):
        print(f"{lvl:5} {p}:{i}  {msg}" if i else f"{lvl:5} {p}  {msg}")
    fixes = sum(1 for x in out if x[0] == "FIX")
    print(f"\n{len(files)} files · FIX {fixes} · CHECK {len(out) - fixes}")
    return 1 if fixes else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
