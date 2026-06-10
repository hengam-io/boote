# boote financial-model template

> `boote-economist` fills this template; the `economics` sub-command writes the output to `boote/<slug>/economics/<YYYY-MM-DD>-financial-model.md` (and, optionally, an `.xlsx` via `anthropic-skills:xlsx`). English, no emoji. Every number either has a source (benchmark + date) or an "assumption" label with a range. Fix the unit and currency at the top of the file. Delete the sections that don't apply to the idea type, but keep the structure.

```markdown
---
idea: <name / working title>
slug: <slug>
date: YYYY-MM-DD
configuration: "<exactly what is modeled — size, unit count, revenue model, location>"
currency: <CAD / USD — one, fixed>
horizon_modeled: <e.g. 5 years + terminal>
version: <vX.Y of the dossier this model was built on>
key_sources: [research/<...>.md, research/<...>.md]
economic_verdict: "<viable | marginal | not-viable-as-modeled> — one sentence"
---

# <name> — financial model (snapshot)

> A snapshot as of the date above. The living source of the idea is [`../dossier.md`](../dossier.md). This file records the numbers at a point in time; the assumptions go stale as the idea changes.

## 0. Configuration & assumptions register
One paragraph: exactly which configuration is modeled, and why this one (not the rejected options).

| Assumption | Value (Base) | Source / label | Bear | Bull |
|---|---|---|---|---|
| <e.g. building size> | <45,000 sqft> | <grounded: research X / assumption> | | |
| <purchase price per sqft> | | | | |
| <loan interest rate> | | | | |
| <ARPM / unit price> | | | | |
| <stabilized peak utilization> | | | | |
| ... | | | | |

> grounded = from a sourced benchmark. assumption = our estimate (with a range). Never leave the source column blank.

## 1. Capital required (capital stack)
| Item | Amount | Source / label |
|---|---|---|
| Land/building (or lease deposit) | | |
| Build-out / tenant improvement | | |
| Equipment | | |
| Pre-opening (marketing, hiring, permits) | | |
| Working capital / buffer | | |
| **Total capital** | | |

**Financing:** equity $X / debt $Y (LTV %), rate %, amortization, target DSCR, annual debt-service payment.

## 2. Revenue build (bottom-up, ramped)
Write the drivers explicitly (count × price × rate). Columns = years 1..5 (or the key ramp months).
| Revenue stream | Driver | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|---|---|---|---|---|---|---|
| <membership> | <members × ARPM × 12> | | | | | |
| <programming/academy> | | | | | | |
| <leagues/events> | | | | | | |
| <court rental> | | | | | | |
| <F&B/other> | | | | | | |
| **Total revenue** | | | | | | |

Explain the ramp logic in one line (e.g. peak utilization: 30% → 50% → 65% → 70%).

## 3. Operating costs
**Staffing:** a role × count × salary table (with sources). Total payroll.
| Role | Count | Salary each | Total |
|---|---|---|---|
| | | | |

**Other opex (annual, stabilized):** occupancy/debt service, utilities, maintenance, marketing, insurance/tax, other → total opex.

## 4. Pro-forma P&L (years 1–5)
| | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|---|---|---|---|---|---|
| Revenue | | | | | |
| COGS / direct | | | | | |
| Opex (ex-rent) | | | | | |
| **EBITDAR** | | | | | |
| (-) Rent / impute | | | | | |
| **EBITDA** | | | | | |
| (-) D&A | | | | | |
| (-) Interest | | | | | |
| (-) Tax | | | | | |
| **Net** | | | | | |

## 5. Unit economics
Per-unit contribution margin (per-member or per-court-hour): unit revenue − unit variable cost. CAC, LTV, LTV/CAC, CAC payback if relevant.

## 6. Break-even
- Utilization % for break-even (or member/transaction count).
- Months to break-even (cash).
- The distance from the current Base assumption to the break-even line (cushion).

## 7. Returns
| Metric | Base | Bear | Bull |
|---|---|---|---|
| Payback (years) | | | |
| IRR (horizon + terminal) | | | |
| NPV @ hurdle % | | | |
| Cash-on-cash (stabilized) | | | |

For asset + operating: split OpCo (X× EBITDA) and PropCo (sale-leaseback @ cap rate = X× EBITDAR), plus an exit scenario.
**Hurdle / opportunity cost:** what return is required for this to beat the host's alternative returns (opportunity cost / core business)?

## 8. Scenarios (summary)
| | Base | Bear | Bull |
|---|---|---|---|
| Key differing assumption | | | |
| Stabilized revenue | | | |
| EBITDA % | | | |
| IRR | | | |
| Payback | | | |
| Subjective probability | | | |

## 9. Sensitivity
One or two two-way tables on the main drivers. Mark the cells below break-even (label them "loss-making").
Example (IRR vs utilization × interest rate):
| util \ rate | 6% | 8% | 10% | 12% |
|---|---|---|---|---|
| 50% | | | | |
| 60% | | | | |
| 70% | | | | |

## 10. Riskiest number + cheapest test
The single input that, if 20% worse, breaks the deal + the cheapest pre-capital experiment to validate it.

## 11. Economic verdict
`economically-viable | marginal | not-viable-as-modeled` + the required conditions + a comparison to the hurdle + "what would turn this into a confident yes" + the 3 most uncertain numbers worth a follow-up research run (as research questions).
```
