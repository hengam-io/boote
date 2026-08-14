# Interview kit template — the skeletons `discovery` fills

Three skeletons: the **kit** (mode `kit`), the **evidence file** (mode `debrief`), and the **synthesis** (mode `synth`). Fill them from the idea's dossier; write the kit in the language the interviews will actually run in. Angle-bracket fields are placeholders; guidance in *(italics)* is for the generator and is dropped from the produced file.

---

## 1) The interview kit

```markdown
# Interview kit — <idea name> · v<N> · <YYYY-MM-DD>

- Target persona (dossier §2): <one line — who qualifies>
- Pain hypotheses under test (dossier §3): H1 <one line> · H2 <one line> (· H3 …)
- Learning goals (max 3, confirmed with the owner): LG1 … · LG2 … · LG3 …
- Format: <30–45 min / remote or in-person> · Language: <interview language>
- Evidence bar reminder: we log what they DID, not what they say they'd do.

## 0. Conduct card (read before every interview)
1. Talk about their life, not your idea. The idea is never pitched.
2. Ask about specific past events; never about the future or hypotheticals.
3. Talk less, listen more; silence is a tool — count to three before rescuing.
4. Follow the emotion: when energy rises or drops, dig ("tell me more about that").
5. Facts and commitments are data; praise and feature requests are not.
6. If they ask what you're building: "I'll tell you everything at the end — first I want to learn how this works for you today."
7. One interviewer leads; if two attend, the second only takes notes.
8. Close every interview with an ask (see §7) — advancement separates polite interest from real pull.

## 1. Screener (recruiting filter — run before booking)
*(3–5 factual questions that verify the persona and the recency of the relevant episode; disqualify politely otherwise. Record, don't filter on, attributes the owner wants tracked as variables — e.g. tool habits.)*
- S1 <did the qualifying event happen, and when? — e.g. "bought/searched in the last N months">
- S2 <are they the actual decision-maker/doer of that episode?>
- S3 <variable to record, not filter: e.g. which tools/services they already use>
- Quota guidance: <mix to aim for across the batch>

## 2. Opening (first 60 seconds + consent)
"<Thanks + who I am in one clause>. I'm doing research on <the domain episode — NOT the product>. There's nothing to sell — I'm trying to learn how this actually went for you. Nothing you say can be wrong. May I take notes / record? <If recording: explicit yes required.>"

## 3. Timeline core — reconstruct the last real episode
*(The spine. JTBD-style: walk the specific past episode end to end. Anchor every answer in that one episode, not "usually".)*
- T1 "Take me back: when did you FIRST think about <episode>? What triggered it?"
- T2 "What did you do first? Then what?" *(loop "then what?" through the whole path)*
- T3 "At each step — what tool/person did you use? Why that one?"
- T4 "Where did it drag or stall? What did that cost you (time / money / stress)?"
- T5 "What almost made you give up or postpone?"
- T6 "How did you finally decide? Who else was involved in the decision?"
- T7 "After it was done — what surprised you? What would you never do again?"

## 4. Pain-hypothesis probes
*(For each dossier §3 hypothesis: 3–5 non-leading questions + the two calibration lines. Questions must not name the pain — they create room for it to surface, or not.)*

### H1 — <hypothesis in one line>
- Q… / Q… / Q…
- Signal we listen for: <the observable behavior/cost that would support H1>
- What would disprove it: <the answer pattern that kills H1 — take it seriously>

### H2 — <hypothesis in one line>
- …

## 5. Workaround and cost digging
- "What have you actually done about <the surfaced problem>?" *(nothing done → not hair-on-fire; log it)*
- "What does the current way cost you — hours, money, favors, stress?"
- "Have you paid for / built / duct-taped anything for this? Show me if you can."
- "What don't you like about what you use now?"

## 6. The idea-mention rule
Default: the idea is NOT mentioned. If all learning goals are covered and the owner explicitly wants reactions, a labeled **solution-reaction section** may run at the very end — clearly separated, and its answers are logged as opinions, never as pain evidence.

## 7. Commitment close + snowball
- Time: "Can I come back in <N weeks> when we have something to show, for 20 minutes?"
- Reputation: "Is there anyone else who just went through <episode> you'd introduce me to?" *(the snowball — also the recruiting engine)*
- Money (only when honest to ask): "If something removed <surfaced pain>, would you pay for it today? What did you last pay for anything in this area?"
- Log exactly what they GAVE, not how warm they sounded.

## 8. Post-interview debrief (fill within 30 minutes — memory decays fast)
→ produces the evidence file (skeleton below).
```

---

## 2) The evidence file (mode `debrief`)

```markdown
# <role/persona> — <YYYY-MM-DD>
- Context: <who (anonymized: role + initial), how recruited, format, duration, interviewer>
- Kit version used: <vN or "none — unstructured">

## Facts (what they DID and what it cost)
- …

## Direct quotes (verbatim, interview language)
- "…"

## Pain signals (per hypothesis)
- H1: <supported / weakened / silent> — <the observed behavior/cost>
- H2: …

## Commitment / advancement given
- <time / reputation / money — exactly what, or "none">

## Our interpretation (NOT evidence — kept separate on purpose)
- …

## Quality self-score
- Past-behavior anchored? <y/n> · Pitched the idea? <y/n — if yes, discount>
- Counts toward `evidence_level`? <yes/no + one-line reason>
```

---

## 3) The synthesis file (mode `synth`)

```markdown
# Discovery synthesis — <idea name> · <YYYY-MM-DD> · N=<count>

## Pattern table
| Pain / theme | Seen in | Strength (behavior vs talk) | Key quote |
|---|---|---|---|
| … | <files> | … | "…" |

## Hypothesis verdicts
- H1: <held / broke / unresolved> — <evidence files>
- H2: …

## Persona heat
<which segment showed the most acute, frequent, expensive pain — with evidence>

## Four forces (from real answers)
- Push: … · Pull: … · Anxiety: … · Habit: …

## Commitments collected
<sum of time / reputation / money given across interviews>

## Proposed consequences (for the owner — apply via refine/critique, not here)
- Riskiest assumption: <keep / replace with …>
- Persona: <lock / widen / pivot>
- Rung 1 gate: <passed — ≥5 behavior-anchored interviews with a repeated acute pain / still open because …>
```
