# The boote mentor brain — methodology for critiquing and building ideas

A synthesis of the YC method (Startup School + office hours), Techstars (the Mentor Manifesto), and idea-evaluation frameworks (the Mom Test, JTBD, RAT, Lean Canvas, Sequoia, Disciplined Entrepreneurship). This file is the brain of `boote-critic` and the guide for all of boote.

> **Provenance:** YC Startup School + office hours (Kevin Hale, Michael Seibel, Eric Migicovsky, Dalton Caldwell), Paul Graham's essays, the Techstars Mentor Manifesto (David Cohen), Steve Blank's Customer Development, Eric Ries' Lean Startup, Rob Fitzpatrick's *The Mom Test*, Bill Aulet's *Disciplined Entrepreneurship*, and Sequoia's business-plan template.

---

## 1. How an experienced mentor actually works (the operating model)

A 10-year YC/Techstars mentor is **not a verdict machine**. The core move:

> Figure out **which rung of the validation ladder** the founder is really standing on, then push them to the next piece of *evidence* — and send them **backward** the moment a downstream claim (solution, model, growth) is resting on an unproven upstream one (a real customer with an acute problem).

The idea is a hypothesis to be de-risked, not a plan to be graded. Most of the value is in **naming the one riskiest assumption and the cheapest way to test it**, and in refusing to let the founder skip ahead.

**Stance — the Techstars Mentor Manifesto (the *how* of good mentoring):**
- **Be Socratic** — ask the question that makes the founder see it, don't lecture.
- **Be direct; tell the truth, however hard** — but **challenging, never destructive**.
- **Clearly separate opinion from fact** — and **know what you don't know** ("I don't know" is a valid answer).
- **Give specific, actionable advice** — never "do more research"; say *which* research, *why*, and *what result would change the call*.
- **Guide, don't control — the decision belongs to the founder.** You provide angles and pressure; they choose.
- **#GiveFirst** — the goal is to build the real idea and to kill a bad one early so nobody's time and money is wasted.

**What every session produces:** (a) the single most important thing right now, (b) the riskiest assumption + its cheapest test, (c) the next concrete step — which for a raw idea is almost always *"go talk to users,"* not *"build."*

## 2. An idea is a hypothesis (Kevin Hale, YC)

Every idea has three parts:
- **Problem** — a real problem. Strong if it is **P**opular (1M+ people), **G**rowing (~20%+/yr), **U**rgent, **E**xpensive, **M**andatory (legal), or **F**requent.
- **Solution** — **do not start here.** The solution earns its place only after the problem and customer are understood.
- **Insight / unfair advantage** — at least one of five: **Founder** (1-in-10,000 expertise), **Market** (natural 20%+ growth), **Product** (10× better/cheaper), **Acquisition** (CAC near zero), **Monopoly** (network effect).

The critic decomposes the idea into these three. If a part is missing or technology-first (SISP), flag it.

## 3. The validation ladder (the spine of every critique)

A mentor places the idea on a **rung** and gates progress on evidence. **You may not bank a higher rung while a lower one is unproven.** (Synthesis of Blank's Customer Development, Aulet's six themes, Lean, and YC.)

| # | Rung | The question | Evidence that passes the gate | If it fails → |
|---|---|---|---|---|
| 1 | **Customer & problem** | Who *exactly*? Name one beachhead persona (Aulet). Is the pain acute & frequent? | ≥5 Mom-Test conversations about **past behavior**; an observed **workaround** ("hair on fire") | back to customer discovery (rung 1) |
| 2 | **Why now** | What changed recently that makes this possible/urgent? | a concrete catalyst (a new tech/API/LLM leap, regulation, behavior shift) | sharpen, or park as "too early" |
| 3 | **Value / JTBD** | What "job" is hired? Does the value beat the status quo? | the four forces favor switching (push+pull > anxiety+habit) | back to rung 1 (wrong problem) |
| 4 | **Solution & RAT** | What's the riskiest assumption, and the *cheapest* test of it? | a smoke-/fake-door/Wizard-of-Oz/concierge result — **not** a full build | redesign the test; don't build more |
| 5 | **Business model** | Bottom-up unit economics; default alive or dead? | a unit that works on realistic (not aspirational) inputs → `boote-economist` | back to rung 3/4, or kill |
| 6 | **Go-to-market** | Where do the first 10 customers come from? CAC vs LTV? | one repeatable channel with a real signal | back to rung 1 (wrong segment?) |
| 7 | **Metrics / PMF** | Real traction? | ~5–7%/week growth, cohort **retention**, ~40% "very disappointed" (Sean Ellis) | iterate — **this is the graduate gate** |

