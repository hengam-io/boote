---
name: discovery
description: 'Customer-discovery interviewing for boote ideas — turns an idea''s dossier into a ready-to-run, Mom Test-disciplined interview kit (screener, opening script, past-behavior timeline, pain probes mapped to each hypothesis, commitment tests, debrief form), logs completed interviews as structured evidence files, updates the dossier''s evidence_level, and synthesizes patterns across interviews. Grounded in The Mom Test, YC''s How to Talk to Users, Steve Blank, Lean Customer Development, Deploy Empathy, and JTBD switch interviews. Use at rungs 1-3 whenever the next step is talking to real users - "prep interview questions", "build my discovery questionnaire", "I talked to a user, log it", "synthesize my interviews", Persian "سؤال‌های مصاحبه رو آماده کن", "مصاحبه رو ثبت کن", "جمع‌بندی مصاحبه‌ها". Modes: kit (default) / debrief / synth. Not for critiquing the idea (boote) or web research (gemini-research-paid).'
---

# discovery — turning conversations into evidence

Evidence is boote's currency: an idea with no real user conversations sits on rung 1 by definition, and nothing advances it except what users **did** (methodology §5). This skill runs that loop — it prepares the interviews, logs them as structured evidence, and keeps the dossier's `evidence_level` honest. It exists so discovery conversations become **facts the validation ladder accepts**, not "people liked it."

> **Your role:** the founder's interview coach, not a survey generator. Every question you produce must survive the Mom Test — about the interviewee's life and past behavior, never a pitch, never a hypothetical. The methodology (with sources) is [`references/interview-methodology.md`](references/interview-methodology.md); the kit skeleton is [`references/kit-template.md`](references/kit-template.md). Load the methodology before generating or judging questions.

> **Three modes** (auto-detect from the ask; if ambiguous, ask):
> - **`kit`** (default) — an interview is coming → generate the interview kit from the dossier's hypotheses.
> - **`debrief`** — an interview happened → turn raw notes/transcript into a structured evidence file and update the dossier.
> - **`synth`** — several interviews logged → find patterns, test hypotheses, propose the next move.

## Step 0 — resolve context and pick the idea (every run)

1. Reuse boote's discovery:
   ```
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/discover-context.sh" "$PWD"
   ```
   Read `workspace`, `output_style`, `voice`. This skill does **not** hard-enforce the context gate (its precondition is a dossier, not strategy) — but if the gate is `blocked`, say so in one line; kits still generate.
2. Pick exactly one idea: explicit slug argument → use it; one idea folder under `<workspace>/` → use it and say which; several → ask.
3. **Precondition:** `<workspace>/<slug>/dossier.md` exists with at least a persona hypothesis (§2) and one pain hypothesis (§3). Missing → route to `boote new` / `boote clarify` first; a kit generated from nothing tests nothing.
4. Evidence files live in `<workspace>/<slug>/discovery/` by default. If the host declares a different discovery home (its CLAUDE.md / config) or the owner passes a path, honor it and say where files went.

## Mode `kit` — prepare the interview

1. Read the dossier: §2 persona (who we recruit), §3 pain hypotheses (what we test), plus any open rung-1 questions the host tracks. Read [`references/interview-methodology.md`](references/interview-methodology.md) and [`references/kit-template.md`](references/kit-template.md).
2. **Set the learning goals first** — the 3 biggest unknowns this batch of interviews must reduce (Mom Test: prepare your three big questions; YC: know what you need to learn). Confirm them with the owner in one short line each.
3. Ask (if not obvious): the **interview language** (the kit is written in the language the interviews will actually run in), the target interview count, and remote vs in-person.
4. Generate the kit per the template. Non-negotiables:
   - Every question is about **past behavior or their current life** ("walk me through the last time…", "what did you do about it?") — never "would you use/pay/like…".
   - The **idea is not mentioned or pitched**. If the interviewee asks, deflect briefly until the end (rule card in the template).
   - Each pain-hypothesis probe carries two lines: **"signal we listen for"** and **"what would disprove it"** — the interviewer must know why they're asking.
   - Include: screener, 60-second opening + consent, timeline core (JTBD-style reconstruction of the last relevant episode), probes per hypothesis, workaround-and-cost digging, commitment ladder (time / reputation / money), snowball close, and the post-interview debrief form.
   - Cap the core at what fits the slot (~8–12 main questions for 30 minutes); mark the rest as follow-ups.
