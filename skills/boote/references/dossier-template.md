# Dossier template — the single living source of an idea

`dossier.md` is the **only living source** of an idea. Rounds, research, economics, and presentations are append-only snapshots that **link** to it; they never copy it.

boote **requires** the fields below. A field that isn't known yet is written as `[unknown — blocking]` (it gates the verdict) or `[unknown — later]` (needed before a specific later stage, not now). The critique **may not return a confident `continue` while any `[unknown — blocking]` field is open**, and the rubric scores for those dimensions are capped (see [`critique-rubric.md`](critique-rubric.md)). Fill fields through `new` → `clarify` → `research`; bump the version on each `refine`.

> Why so strict: a mentor can't give a meaningful critique of "an app for restaurants." Without the beachhead customer, evidence of pain, why-now, and the riskiest assumption, all feedback degrades to generic platitudes. Forcing these fields is how boote stays a mentor and not a horoscope.

---

## Frontmatter (required)

```yaml
---
name:             # human title (set at `name`, else the working title)
slug:             # kebab-case folder name
version:          # v0.1, v0.2, … (bumped on each refine)
status:           # raw | clarifying | critiqued | refining | modeled | presented | graduated | parked
validation_stage: # 1-customer-problem | 2-why-now | 3-value | 4-solution-rat | 5-business-model | 6-gtm | 7-pmf
evidence_level:   # none | secondhand | interviews:N | commitments | usage-data
riskiest_assumption:   # one sentence — the thing that, if wrong, kills it
next_action:      # the single concrete next step (often "talk to N users")
verdict:          # continue | pivot | kill | (none yet)
confidence:       # X/10 (with the latest critique)
identity:         # set at `name`: chosen name + tagline
---
```

`validation_stage` and `evidence_level` are the spine of the methodology (see [`methodology.md`](methodology.md) §3, §5). Every critique restates them and gates on them; they never silently jump a rung without evidence.

## Body sections (required — mark unknowns explicitly)

1. **Thesis** — two sentences + one concrete example, 80% accurate / 100% clear (Seibel). If you can't state it this cleanly, that is itself the first flag.
2. **Beachhead customer** — *one* named persona (Aulet), not "everyone" / "SMBs" / "consumers". Demographic + the situation they're in.
3. **Problem & evidence** *(blocking)* — the pain: how acute, how frequent, what it costs them. The **workaround they use today**. The **user conversations**: how many, and what they *did* (not what they said they'd do). If none yet → `evidence_level: none` and this is `[unknown — blocking]`.
4. **Why now** — the recent catalyst (tech/API/LLM/regulation/behavior) that makes this feasible or urgent now and not two years ago.
5. **Founder-market fit / unfair advantage** — which of the five (Founder / Market / Product / Acquisition / Monopoly), and whether it's real leverage or just "we can do it too". Flag entering a wholly unfamiliar industry as a risk — but credit genuine existing domain expertise.
6. **Alternatives & competition** — who/what they use instead (including "do nothing"), **which competitor you fear most**, and **what you understand that they don't**. "We have no competitors" is a red flag, not an answer.
7. **Value proposition / JTBD** — the job the customer hires this for, and why the value beats the status quo (the four forces).
8. **Solution** — the simplest version that proves the value (not a feature list). Marked `[unknown — later]` until rungs 1–3 hold.
9. **Riskiest assumption + cheapest test (RAT)** *(blocking)* — the single assumption that, if wrong, collapses everything, and the cheapest pre-build experiment to test it.
10. **Business model & WTP** — how it makes money, the willingness-to-pay signal, and the bottom-up market (a customer count × a real price). `[unknown — later]` until rung 5.
11. **Host-context fit** — strategic/portfolio fit (`strategy`), any conflict with the host's principles/red lines (`principles`), risks touched (`risks`), and any ownership/transfer constraint (e.g. ROFR). Resolved from discovered host context — see [`context-discovery.md`](context-discovery.md). If host context is missing, this is itself a blocker (boote requires it; it does not invent the host's strategy or red lines).
12. **Open questions / next action** — the live list, and the single `next_action` echoed from the frontmatter.

---

A dossier at `validation_stage: 1` with `evidence_level: none` is a **raw idea**, not a weak one — the honest next step is customer discovery, and boote should say exactly that rather than scoring it as a failure.
