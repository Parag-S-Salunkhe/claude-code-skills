---
name: eng-security
description: >-
  Security review of a code project's changes, config, dependencies and GitHub Actions: threat model first, trace
  untrusted input to dangerous sinks, false-positive check on every finding, report only confirmed issues with
  confidence. Use for "security review", "is this safe to ship", auth, forms, uploads, payments, AI features, new
  dependencies or workflows. Secrets storage and access, and "is this safe to install" for a skill, MCP or tool, go to secrets-guard.
---

# Security review

Report on the target (diff, files, feature); research the whole codebase before deciding.

## 1. Threat model (five minutes)

- Trust boundaries: where untrusted data enters — requests, forms, uploads, webhooks, URL params, third-party API
  responses, files, model output, and any text an AI agent reads (README, issues, web pages).
- Assets: credentials, personal data, payments, admin actions, CI tokens, the site itself (defacement).
- Per boundary, STRIDE: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of
  privilege. Write one abuse case per feature; it becomes a test.

## 2. Look

Per changed file, list: inputs, queries, auth and authorization checks, sessions, outbound calls, crypto, file paths,
shell or eval, HTML rendering, prompt construction. Then check these classes:

- Injection (SQL, shell, template, header), XSS, broken authorization / IDOR, CSRF, SSRF, path traversal, unsafe
  deserialization, check-then-act races.
- Secrets in code, client bundles, logs, error messages or git history.
- Unbounded work: missing rate limits, size caps, timeouts.
- Insecure defaults: debug mode on, permissive CORS, default credentials, missing security headers (CSP, HSTS,
  X-Content-Type-Options, frame-ancestors), cookies without HttpOnly / Secure / SameSite.
- AI features: model output reaching eval, SQL, shell or raw HTML; injected text able to drive tools.
- Static sites: keys in client JS, third-party scripts without a pinned version or SRI hash, forms posting to unknown
  endpoints, exposed `.git` or source maps.

## 3. Dependencies

New dependency: is it needed, maintained (recent release, not archived), the real package (not a look-alike name),
free of install scripts you did not expect? Exact versions, lockfile committed, run the package manager's audit
(`npm audit`, `pip-audit`) and read the advisories that apply, not just the count.

## 4. GitHub Actions (`.github/workflows/`)

- `pull_request_target` or `workflow_run` that checks out or runs PR code with secrets → critical.
- Attacker-controlled `${{ github.event.* }}` text (PR title, branch name, comment body) inside `run:` → injection.
  Safe in `if:`, `with:` and `env:`; the fix is passing it through an env var.
- Comment-triggered commands without an author-association check.
- `permissions:` missing or write-all; long-lived secrets where OIDC would do.
- Third-party actions not pinned to a full commit SHA in jobs that hold secrets or write access.
- Issue or PR text fed to an AI agent that has write tools.
- Needs write access to exploit (manual dispatch inputs, pushes to protected branches) → not a finding.

## 5. False-positive check (every candidate)

- Restate it: claim, root cause, trigger, impact, what the attacker can already do. Cannot restate it clearly → drop it
  or ask.
- Trace source to sink. Values from env, config or constants are server-controlled, not attacker-controlled.
  Framework protections (auto-escaping, parameterized ORM queries) hold unless bypassed (raw HTML, raw SQL).
- Argue against it once: which caller, middleware or validation would make it unexploitable? Look for it.
- Confidence: **High** = the attacker reaches the risky code and the input path is proven → report it with a severity.
  **Medium** = input source unclear → report as "needs verification". **Low** = theoretical → hardening ideas only.

## 6. Report

Per finding: `file:line` — severity — confidence — what an attacker does — evidence (the source-to-sink path) — fix.
Then the files reviewed, the checks that found nothing, and what could not be verified. Zero findings is a valid
result. Report only; changes to auth, CORS, permissions or secrets need the user's yes.

## Credits

Ideas only, no text copied. These links are for people reading this file; Claude doesn't need to open them.

- [getsentry/skills: security-review](https://github.com/getsentry/skills/tree/HEAD/skills/security-review) (Apache-2.0): research before flagging, confidence levels, attacker- vs server-controlled input.
- [getsentry/skills: gha-security-review](https://github.com/getsentry/skills/tree/HEAD/skills/gha-security-review) (Apache-2.0): GitHub Actions checks.
- [addyosmani/agent-skills: security-and-hardening](https://github.com/addyosmani/agent-skills/tree/HEAD/skills/security-and-hardening) (MIT): threat model first.
- [trailofbits/skills: fp-check](https://github.com/trailofbits/skills/tree/HEAD/plugins/fp-check/skills/fp-check) (CC-BY-SA-4.0): restate each finding and argue against it (general idea only).
- [trailofbits/skills: supply-chain-risk-auditor](https://github.com/trailofbits/skills/tree/HEAD/plugins/supply-chain-risk-auditor/skills/supply-chain-risk-auditor) (CC-BY-SA-4.0): dependency questions: maintained? look-alike name? install scripts? (general idea only).
