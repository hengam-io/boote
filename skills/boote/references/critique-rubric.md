# Critique rubric — boote's critique checklist and scoring

The structured tool `boote-critic` applies. It is **a thinking tool, not a final verdict** (the Airbnb exception in methodology §13). Basis: the YC/Techstars method and the validation ladder in [`methodology.md`](methodology.md).

> No emoji. Every score must come with a short reason. A claim with no number = an assumption, not a score.

## Step 0 — preconditions (do this before scoring)

1. **Place the idea on the ladder.** State its `validation_stage` (rung 1–7) and `evidence_level` (none / secondhand / interviews:N / commitments / usage-data) from the dossier ([`methodology.md`](methodology.md) §3). The whole critique is read through these two.
2. **Check dossier completeness.** If any `[unknown — blocking]` field is open (beachhead customer, problem & evidence, riskiest assumption — see [`dossier-template.md`](dossier-template.md)), the idea is **not yet critiquable for a confident verdict**. Score what you can, but the verdict is capped (below) and the next action is to fill the blocking field, not to advance.

## The evidence gate (the most important gate)

- **`evidence_level: none`** (no real user conversations) → the idea is on **rung 1 by definition**. **Problem is capped at 10/25**, and the verdict may not be `continue` above **4/10 confidence**. The default next action is "talk to ~10 users (Mom Test), report what they *did*."
- **`secondhand`** (the founder's assumption, market reports, no direct talks) → Problem capped at 15/25.
- **`interviews:N`** with observed past behavior + workarounds → uncapped; weight by N and quality.
- **`commitments` / `usage-data`** (time, intros, pre-orders, retention) → the strongest evidence; let it lift Problem and the verdict.

Praise and feature requests are **not** evidence. "Lots of people would love this" with nobody having tried to solve it themselves = `none`.

## Scoring (100 points, 5 dimensions)

| Dimension | Points | What it measures |
|---|---|---|
| **Problem** | 25 | How real / acute / frequent? Does the user build a workaround today? Is it "hair on fire"? **Gated by the evidence gate above.** |
| **Insight / unfair advantage** | 20 | Which of the five (Founder / Market / Product / Acquisition / Monopoly)? Real, or just "we can do it too"? |
| **Why now** | 15 | A specific fresh catalyst? Or "it was always possible and nobody did it"? |
| **Market & model** | 20 | Bottom-up market with a number + source? A clear revenue model? Reasonable unit economics? |
| **Execution / founder-market fit** | 20 | Can the team/founder execute this? Leverage of existing expertise, or an unknown industry (the unfamiliar-industry risk)? Is the cheapest path to proof clear? |

**Interpreting the total score:**
- `< 40` — weak. Probably a tarpit/SISP. Default: kill, or a fundamental pivot.
- `40–59` — raw. A potential idea, but the fundamental assumptions are untested. Needs research + clarify + user evidence.
- `60–74` — serious. Worth building a presentation and taking to outside feedback.
- `75+` — strong. Ready to graduate (the host's deeper evaluation / a go decision).

> A high score with `evidence_level: none` is impossible by construction — it means the model is scoring its own assumptions. If you reach `60+` with no user evidence, you've made an error; recheck the evidence gate.

## The traps checklist (each "yes" = a red flag)
- [ ] **Tarpit?** Looks simple/attractive on paper, with a "why hasn't anyone done it"? Impossible unit economics or high adoption friction underneath?
- [ ] **SISP?** Started from the technology (AI) rather than from an acute problem?
- [ ] **Vacuum?** No real user conversation behind it?
- [ ] **Cold-start?** Needs a large network effect from day one?
- [ ] **Generic AI wrapper?** Just aggregates LLMs with no moat?
- [ ] **No founder-market fit?** A wholly unknown industry, chosen just because it "looks empty"?

## Mandatory questions that must have answers (from YC)
1. In two sentences + one example, what is this? (the clarity test)
2. Exactly **who** needs this? Name one specific beachhead persona.
3. Because this doesn't exist, what do they turn to right now? (desperation / the workaround)
4. Why now? (the catalyst)
5. What do you understand that competitors don't? + Which competitor do you fear most?
6. How does it make money? How big is the bottom-up market?
7. What is the biggest assumption that, if wrong, kills everything? (the riskiest assumption)

## The host-context layer (always check)
- **Strategic fit:** where does it sit in the host's strategy/portfolio? Does it match the host's investment framework (`strategy`)?
- **Principles + red lines:** any conflict with the host's principles/red lines (`principles`)? (e.g. a product red line = an immediate stop)
- **Existential risk:** which of the host risk-register items (`risks`) does it worsen or reduce?
- **Ownership/transfer constraint:** if the host has defined a constraint (e.g. a right of first refusal / ROFR on a sale, a structural partnership, or an equity transfer), does it apply? → flag.
- **`learnings`:** does this idea repeat a flaw that reviewers or the board have caught before?

> boote carries no built-in host rules. If the host context that this layer needs (`strategy` / `principles` / `risks`) was not provided, say so and treat it as a gap to fill via `boote init`, not something to invent.

## The verdict format
- **Stage & evidence:** current rung + evidence level, in one line.
- **Verdict:** `continue` / `pivot` / `kill` + confidence (X/10) + one sentence on why.
- **The gate to the next rung:** what evidence would advance it one rung — or, more often, **which rung to go back to** and why (e.g. "back to rung 1: you're describing the solution but have zero user conversations").
- **The single concrete next step** (e.g. "the riskiest assumption = will they pay $X/month; test it with a fake-door before anything else", or "talk to 10 [persona] about the last time they hit this").
