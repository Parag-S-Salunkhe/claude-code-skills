#!/usr/bin/env python3
"""Engineering skill library manager.

Library (never auto-loaded): $ENG_SKILLS_LIB/eng-*/SKILL.md (default ~/.claude/skill-library)
Installs copies into <repo>/.claude/skills/ so they load only in that project.

  skills.py list                         library skills + description size
  skills.py suggest <repo>               skills that fit the repo, with reasons + token cost
  skills.py install <repo> <name>...     copy (scanned first), hide from git, record hashes
  skills.py status  <repo>               installed skills: ok / library newer / edited locally
  skills.py update  <repo> [--force]     recopy skills whose library version changed
  skills.py remove  <repo> <name>...     delete installed copies
  skills.py tokens  [<repo>]             always-loaded text per session (skill descriptions, CLAUDE.md, MEMORY.md)
"""
import hashlib, importlib.util, json, os, re, shutil, subprocess, sys

HOME = os.path.expanduser("~")
LIB = os.path.expanduser(os.environ.get("ENG_SKILLS_LIB") or os.path.join(HOME, ".claude", "skill-library"))
USER_SKILLS = os.path.join(HOME, ".claude", "skills")
MANIFEST = ".eng-skills.json"
CORE = ["eng-plan", "eng-build", "eng-debug", "eng-review"]

UI = {"react", "vue", "svelte", "astro", "next", "nuxt", "vite", "@sveltejs/kit", "solid-js", "gatsby",
      "@11ty/eleventy", "preact", "lit", "@angular/core", "remix", "@remix-run/react", "tailwindcss"}
SERVER = {"express", "fastify", "koa", "hono", "@nestjs/core", "flask", "django", "fastapi", "starlette",
          "next-auth", "passport", "jsonwebtoken", "bcrypt", "@auth/core", "lucia", "@clerk/nextjs",
          "@supabase/supabase-js", "firebase", "stripe"}
AI = {"openai", "@anthropic-ai/sdk", "anthropic", "langchain", "@langchain/core", "llama-index", "llamaindex",
      "ai", "@ai-sdk/openai", "@google/generative-ai", "google-genai", "transformers", "ollama", "litellm"}
DATA = {"prisma", "@prisma/client", "mongoose", "pg", "mysql2", "sqlalchemy", "drizzle-orm", "sequelize",
        "typeorm", "psycopg", "psycopg2", "redis", "ioredis", "kafkajs", "celery"}


def die(msg):
    print(msg); sys.exit(1)


def frontmatter(path):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return "", ""
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return "", ""
    fm = m.group(1)
    name = (re.search(r"^name:\s*(.+)$", fm, re.M) or [None, ""])[1].strip()
    d = re.search(r"^description:\s*(.*?)(?=^\w[\w-]*:|\Z)", fm, re.S | re.M)
    desc = re.sub(r"\s+", " ", d.group(1).replace(">-", "").replace(">", "", 1)).strip().strip('"') if d else ""
    return name, desc


def lib_skills():
    if not os.path.isdir(LIB):
        die(f"library not found: {LIB}\nCopy the eng-* skill folders there, or set ENG_SKILLS_LIB.")
    return sorted(n for n in os.listdir(LIB) if n.startswith("eng-") and n != "eng-skills" and
                  os.path.isfile(os.path.join(LIB, n, "SKILL.md")))


def tree_hash(d):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(d)):
        for f in sorted(files):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, d).encode()); h.update(open(p, "rb").read())
    return h.hexdigest()[:16]


def desc_tokens(skill_dir):
    name, desc = frontmatter(os.path.join(skill_dir, "SKILL.md"))
    return (len(name) + len(desc)) // 4


def load_scanner():
    spec = importlib.util.spec_from_file_location("scan_skill", os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_skill.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def repo_files(repo, limit=4000):
    out = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", ".venv", "venv", "dist", "build", ".next",
                                                 "__pycache__", ".astro", "vendor"}]
        out += [os.path.relpath(os.path.join(root, f), repo) for f in files]
        if len(out) > limit:
            break
    return out


def deps(repo, files):
    found = set()
    for f in files:
        base = os.path.basename(f)
        p = os.path.join(repo, f)
        try:
            if base == "package.json":
                j = json.load(open(p))
                for k in ("dependencies", "devDependencies"):
                    found |= set((j.get(k) or {}).keys())
            elif re.match(r"requirements.*\.txt$", base) or base in ("pyproject.toml", "Pipfile"):
                for line in open(p, errors="replace"):
                    m = re.match(r"\s*\"?([A-Za-z0-9_.\-]+)", line)
                    if m:
                        found.add(m.group(1).lower())
        except (OSError, ValueError):
            pass
    return found


