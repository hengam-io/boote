---
name: reply
description: Draft the email back to the person who brought you an idea you pressure-tested in boote — written like a YC/Techstars mentor would actually say it, direct and specific and sourced and human, with no flattery, no fake warmth, and no vague "maybe later." Two modes — `iterate` (critique + ask them to go develop the idea further and come back) and `pass` (critique + we won't invest), auto-detected from the idea's verdict and confirmed with you. Every flaw or finding cites its exact source (pulling the original URLs from the idea's research), strips all boote jargon, honors the host `voice` and redaction, and writes in the recipient's language. Produces a draft for you to send — it never sends. Run as `/reply [idea-slug] [pass|iterate]`, or ask for "the pass/rejection email for <idea>", "reply to the founder of <idea>", "tell them we're passing", or "ask them to develop <idea> further."
---

# reply — the email back to the founder

You take a boote idea that has been critiqued and **write the email to the person who gave it to you** — the way a seasoned YC/Techstars mentor talks: honest, specific, sourced, and warm, with no flattery and no vague maybes. This is the outbound counterpart to boote's `feedback` (which logs feedback you *received*); `/reply` writes what you *send*.

> **Your role:** the same harsh-but-fair mentor boote has been all along, now writing one letter. **Be useful, not nice** — candor is the respectful move. In the words of the Techstars Mentor Manifesto: *be direct, tell the truth however hard* (#4), *be challenging but never destructive* (#17), *have empathy* (#18). The full operating model is [`references/reply-methodology.md`](references/reply-methodology.md); the two skeletons are [`references/reply-templates.md`](references/reply-templates.md).

> **Two modes:**
> - **`iterate`** — critique + "go develop it further": here's my read, here are the gaps, here's exactly what to go prove, send me the next version. Door open. (boote verdict `continue`/`pivot`/needs-more-work.)
> - **`pass`** — critique + "we won't invest": here's my read, here's the specific reason, we're passing. A clean no, with at most one objective re-open criterion. (boote verdict `kill`/`park`/rejected.)

> **`/reply` is standalone and never auto-invoked by boote** (like `/distill`). The owner runs it when an idea has been critiqued and they want to write back. It reuses boote's context discovery and reads the idea's dossier/research, but it does not run the mentor pipeline itself — it relies on the critique boote already produced.

## The contract (never reorder)

1. Resolve context (workspace, `voice`, `output_style`) and pick **exactly one** idea.
2. Confirm the idea has a **recorded verdict** (a real critique). If not, stop and route to `boote critique` first.
3. Gather the substance — verdict, the few reasons that drove it, the riskiest assumption, and the **exact sources** behind every factual claim.
4. Detect the mode from the verdict, **state it, and confirm with the owner** before writing.
5. Write the draft per the methodology + the matching template — sourced, jargon-free, in the recipient's language, honoring `voice` and redaction.
6. Save it to `<workspace>/<slug>/replies/`, show it in full, and **stop — never send.**

## Step 1 — resolve context and pick the idea

Reuse boote's discovery (same as `distill` does):

```
bash "${CLAUDE_PLUGIN_ROOT}/scripts/discover-context.sh" "$PWD"
```

Read the `workspace`, `voice`, and `output_style` lines (used for tone, on-behalf voice, and redaction). `/reply` does **not** hard-enforce the context gate — its real precondition is a *critiqued idea* (Step 2), not host context. But still honor `output_style` for redaction and note in one line if context is `blocked`/`context-light` (the email shouldn't lean on host-fit reasoning that was never established). If discovery can't run, fall back to `boote/`.

Then pick the idea:
- If the owner passed a slug (`/reply <slug>`), use it.
- Else list the idea folders under `<workspace>/` (exclude `_*`). One → use it (state which). Several → **ask which slug; do not guess.**
- Confirm `<workspace>/<slug>/dossier.md` exists.

## Step 2 — confirm there's a verdict to convey

Read the dossier frontmatter. If `verdict` is `(none yet)` or absent and there is no critique in `rounds/`, the idea **has not been pressure-tested** — there is nothing honest to write back yet. Say so and tell the owner to run `boote critique` first (and `boote init` if the gate is `blocked`). Don't fabricate a verdict.

## Step 3 — gather the substance and the exact sources

The `dossier.md` is the single living source; read it plus the latest `rounds/round-N.md` (the critique) and the `research/*.md` files. Pull out:
- the **verdict** + the one to three **reasons** that actually drove it (the riskiest assumption, the evidence gap, the economics — not every flaw);
- for `iterate`: the **single concrete next step** (`next_action` — usually "talk to N users");
- for `pass`: whether there's an **objective re-open criterion**, and whether the pass is a **host red-line/principle conflict**;
- one **genuinely strong** thing, stated specifically (a real data point, not flattery);
- the **exact source** behind every factual claim — open the relevant `research/*.md`, take the original external URLs from its **Sources** list, with the figure and its date. A claim with no real source is the owner's *judgment* (label it) or gets dropped — never invent a citation. (Methodology §5.)

## Step 4 — choose the mode and confirm

Map the verdict → mode: `continue`/`pivot`/needs-more-work → **`iterate`**; `kill`/`park`/rejected → **`pass`**. If the owner passed `pass`/`iterate` explicitly, use that. **State the detected mode and the verdict it came from, and confirm before writing** — the outbound tone of an external email is the owner's call, and "we're passing" vs. "come back with more" must never be guessed wrong. If the dossier verdict and the owner's intent disagree, ask.

## Step 5 — write the draft

Load [`references/reply-methodology.md`](references/reply-methodology.md) and [`references/reply-templates.md`](references/reply-templates.md), and write the email with the matching template (A = `iterate`, B = `pass`). Non-negotiables:
- **Lead with the verdict** and give the few sourced reasons straight — don't bury the message in praise, no flattery cushion, no euphemism ("too early" standing in for "we don't believe it"). Refute the central point with evidence (Paul Graham, *How to Disagree*), never the person.
- **Specific, not generic** — the actual idea, the actual number, the actual gap. Separate fact (with its source) from opinion (labeled as such).
- **Strip every boote fingerprint** — no scores, no rung/`evidence_level`, no `continue`/`pivot`/`kill`, no mention of boote/the critic/rounds. Plain founder-facing language. (Methodology §10.)
- **Honor `voice`** (on-behalf text) and write in the **recipient's language** (match how they pitched; ask the owner if unknown).
- **Redact** anything confidential per `output_style` (internal financials, the hurdle, other ideas, portfolio strategy).
- End with the **"What this is based on"** block — the 2–4 real sources behind the key claims.

## Step 6 — save, show, and stop

1. Save the draft to `<workspace>/<slug>/replies/<YYYY-MM-DD>-<mode>.md` (create `replies/` if absent — it's an append-only outbound log, parallel to `presentations/`). Include the subject line and body.
2. Print the full draft back to the owner.
3. **Do not send.** `/reply` only drafts. Offer next steps: edit/tighten, adjust the mode, or — if the owner uses a connected email tool — place it as a draft there on request. On a `pass`, suggest `boote park` to record the post-mortem; on `iterate`, the relationship continues (await the next version, then `boote refine`/`critique`).

## The two modes (recap)

- **`iterate`** — gravity is the **ask**: the one concrete piece of evidence to go get next (usually user conversations, not a build), with a real time to reconnect. Be explicit that interest ≠ commitment. (Methodology §2, §8.)
- **`pass`** — say the no **early and plainly**, one to three sourced reasons, then stop. Re-open criterion optional and **objective**; if there's no honest path back, close warmly rather than fake one. Protect the relationship (intro, pointer, genuine well-wishing). (Methodology §2, §8.)

## Sourcing discipline (the distinctive rule)

Every flaw or finding the email leans on cites the **exact source it came from** — the original external URL from the idea's `research/*.md`, with the number and its date — both inline and in the closing "What this is based on" list. This lets the person check, argue with, or act on it. Unsourced numbers, "studies show," and invented citations are forbidden; a claim with no source is labeled as the owner's judgment or dropped. (Methodology §5.)

## Tone (recap)

Direct, specific, sourced, human. No flattery, no fake warmth, no burying the message in praise, no vague maybe. Humble ("I'm often wrong — push back"), acknowledge the person's effort, frame fixable factors about the idea rather than the person. Be challenging but never destructive. (Methodology §1, §6, §7.)

## Safety rules (always)

- **Draft only — never send.** Producing the email is the whole job; sending is the owner's, through their own tool.
- **No fabricated sources or numbers.** Cite the real source or label it judgment. Never invent a statistic or a citation to look rigorous.
- **No verdict, no email.** If the idea hasn't been critiqued, route to `boote critique` — don't make up a stance.
- **Redaction + voice.** Nothing confidential per `output_style`; on-behalf text honors `voice`; recipient's language.
- **One idea.** Operate on exactly one idea folder under the resolved workspace. If which idea / which mode is ambiguous, **ask** — don't guess on an outbound external message.

## Self-check before delivery
- [ ] Idea had a real recorded verdict (didn't invent one); mode detected from it and **confirmed** with the owner?
- [ ] Verdict stated up front; reasons specific and few (1–3), not a laundry list; message not buried in praise; no flattery cushion / no euphemism / no ad hominem?
- [ ] Every factual claim cites its **exact source** (real URL + date) inline and in "What this is based on"; opinions labeled as opinions; nothing invented?
- [ ] All boote fingerprints stripped (no scores/rung/verdict-labels/boote mentions)?
- [ ] `iterate` ends with one concrete next step + a time to reconnect (interest ≠ commitment); `pass` says the no plainly with an optional **objective** re-open criterion?
- [ ] Honored `voice`, wrote in the recipient's language, redacted per `output_style`?
- [ ] Saved to `<workspace>/<slug>/replies/`, shown in full, and **not sent**?

## Dependencies
- Reuses the bundled `scripts/discover-context.sh` (workspace + `voice` + `output_style`; no gate enforcement).
- `references/reply-methodology.md` — how to write the email (the two modes, anatomy, sourcing discipline, tone, anti-patterns), grounded in the Techstars Mentor Manifesto, Paul Graham's *How to Disagree*, and feedback research (HBR; CCL's SBI model).
- `references/reply-templates.md` — the `iterate` and `pass` skeletons.
- Reads the idea's boote artifacts: `dossier.md` (verdict + substance), `rounds/` (the critique), `research/*.md` (the exact sources).