> **boote is phase-1.** It lives mostly on **rungs 1–5**; rungs 6–7 are where an idea hands off (`graduate`). The dossier always records the idea's current rung (`validation_stage`) and `evidence_level`; the critique restates them and gates on them.

## 4. The iteration loops — where a mentor sends the founder *backward*

The most valuable mentor reflex is the **redirect**. Watch for these and send the founder back:

| Symptom | Send back to |
|---|---|
| Talking about the solution/features before any customer evidence | rung 1 — "stop; tell me about the last time *they* hit this problem" |
| "We have no competitors" | rung 1/3 — what janky workaround do they use *today*? |
| Building/economics on a fluid, unlocked idea | lock the configuration to one sentence first (a `_learnings` lesson) |
| Vanity metrics (cumulative downloads/signups) | rung 7 — show **active usage + retention** |
| Chasing a market with no founder-market fit | name the unfair advantage, or treat "unknown industry" as the riskiest assumption |

**Pivot vs persevere (Ries).** When validated learning **refutes** the rung-1/3 hypothesis, **pivot** — change *one* block of the Lean Canvas (usually segment or problem) and keep the rest; a pivot is a change of hypothesis, **not** a failure. When learning **confirms** it, **persevere** and iterate. `kill` is for ideas that fail the same gate repeatedly with no viable pivot left, or hit a host red line.

## 5. Evidence is the currency — talking to users (The Mom Test)

The default failure mode (Michael Seibel): **building before talking to users.** A mentor relentlessly converts opinions into observed behavior.

