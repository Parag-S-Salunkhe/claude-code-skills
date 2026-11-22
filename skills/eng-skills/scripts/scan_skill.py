#!/usr/bin/env python3
"""Static scan of skill / instruction files for hidden or injected content.
Usage: python3 -I scan_skill.py <file-or-dir> [...]   (exit 1 if any HIGH finding)
Checks: hidden Unicode (zero-width, bidi, tag chars), HTML comments, long base64/hex blobs,
download-and-run commands, prompt-injection phrases, secret-looking strings, data-exfil hints, URLs.
It reads files as data only; it never runs anything from them."""
import os, re, sys

HIDDEN = re.compile('[\\u200b-\\u200f\\u202a-\\u202e\\u2060-\\u2064\\ufeff\\U000e0000-\\U000e007f]')
RULES = [  # (severity, label, regex)
 ("HIGH", "html-comment", r"<!--.*?-->"),
 ("HIGH", "pipe-to-shell", r"(curl|wget)[^\n|]*\|\s*(sudo\s+)?(ba|z)?sh\b"),
 ("HIGH", "injection-phrase", r"(?i)\b(ignore|disregard|forget)\s+(all\s+|any\s+)?(previous|prior|above|earlier)\s+(instructions|rules|prompts?)"),
 ("HIGH", "conceal-from-user", r"(?i)(do\s*n[o']t|never|without)\s+(tell|telling|inform|informing|mention|mentioning|show|showing)\s+(it\s+to\s+)?the\s+(user|human)"),
 ("HIGH", "secret-looking", r"(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{40,}|sk-[A-Za-z0-9_-]{20,}|xox[abpr]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
 ("HIGH", "credential-files", r"(~|\$HOME)/\.(ssh|aws|config/gh|netrc|docker/config)|security\s+find-(generic|internet)-password"),
 ("MED",  "credential-mention", r"keychain|\.env\b"),
 ("MED",  "exfil-hint", r"(?i)(curl|wget|fetch|requests\.(post|put))[^\n]{0,80}(-d|--data|POST|json=|data=)"),
 ("MED",  "base64-blob", r"[A-Za-z0-9+/]{120,}={0,2}"),
 ("MED",  "system-prompt-talk", r"(?i)(system prompt|you are now|new instructions|override (your|the) (rules|instructions)|jailbreak)"),
 ("MED",  "auto-approve", r"(?i)(dangerously-skip-permissions|--yolo|bypassPermissions|auto-?approve)"),
 ("LOW",  "url", r"https?://[^\s)>\]\"'`]+"),
]

def scan(fp):
    try:
        text = open(fp, encoding="utf-8", errors="replace").read()
    except OSError as e:
        return [("HIGH", "unreadable", str(e), 0)]
    out = []
    for m in HIDDEN.finditer(text):
        out.append(("HIGH", "hidden-unicode", "U+%04X" % ord(m.group()), text.count("\n", 0, m.start()) + 1))
    for sev, label, rx in RULES:
        for m in re.finditer(rx, text, re.S):
            snippet = m.group(0).replace("\n", " ")[:90]
            out.append((sev, label, snippet, text.count("\n", 0, m.start()) + 1))
    return out

def main(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                files += [os.path.join(root, n) for n in names if not n.startswith(".")]
        else:
            files.append(p)
    high = 0; urls = {}
    me = os.path.realpath(__file__)
    for fp in sorted(files):
        if os.path.realpath(fp) == me:
            continue  # its own pattern list would match itself
        for sev, label, snip, line in scan(fp):
            if sev == "LOW":
                urls.setdefault(re.sub(r"^https?://([^/]+).*", r"\1", snip), set()).add(os.path.basename(fp)); continue
            high += sev == "HIGH"
            print(f"{sev:4} {label:18} {os.path.basename(fp)[:60]}:{line}  {snip}")
    if urls:
        print("URL domains:", ", ".join(f"{d}({len(f)})" for d, f in sorted(urls.items())))
    print(f"scanned {len(files)} files, HIGH={high}")
    return 1 if high else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["."]))