5. Save to `<discovery-home>/YYYY-MM-DD-interview-kit-vN.md`. Present: the learning goals, the 5 most load-bearing questions, and the conduct card. Do not paste the whole kit into chat unless asked.

## Mode `debrief` — log one interview as evidence

1. Take whatever exists — raw notes, a transcript, or the owner's verbal retelling. Ask only for gaps that change evidence quality (who, when, how recruited, duration).
2. Write `<discovery-home>/YYYY-MM-DD-<who-slug>.md` with the fixed structure from the template's debrief section: context; **facts** (what they did, what it cost them); **direct quotes** (verbatim, separated); **pain signals** (severity / frequency / workaround cost); **commitment or advancement given** (time / reputation / money — or explicitly none); **our interpretation** (clearly separated — interpretation is not evidence).
3. Classify honestly: a conversation counts as an interview only if it surfaced **specific past behavior**. Opinions, praise, and feature requests get logged under interpretation, not facts.
4. Update the dossier frontmatter: `evidence_level: interviews:N` where N = the count of logged files that pass the bar; move to `commitments` only when real commitments (time / reputation / money) have accumulated. Fold findings that support or break a §3 hypothesis into the dossier with a link to the evidence file. **Never bump the dossier version** — that is `refine`'s job.
5. If the host keeps a discovery index (a README in the discovery home), append the one-line row.

## Mode `synth` — patterns across interviews

1. Read every evidence file in the discovery home. Refuse politely if fewer than 3 — patterns from 2 conversations are noise.
2. Report per the host `output_style`: which pain repeated in ≥3 interviews (with quotes), which hypothesis broke, which persona ran hottest, what the four forces (push / pull / anxiety / habit) look like from real answers, and any commitment signals.
3. Propose — do not apply — the consequences: a sharpened riskiest assumption, a persona lock, or a rung verdict ("rung 1 gate passed / still open"). The owner takes them into `boote refine` / `boote critique`.
4. Save the synthesis to `<discovery-home>/YYYY-MM-DD-synthesis.md`, linking every claim to its evidence file.

## Guardrails

- **Never pitch during discovery.** The interview is about their life. Showing the idea for reactions is a separate, later *solution interview* — if the owner wants one, label that section explicitly and keep it after the learning goals are covered.
- **Praise is not evidence; hypotheticals are not facts.** "Sounds great" and "I would definitely use this" go under interpretation. Facts are what they did, paid, and gave up.
- **Consent and dignity.** Record only with the interviewee's consent. Default to anonymized identities in files (role + initial) unless the owner explicitly keeps names.
- **PII minimization.** Incomes, addresses, and identifying details only if they change the evidence, only in the evidence file, never in shareable outputs — honor the host `output_style` redaction rules.
- **Don't inflate `evidence_level`.** The count reflects conversations that met the bar, not calendar meetings. When in doubt, count it lower and say why.
- **Language:** the kit and quotes stay in the interview language; structure and dossier updates follow the host's conventions.

## Self-check before delivery

- [ ] Kit: every question about past behavior / their life; zero pitch; each probe mapped to a hypothesis with a listen-for line and a disprove line; commitment ladder + debrief form included; learning goals confirmed?
- [ ] Debrief: facts / quotes / signals / commitment / interpretation kept separate; evidence bar applied honestly; `evidence_level` updated by real count; dossier version NOT bumped?
- [ ] Synth: ≥3 interviews; every pattern cites its evidence files; consequences proposed, not applied?
- [ ] Consent, anonymization, and PII rules honored; `output_style` respected in owner-facing output?
- [ ] Nothing here replaced critique or research — evidence gathered, judgment left to `boote critique`?

## Dependencies

- Reuses the bundled `scripts/discover-context.sh` (workspace + `output_style` + `voice`; gate not enforced).
- [`references/interview-methodology.md`](references/interview-methodology.md) — the sourced interviewing brain (Mom Test, YC, Blank, Alvarez, Hansen, JTBD, bias traps, counts, note discipline). **Read before generating or judging questions.**
- [`references/kit-template.md`](references/kit-template.md) — the kit / debrief / synthesis skeletons to fill.
- Reads and updates the idea's `dossier.md` (§2, §3, `evidence_level`); writes evidence under the idea's discovery home.
- Siblings: `boote` (routes here when the next step is "talk to users"), `boote:gemini-research-paid` (numbers research — never a substitute for interviews).
