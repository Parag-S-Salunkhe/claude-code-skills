#!/usr/bin/env python3
"""Deterministic checks for a LinkedIn post draft. Standard library only, no network.

Usage:
  python3 check.py draft.txt          # or: cat draft.txt | python3 check.py -
  python3 check.py --selftest

Levels: BLOCK (must fix before posting), WARN (fix unless deliberate house style), INFO (facts).
Exit code 1 if any BLOCK.
Grades in brackets refer to references/rulebook.md.
"""
import os
import re
import sys
import unicodedata

MAX_UTF16 = 3000
MIN_CHARS, MIN_WORDS = 400, 50
NOTES = os.path.expanduser(os.environ.get("LINKEDIN_NOTES", "~/Documents/LinkedIn"))
VOICE_FILE = os.path.join(NOTES, "voice-profile.md")

AI_WORDS = re.compile(
    r"(?i)\b(delv(e|es|ed|ing)|testament|crucial(ly)?|pivotal|showcas(e|es|ed|ing)|underscor(e|es|ed|ing)|"
    r"meticulous(ly)?|intricate|realm|tapestry|landscape|robust|comprehensive|seamless(ly)?|leverag(e|es|ed|ing)|"
    r"foster(s|ed|ing)?|harness(es|ed|ing)?|unlock(s|ed|ing)?|elevat(e|es|ed|ing)|empower(s|ed|ing)?|notably|"
    r"fundamentally|ultimately|invaluable|game-?changer)\b")
BAIT = re.compile(
    r"(?i)(comment ['\"]?yes|\bagree\?|^\s*thoughts\?|what do you think\?|tag someone|tag a friend|"
    r"like (this|if)|drop an? \S+ (below|in the comments)|let me know in the comments|comment below|"
    r"repost if|share if you)", re.M)
FOLKLORE = {
    "negative parallelism": r"(?i)\b(it'?s|this is|isn'?t|is not) (not |just )?(about )?[^,.\n]{1,40}, (it'?s|but) ",
    "reveal bridge": r"(?im)^\s*(the (result|catch|kicker|truth|lesson)\?|here'?s (the thing|what|how|why)\b|plot twist:)",
    "announced candour": r"(?im)^\s*(let me be (honest|real|clear)|real talk|unpopular opinion|full transparency)",
    "stock opener": r"(?im)^\s*(in today'?s|have you ever wondered|most people don'?t realize)",
    "trailing -ing clause": r",\s+(highlighting|underscoring|showcasing|ensuring|emphasizing|reflecting|making it)\b",
    "nominalisation": r"(?i)\bthe (implementation|optimization|optimisation|utilization|utilisation|facilitation) of\b",
}
INVISIBLE = re.compile("[​‌‍⁠﻿­]")
URL = re.compile(r"(https?://\S+|www\.\S+|\b[\w-]+\.(com|ie|in|io|me|ai|org|net|dev)\b(/\S*)?)", re.I)


def utf16_len(text):
    return len(text.encode("utf-16-le")) // 2


def plain(text):
    """Map Unicode bold/italic letters to plain ASCII so word checks still work."""
    return unicodedata.normalize("NFKC", text)


def unicode_styled_count(text):
    return sum(1 for ch in text if 0x1D400 <= ord(ch) <= 0x1D7FF)


# House style: sans-serif bold / italic / bold-italic letters and sans-serif bold digits.
HOUSE_STYLE = ((0x1D5D4, 0x1D66F), (0x1D7EC, 0x1D7F5))


def off_style_chars(text):
    return [ch for ch in text if 0x1D400 <= ord(ch) <= 0x1D7FF
            and not any(lo <= ord(ch) <= hi for lo, hi in HOUSE_STYLE)]


def personal_banned(path=VOICE_FILE):
    words, inside = [], False
    try:
        for line in open(path, encoding="utf-8"):
            if line.startswith("## "):
                inside = line.strip().lower().startswith("## banned words")
                continue
            if inside and line.strip().startswith("- "):
                w = line.strip()[2:].split("(")[0].strip().strip('"').strip()
                if w:
                    words.append(w)
    except OSError:
        pass
    return words