Three rules: (1) talk about **their life**, not your idea; (2) ask about **specific past events**, not opinions about the future; (3) **talk less, listen more.** ("The Mom Test" = questions even your mom can't lie about, because you never mention the idea.)

Five questions: "What's the hardest part of doing X?" / "Tell me about the **last time** you had this problem." / "Why was it hard?" / "What have you **done** to solve it?" (nothing done = not acute) / "What don't you like about the solutions you've tried?"

Good data = **commitment & advancement** — the user gives **time** (a next meeting), **reputation** (an intro), or **money** (a pre-order/LOI). Praise and raw feature requests = bad data.

boote ships a dedicated sibling skill — **`boote:discovery`** — that generates the Mom Test-disciplined interview kit from an idea's dossier, logs each conversation as a structured evidence file, and keeps `evidence_level` honest.

> **The evidence gate.** With **no real user evidence**, the idea is on **rung 1 by definition**. The critique may not return `continue` with high confidence and the rubric **Problem** score is capped; the default next step is "talk to ~10 users (Mom Test)" before anything else.
>
> **Limitation:** the Mom Test is weak for a genuinely new or entertainment category where users have no "known problem" (the Steve Jobs critique). There, lean on a fake-door/RAT and a demand signal instead.

## 6. Validate before building — RAT and Lean

- **RAT (Riskiest Assumption Test):** instead of building an MVP, test the single assumption that could kill the business with the **cheapest** experiment (a build-measure-learn loop run learn-first). Experiments: **smoke-test / fake-door** (a landing page), **Wizard-of-Oz** (a manual back end), **concierge**, **piecemeal** (gluing existing tools together).
- **Lean Canvas (9 blocks):** Problem, Customer Segments, UVP, Solution, Channels, Revenue, Cost, Key Metrics, Unfair Advantage. Rank blocks by risk and test from the riskiest (usually Problem/Segment).
- **JTBD:** the customer "hires" the product to make progress in a situation. The **Four Forces**: the Push of the problem + the Pull of the new solution must overcome the Anxiety of adopting + the Habit of the status quo.

## 7. Make "make something people want" quantitative

- The measure: one KPI, a **5–7% weekly growth** target; the ultimate proof is **cohort retention** (a curve that flattens above zero), not cumulative totals.
- Only two things are real work: **"write code and talk to users."** PR, networking, endless decks/mockups = **fake work**.
- The 90/10 MVP: 90% of the value with 10% of the engineering. If you aren't embarrassed by your MVP, you launched too late.
- **Default alive or default dead?** (PG) On constant expenses and current growth, do you reach profitability on the cash you have? Ask **too early** rather than too late; the "fatal pinch" is default-dead + slow growth + little runway.

## 8. The traps (the most important part of a critique)

- **Tarpit idea:** looks simple and attractive on paper ("why hasn't anyone solved this?") but underneath has impossible unit economics or huge adoption friction. Classics: restaurant-discovery app, bill-splitting, generic habit-tracker; **consumer ideas are the most tarpit** (Caldwell/Seibel). **AI-era:** a thin LLM-aggregator chatbot, a generic code-review agent, an old tarpit relabeled "powered by AI."
- **SISP (Solution in Search of a Problem):** picking up the technology (blockchain/AI) first, then hunting for a problem.
- **Building in a vacuum:** no user conversations — only the founder's assumption.
- **Cold-start:** needs a large network effect from day one without solving the single-player problem first.
- **No founder-market fit:** chasing a lucrative industry with no domain expertise ("you don't know what you don't know").

## 9. YC's sharpest questions (the critic's weapon)

- **Unique insight:** "What do you understand about this business that others don't?"
- **Desperation:** "Because this doesn't exist, what janky workaround do people use right now?" (No manual workaround → not hair-on-fire.)
- **Organic:** "Is this your own problem?" (Building for a population you don't know = red flag.)
- **Intellectual honesty:** "Who are your competitors, and which do you fear most?" ("We have none" = ignorance of the market.)
- **Schlep:** "Are you running from the hard, tedious work (regulation, messy integration)?"
- **Why now:** "What fresh catalyst makes this possible now and not two years ago?"
- **Why you / the numbers:** drill the unit economics; an invented number → flag. The right answer is "I don't know, but here's how I'd find out."
- **The two-sentence test:** if you can't explain it in two sentences + one concrete example such that a smart friend gets it with no follow-up, the idea (or its articulation) is broken. Aim for **80% accurate, 100% clear** (Seibel).
- **Vanity metrics:** reject cumulative metrics; ask for active usage (DAU/WAU) and retention.

## 10. The pitch narrative — Sequoia (the required structure)

Company Purpose → Problem → Solution → **Why Now** → Market Size → Competition → Product → Business Model → Team → Financials → (the ask). Logic: hook (one-liner + acute pain) → reveal & urgency (solution + why-now) → proof → team/vision. Market is **bottom-up** (a specific customer count × a real price; TAM top-down only as a sanity check), never "1% of a $10T market." The initial TAM is almost always wrong — weight the **growth rate** over the initial size.

## 11. Managing conflicting feedback (the Techstars whiplash)

Many mentors → conflicting advice ("talk to 5 mentors, get 7 opinions"). How to manage it:
1. Look for a **pattern**, not a single loud opinion.
2. Weight feedback by the mentor's **real track record in that specific domain**, not by volume or confidence.
3. Treat each piece as a **data point** to evaluate against your own context — and use weighted decision scoring to break emotional paralysis.
4. Reconcile "big vision" vs "narrow focus" by treating focus as the **first step** on the path to the vision.
5. **The founder is the steward** — they take what fits and own the call.

> **Application in boote:** board/individual feedback produces exactly this whiplash. In `feedback`, separate the patterns, weight by source credibility, and record recurring objections in `_learnings.md` so future ideas cover them up front.

## 12. The office-hours cadence (boote is a loop, not a line)

Every recurring touch (`status`, `office-hours`, `feedback`, the top of each round) re-anchors on the same four questions — the YC office-hours rhythm:
1. What's the **one most important thing** right now?
2. What did you **learn from users** since last time — what did they *do* (not say)?
3. What's the **current riskiest assumption**, and how are you testing it **this week**?
4. Are you **default alive**?

This keeps the idea circling its riskiest assumption instead of drifting into fake work, and it is what turns boote's stages into an iterative loop rather than a one-shot pipeline.

## 13. Today's realities (the tensions — be honest)

- **The AI era:** building has become so fast and cheap that "validate-before-build" can sometimes be inverted — occasionally you build fast and iterate. Not an excuse for aimless building.
- **Red-ocean B2B:** in crowded enterprise SaaS a scrappy MVP isn't enough; buyers want a heavy baseline (security, auth, SSO) before they'll even test.
- **The Airbnb exception:** some winners had no clear insight or advantage on day one and won on grit + traction. So the ladder and rubric are **thinking tools, not a final verdict** — name the exception explicitly when you invoke it.
