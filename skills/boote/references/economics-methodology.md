# The boote financial-modeling brain — methodology for the "numbers" stage

> This file is the brain of `boote-economist` and the guide for the `economics` sub-command. It complements [`methodology.md`](methodology.md) (the brain of the qualitative critique): there the question is "is this idea right?"; here it is "do the numbers add up, and is it worth the capital?"
>
> The goal of this stage is not to build an optimistic pro-forma. The goal is to **find the price of being wrong**: under which assumptions the idea works, under which it dies, and how far the edge is. The output is a decision tool, not a forecast.

## When this stage comes
After the idea has passed `critique` and at least one round of `refine`, and has been locked to a **specific configuration** (one vertical, one revenue model, one frame). Before that, modeling is fake-work — you can't put numbers on a fluid idea (a `_learnings.md` lesson: until the model is locked to one sentence, every number is wasted). Usually right **before `graduate`**: before the founder commits real capital or attention.

## The 10 modeling principles

**1. Unit first, scale later.** Define the economic unit (one member, one court-hour, one location, one transaction, one merchant). Build contribution margin, CAC, LTV, and payback at the unit level before any company-wide total. **If the unit doesn't work, scale only magnifies the loss.**

**2. Bottom-up, not top-down.** Revenue = real customer count × real price × realistic utilization/attach rate. Every driver is tied to a benchmark or flagged as an assumption. "1% of an $X-billion market" is banned.

**3. Always three scenarios.** Base (most likely — realistic, not aspirational), Bear (the downside — what the failure-mode research says actually happens), Bull (the upside). Each must be **internally consistent** (you can't staple Bull revenue onto Bear costs). **The decision is made on surviving the Bear case, not on winning the Bull.**

**4. The capital stack is part of the model.** For capital-heavy ideas: equity vs debt, interest rate, LTV, amortization, and DSCR (debt-service coverage ratio). Leverage magnifies both returns and ruin — the "utilization trap": +200bps of rate can push break-even back by months.

**5. Returns as an investor sees them.** Payback period, IRR, NPV (with an explicit hurdle/discount rate), and cash-on-cash/ROI. For an asset + operating business: split **OpCo/PropCo** and an exit multiple (operations at X× EBITDA, property via sale-leaseback at a cap rate). Always state the hurdle: what return covers the founder's/host's opportunity cost?

**6. Sensitivity is where the model lives or dies.** One or two two-way tables on the 2–3 highest-impact drivers. Find the break-even line and say how much cushion there is. A single-point model is useless.

**7. Find the riskiest number.** The quantitative mirror of the riskiest assumption: which single input, if 20% worse than assumed, breaks the deal? That is what the cheap pre-capital experiment must validate.

**8. Default alive or dead?** (YC) Does the Base scenario reach self-funding before the capital runs out? Model runway/burn and working capital explicitly. Revenue ≠ cash.

**9. Honesty about precision.** Every number is either sourced (benchmark + date) or flagged (assumption + range). Separate "grounded" from "assumed." No false precision — if you're uncertain, give a range, not a single figure.

**10. An economic verdict, not an emotional one.** `economically-viable` / `marginal` / `not-viable-as-modeled`, with the conditions, the riskiest number, a comparison to the hurdle, and "what would turn this into a confident yes."

## Common financial traps (an explicit checklist)
- **Hollow pro-forma:** percentage-of-TAM, a hockey stick with no ramp logic.
- **Ignoring the ramp:** year 1 ≠ steady state.
- **Rent = zero under ownership:** either impute rent or carry debt service; use EBITDAR.
- **Confusing revenue with cash:** debt service + taxes + working capital.
- **Under-estimating capex:** low $/sqft, forgetting HVAC / pre-opening / working capital.
- **Survivorship bias:** the base failure rate belongs in the Bear case and in risk.
- **Downside via the asset:** a fairy tale without a liquidation discount + carrying cost.
- **Ignored leverage:** profit is rate-sensitive; ruin comes through debt service, not operations.

## How to use deep research
The model's inputs come from three places: (a) the idea's existing research, (b) a new, targeted research question for the model's **specific numeric gaps** (financing rate, local pricing, build cost, the ramp curve, margin benchmarks), (c) a point WebSearch for a single cell. Fire the research questions in parallel (in the background) with `deep-research.sh` before and while building the model (PII-clean, in English). Every model cell is labeled with its source. The recurring gap pattern: (1) capital stack + local financing, (2) pricing + ramp + local staffing, (3) industry margin / failure-rate benchmarks.

## A map for idea types (the unit changes, the principles don't)
- **Asset + operating (e.g. a racket club):** unit = location/court-hour; the capital stack is central; OpCo/PropCo; utilization is the main driver.
- **SaaS / agent:** unit = subscriber/seat; capex = engineering + inference cost; drivers are CAC/LTV/NRR/gross-margin; instead of a property IRR, use CAC payback and the rule of 40.
- **Marketplace:** unit = transaction; take-rate × GMV; cold-start and liquidity; contribution after two-sided CAC.

> In every case: unit → bottom-up revenue → opex → P&L → returns → scenarios → sensitivity → the riskiest number → verdict.