def suggest(repo):
    files = repo_files(repo)
    ds = deps(repo, files)
    picks = {s: "core for any code project" for s in CORE}
    html = [f for f in files if f.endswith((".html", ".astro", ".vue", ".svelte", ".jsx", ".tsx"))]
    if ds & UI or html:
        picks["eng-webtest"] = "has a web UI (" + ", ".join(sorted(ds & UI)[:3] or html[:2]) + ")"
    sec = sorted(ds & SERVER)
    wf = [f for f in files if f.startswith(".github/workflows/")]
    if sec or wf or any(os.path.basename(f) in ("Dockerfile",) for f in files):
        why = []
        if sec: why.append("server/auth/payment deps: " + ", ".join(sec[:3]))
        if wf: why.append(f"{len(wf)} GitHub workflow(s)")
        picks["eng-security"] = "; ".join(why) or "container build"
    if ds & AI or any("prompt" in f.lower() for f in files):
        picks["eng-evals"] = "AI features (" + ", ".join(sorted(ds & AI)[:3] or ["prompt files"]) + ")"
    agent_docs = [f for f in files if os.path.basename(f) in ("CLAUDE.md", "AGENTS.md", "SKILL.md")]
    if agent_docs:
        picks["eng-context"] = "agent docs present: " + ", ".join(agent_docs[:3])
    infra = [f for f in files if f.endswith(".tf") or "docker-compose" in f or f.startswith(("k8s/", "helm/"))]
    if ds & DATA or infra or len(files) < 15:
        picks["eng-design"] = ("new or near-empty repo" if len(files) < 15 else
                               "data/infra: " + ", ".join((sorted(ds & DATA) + infra)[:3]))
    installed = read_manifest(repo)
    total = 0
    print(f"Suggested for {repo}:")
    for s in lib_skills():
        if s in picks:
            t = desc_tokens(os.path.join(LIB, s)); total += t
            mark = " (installed)" if s in installed else ""
            print(f"  {s:13} ~{t:3} tok  {picks[s]}{mark}")
    print(f"  per-session cost in this repo: ~{total} tokens (descriptions only; a body loads only when used)")
    print("  not suggested: " + (", ".join(s for s in lib_skills() if s not in picks) or "none"))


def skills_dir(repo):
    return os.path.join(repo, ".claude", "skills")


def read_manifest(repo):
    p = os.path.join(skills_dir(repo), MANIFEST)
    try:
        return json.load(open(p))
    except (OSError, ValueError):
        return {}


def write_manifest(repo, m):
    os.makedirs(skills_dir(repo), exist_ok=True)
    json.dump(m, open(os.path.join(skills_dir(repo), MANIFEST), "w"), indent=1, sort_keys=True)


def git_exclude(repo):
    try:
        top = subprocess.run(["git", "-C", repo, "rev-parse", "--show-toplevel"], capture_output=True, text=True)
        if top.returncode:
            return "not a git repo (nothing to hide)"
        ex = subprocess.run(["git", "-C", repo, "rev-parse", "--git-path", "info/exclude"],
                            capture_output=True, text=True).stdout.strip()
        ex = ex if os.path.isabs(ex) else os.path.join(repo, ex)
        rel = os.path.relpath(skills_dir(repo), top.stdout.strip())
        lines = [f"/{rel}/eng-*/", f"/{rel}/{MANIFEST}"]
        have = open(ex).read().splitlines() if os.path.exists(ex) else []
        new = [l for l in lines if l not in have]
        if new:
            os.makedirs(os.path.dirname(ex), exist_ok=True)
            with open(ex, "a") as f:
                f.write("\n# eng-skills (local only)\n" + "\n".join(new) + "\n")
        tracked = subprocess.run(["git", "-C", repo, "ls-files", rel], capture_output=True, text=True).stdout
        warn = " WARNING: some .claude/skills files are already tracked by git" if "eng-" in tracked else ""
        return "hidden from git via .git/info/exclude" + warn
    except OSError as e:
        return f"could not update git exclude: {e}"


def install(repo, names, overwrite=False):
    if os.path.realpath(skills_dir(repo)) == os.path.realpath(USER_SKILLS) or os.path.realpath(repo) == HOME:
        die("refused: installing into the home folder would load eng-* skills in every session.\n"
            f"Use a project folder, or read {LIB}/<name>/SKILL.md for a one-off task.")
    scanner = load_scanner()
    m = read_manifest(repo)
    for n in names:
        src = os.path.join(LIB, n)
        if n not in lib_skills():
            print(f"  {n}: not in library"); continue
        dst = os.path.join(skills_dir(repo), n)
        if os.path.exists(dst) and n not in m and not overwrite:
            print(f"  {n}: {dst} exists and was not installed by this tool; skipped"); continue
        high = [h for root, _, files in os.walk(src) for f in files
                for h in scanner.scan(os.path.join(root, f)) if h[0] == "HIGH"]
        if high:  # always scanned, also on update and --force
            print(f"  {n}: scanner HIGH findings, not installed: {high[:3]}"); continue
        shutil.rmtree(dst, ignore_errors=True); shutil.copytree(src, dst)
        m[n] = tree_hash(dst)
        print(f"  {n}: installed")
    write_manifest(repo, m)
    print("  " + git_exclude(repo))
    print("  New skills load from the next session started in this repo.")