def check(text, banned=None):
    out = []
    add = lambda lvl, msg: out.append((lvl, msg))
    p = plain(text)
    words = re.findall(r"\b\w[\w'-]*\b", p)
    n16 = utf16_len(text)
    lines = [l for l in text.splitlines() if l.strip()]
    first = plain(lines[0]).strip() if lines else ""

    if n16 > MAX_UTF16:
        add("BLOCK", f"Length {n16} UTF-16 units > {MAX_UTF16} (LinkedIn limit; Unicode bold letters count as 2)")
    if len(text.strip()) < MIN_CHARS or len(words) < MIN_WORDS:
        add("WARN", f"Short post ({len(text.strip())} chars, {len(words)} words): under ~400 chars is the weakest band [Moderate, rule 15]")
    for m in re.finditer(r"\{\{[^}]*\}\}", text):
        add("BLOCK", f"Unfilled placeholder: {m.group(0)}")
    for m in BAIT.finditer(p):
        add("BLOCK", f"Engagement bait: \"{m.group(0).strip()}\" [Definitive, rule 4]")
    if "?" in first:
        add("WARN", f"First line contains a question: \"{first[:80]}\" [Moderate, rule 11]")
    if len(first) > 120:
        add("WARN", f"First line is {len(first)} chars; shorter first lines did best [Moderate]")
    elif len(first) > 40:
        add("INFO", f"First line is {len(first)} chars (0-40 did best; fine if it is a strong scene)")
    first40 = " ".join(words[:40])
    if not re.search(r"\d", first40):
        add("WARN", "No number in the first ~40 words [rule 2]")
    hashtags = re.findall(r"(?<!\w)#\w+", p)
    if len(hashtags) > 3:
        add("WARN", f"{len(hashtags)} hashtags; house style is 0-3 [Folklore, rule 19]")
    urls = URL.findall(p)
    if urls:
        add("INFO", f"{len(urls)} URL(s) in body: fine, but don't let a link-preview card be the only visual [Moderate, rule 13]")
    dashes = text.count("—")
    cap = max(1, round(len(words) / 100))
    if dashes > cap:
        add("WARN", f"{dashes} em dashes (cap ~{cap} for {len(words)} words) [Folklore, rule 18]")
    styled = unicode_styled_count(text)
    if styled:
        letters = sum(1 for ch in p if ch.isalpha()) or 1
        share = styled / letters
        lvl = "WARN" if share > 0.15 else "INFO"
        add(lvl, f"Unicode bold/italic letters: {styled} ({share:.0%} of letters). House style allows hook + short headers only")
        odd = off_style_chars(text)
        if odd:
            add("WARN", f"{len(odd)} styled characters not in the house style (e.g. '{''.join(odd[:6])}'): "
                        "use sans-serif bold 𝗔𝗕𝗖 / italic 𝘈𝘉𝘊 / bold digits 𝟭𝟮𝟯, not serif bold 𝐀𝐁𝐂 or others")
    if INVISIBLE.search(text):
        add("WARN", "Invisible characters (zero-width/soft hyphen) found: remove them")
    for i, para in enumerate(re.split(r"\n\s*\n", p), 1):
        hits = [m.group(0) for m in AI_WORDS.finditer(para)]
        if len(hits) >= 2:
            add("WARN", f"Paragraph {i}: {len(hits)} AI-associated words {hits} [Definitive (general), ai-tells A1]")
        elif hits:
            add("INFO", f"Paragraph {i}: AI-associated word '{hits[0]}' (one is fine)")
    for name, pat in FOLKLORE.items():
        for m in re.finditer(pat, p):
            lvl = "WARN" if name in ("trailing -ing clause", "nominalisation") else "INFO"
            add(lvl, f"{name}: \"{m.group(0).strip()[:70]}\"")
    for w in banned if banned is not None else personal_banned():
        if re.search(r"(?i)\b" + re.escape(w) + r"\b", p):
            add("WARN", f"Personal banned word/phrase from voice-profile.md: \"{w}\"")
    if re.search(r"(?i)(written|generated|created) (with|by) (ai|chatgpt|claude)|#aigenerated", p):
        add("WARN", "Explicit AI-authorship label: disclosure of AI authorship lowers trust [rule 10]")
    add("INFO", f"Length {n16}/{MAX_UTF16} UTF-16 units, {len(words)} words, {len(hashtags)} hashtags")
    return out


def selftest():
    good = ("Our team lead turned 50 and her laptop took 9 minutes to boot.\n\n" + ("She uses it for every client call. " * 20)
            + "\n\nWe removed 40 login items in one evening.\n\n#macOS")
    r = check(good, banned=[])
    assert not [x for x in r if x[0] == "BLOCK"], r
    assert any("Length" in m for _, m in r)
    bad = "Have you ever wondered why phones get slow?\n\nShort.\n\nThoughts?\n\n#a #b #c #d #e"
    r = check(bad, banned=[])
    lv = {m.split(":")[0]: l for l, m in r}
    assert any(l == "BLOCK" and "bait" in m for l, m in r), r
    assert any("question" in m for _, m in r)
    assert any("hashtags" in m for _, m in r)
    assert any("Short post" in m for _, m in r)
    assert any(l == "BLOCK" and "placeholder" in m for l, m in check("Saved {{your number: GB}} of storage.", banned=[]))
    assert utf16_len("\U0001d5e7") == 2  # Unicode bold letter counts as 2
    bold = "\U0001d5e7\U0001d5f5\U0001d5f6\U0001d600 is a test " * 3
    assert any("Unicode bold" in m for _, m in check(bold, banned=[]))
    assert not any("house style" in m for _, m in check(bold, banned=[]))  # sans-serif bold is the house style
    serif = "\U0001d400 \U0001d41f\U0001d40e \U0001d7d7 serif bold hook " * 3  # serif bold A, f, O, digit 9
    assert any("not in the house style" in m for _, m in check(serif, banned=[]))
    ai = "We leverage robust tooling.\n\nIt fosters seamless, comprehensive growth, highlighting the realm of AI."
    r = check(ai, banned=[])
    assert any("AI-associated words" in m for _, m in r), r
    assert any("trailing -ing" in m for _, m in r), r
    assert any("banned" in m for _, m in check("I am thrilled to share this.", banned=["thrilled to share"]))
    assert check("x" * 3001, banned=[])[0][0] == "BLOCK"
    print("selftest OK")


def main(argv):
    if len(argv) > 1 and argv[1] == "--selftest":
        selftest()
        return 0
    if len(argv) < 2:
        print(__doc__)
        return 2
    text = sys.stdin.read() if argv[1] == "-" else open(argv[1], encoding="utf-8").read()
    results = check(text)
    order = {"BLOCK": 0, "WARN": 1, "INFO": 2}
    for lvl, msg in sorted(results, key=lambda x: order[x[0]]):
        print(f"{lvl:5} {msg}")
    return 1 if any(l == "BLOCK" for l, _ in results) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
