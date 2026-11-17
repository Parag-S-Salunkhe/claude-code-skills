---
name: rca
description: >-
  Root cause analysis with evidence. Use when asked for an RCA or "why did this happen" on a server, device, service,
  CI job or deployment failure ("RCA", "root cause", "why did it fail", "why does it keep failing", "what caused",
  "customer wants an RCA"), or when a fix has already failed twice. Makes Claude prove a cause from logs, timestamps
  and a healthy comparison before naming it, label its confidence, and write the RCA in a fixed format.
---

# rca: evidence before cause

Iron rule: **no root cause without evidence, no fix without a root cause.** "Not proven yet, the next check is X" is a
valid answer. A guess presented as a cause is not.

## Steps

Copy and tick:
```
- [ ] 1 Exact symptom   - [ ] 2 Notes first   - [ ] 3 Timeline   - [ ] 4 Compare with healthy
- [ ] 5 One hypothesis  - [ ] 6 Confidence    - [ ] 7 Write it   - [ ] 8 Save
```

1. **Exact symptom.** Copy the exact error text, which system, and when (UTC plus the user's local time). Several
   errors on one system → put them on ONE timeline before treating them separately: two errors in the same window are
   often one failure seen by two layers.
2. **Notes first.** Search the team's runbooks and past RCAs for the exact error text. A known entry → follow it.
3. **Timeline from logs, read-only.** Only timestamps copied from a log line or a database field go in the timeline,
   never estimated ones. Sources: application logs, system or kernel logs, CI console, deploy history.
   Then **what changed just before**: deploys, config changes, reboots, scheduled jobs, upstream incidents.
4. **Compare with healthy.** The same kind of system that is working: a sibling server, the last green build, the
   same device model elsewhere. List every difference. **Scope tells the layer:** one item = the item itself; one
   group = what the group shares (switch, hub, power, node); everything in one window = a shared dependency.
5. **One hypothesis at a time.** Write "X, because evidence Y". Run the cheapest **read-only** check that would prove it
   wrong. Failed → a new hypothesis; never stack fixes. **Two fixes failed → stop** and tell the user what was checked.
6. **Confidence label** on every cause:
   - **Proven:** evidence, and the fix brought the system back to healthy.
   - **Likely:** evidence, but the fix isn't confirmed yet.
   - **Unknown:** say what was ruled out and what the next check is.
7. **Write it** in this format:
   ```
   System      : <what>                           Date : <DD-Mon-YYYY>
   Occurrences : <error 1 at time>, <error 2 at time> -> one window <start–end, timezone>
   Root cause  : <cause> (<evidence: log line / count / timestamp>)   [Proven | Likely | Unknown]
   Ruled out   : <e.g. no restart (uptime continuous); 5 siblings on the same switch were fine>
   Recovery    : <what fixed it, when, how long it took>
   Impact      : <what was unavailable, for how long, who was affected>
   Status now  : <healthy? how it was checked>
   Prevention  : <action + owner>
   ```
   Claude drafts it. A person sends it: never post an RCA to a customer, a ticket or chat yourself.
   No customer data, tokens or internal secrets in the text.
8. **Save** the new learning in the runbook (see the `save-learnings` skill). A wrong first guess → add it to your
   evals so it is tested next time.

## Known false causes

Keep a short list here of causes that sound right but have been disproved in your environment, each with the evidence
that would be needed to cite it again. Example: "a bad cable, when there is no error burst in the kernel log: prove it
with the log first".

## Credits

Ideas only, no text copied. These links are for people reading this file; Claude doesn't need to open them.

- [obra/superpowers: systematic-debugging](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging): the iron rule, one hypothesis at a time, stop after failed fixes (theirs at three, here at two).