def status(repo, quiet=False):
    m = read_manifest(repo); rows = {}
    for n, h in sorted(m.items()):
        dst = os.path.join(skills_dir(repo), n)
        if not os.path.isdir(dst):
            rows[n] = "missing"; continue
        cur, lib = tree_hash(dst), tree_hash(os.path.join(LIB, n)) if n in lib_skills() else None
        rows[n] = ("edited locally" if cur != h else "library newer" if lib and lib != h else
                   "removed from library" if lib is None else "ok")
    if not quiet:
        print(f"{repo}:" if m else f"{repo}: no eng-* skills installed")
        for n, s in rows.items():
            print(f"  {n:13} {s}")
    return rows


def update(repo, force=False):
    rows = status(repo, quiet=True)
    todo = [n for n, s in rows.items() if s == "library newer" or (force and s in ("edited locally", "missing"))]
    skipped = [n for n, s in rows.items() if s == "edited locally" and not force]
    if todo:
        install(repo, todo, overwrite=True)
    print(f"updated: {', '.join(todo) or 'none'}" + (f"; kept local edits: {', '.join(skipped)}" if skipped else ""))


def remove(repo, names):
    m = read_manifest(repo)
    for n in names:
        if n not in m:
            print(f"  {n}: not installed by this tool; left alone"); continue
        shutil.rmtree(os.path.join(skills_dir(repo), n), ignore_errors=True); m.pop(n)
        print(f"  {n}: removed")
    write_manifest(repo, m)


def tokens(repo=None):
    def skill_rows(d):
        rows = []
        if os.path.isdir(d):
            for n in sorted(os.listdir(d)):
                if os.path.isfile(os.path.join(d, n, "SKILL.md")):
                    rows.append((n, desc_tokens(os.path.join(d, n))))
        return rows

    def size(p):
        return os.path.getsize(p) // 4 if os.path.isfile(p) else 0

    u = skill_rows(USER_SKILLS)
    print(f"User-level skill descriptions ({len(u)} skills): ~{sum(t for _, t in u)} tokens")
    for n, t in u:
        print(f"    {n:26} ~{t}")
    total = sum(t for _, t in u)
    cm = os.path.join(HOME, ".claude", "CLAUDE.md"); total += size(cm)
    print(f"~/.claude/CLAUDE.md: ~{size(cm)} tokens")
    target = os.path.abspath(repo or HOME)
    if repo:
        p = skill_rows(skills_dir(target))
        print(f"Project skill descriptions in {target} ({len(p)}): ~{sum(t for _, t in p)} tokens")
        for n, t in p:
            print(f"    {n:26} ~{t}")
        total += sum(t for _, t in p)
        for f in ("CLAUDE.md", os.path.join(".claude", "CLAUDE.md")):
            if size(os.path.join(target, f)):
                print(f"{f} in project: ~{size(os.path.join(target, f))} tokens"); total += size(os.path.join(target, f))
    mem = os.path.join(HOME, ".claude", "projects", target.replace("/", "-"), "memory", "MEMORY.md")
    print(f"MEMORY.md for {target}: ~{size(mem)} tokens" + ("" if os.path.isfile(mem) else " (none yet)"))
    total += size(mem)
    print(f"Total from your files, every session here: ~{total} tokens (chars/4; Claude Code's own prompt, tools "
          f"and built-in/plugin skills come on top; /context shows the real figure)")


def main(a):
    if not a or a[0] in ("-h", "--help", "help"):
        print(__doc__); return
    cmd, rest = a[0], a[1:]
    force = "--force" in rest; rest = [r for r in rest if r != "--force"]
    repo = os.path.abspath(os.path.expanduser(rest[0])) if rest else None
    if cmd == "list":
        for s in lib_skills():
            print(f"{s:13} ~{desc_tokens(os.path.join(LIB, s)):3} tok  {frontmatter(os.path.join(LIB, s, 'SKILL.md'))[1][:110]}")
    elif cmd == "tokens":
        tokens(repo)
    elif not repo or not os.path.isdir(repo):
        die(f"{cmd}: give an existing repo folder")
    elif cmd == "suggest":
        suggest(repo)
    elif cmd == "install":
        install(repo, rest[1:], overwrite=force) if rest[1:] else die("install: name at least one skill")
    elif cmd == "status":
        status(repo)
    elif cmd == "update":
        update(repo, force)
    elif cmd == "remove":
        remove(repo, rest[1:])
    else:
        die(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
