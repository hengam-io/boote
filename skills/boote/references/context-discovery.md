# Context discovery — how boote uses (and requires) the host project's context

> boote is **context-free** in the sense that it ships zero company data — but it is **not context-optional**. A mentor who knows nothing about your strategy, your red lines, and your opportunity cost can only give generic advice. So at the start of every run boote **resolves the host's own context, and requires the verdict-changing parts before it will critique, model, or present.** This file is the single source of truth for the context model; the `boote` skill and the `boote-critic` / `boote-economist` / `boote-namer` agents all resolve context the way described here.

## The eight context slots

| slot | what it feeds | typical host file | required to lift the gate? |
|---|---|---|---|
| `strategy` | where an idea fits in the portfolio/horizons + the **hurdle / opportunity cost** | a strategy doc | **yes** |
| `principles` | values + **red lines** an idea is checked against | a values/principles doc | **yes** |
| `risks` | the company risk register an idea may touch or worsen | a risk register | recommended |
| `learnings` | append-only cross-idea lessons (so the same mistake isn't repeated) | `<workspace>/_learnings.md` | no (created on first lesson) |
| `workspace` | where idea folders live (`<workspace>/<slug>/`) | `boote/` | no (default `boote/`) |
| `output_style` | house style for owner-facing outputs (reports, memos) | a reporting-style doc | no (default: clean, no emoji, one page) |
| `voice` | founder voice for text written **on the owner's behalf** | a voice/tone doc | no (default: neutral, professional) |
| `research_key` | Gemini key for bundled deep research | env `GEMINI_API_KEY` | no (research is skipped without it) |

A **hurdle rate** (the opportunity-cost return a go/no-go is measured against) is part of the `strategy` slot — set it in the config notes or the strategy doc. It is required for `economics`.

The mentor **methodology itself** (YC/Techstars critique, the validation ladder, RAT, the economics model, naming) is generic and ships in the plugin — it is NOT context. Only the company-specific framing above is discovered.

## The context gate (resolved / context-light / blocked)

`scripts/discover-context.sh <host-root>` resolves every slot and prints a manifest plus a machine-readable gate line:

- **`BOOTE_GATE resolved`** — the required slots (`strategy` incl. hurdle, and `principles`) are present (via config or auto-discovery). Proceed normally.
- **`BOOTE_GATE context-light`** — no required context, **but** the owner has explicitly opted in (a `mode: context-light` line in `boote.config.md`, or a `<workspace>/.context-light` marker). Proceed on pure YC/Techstars methodology, and **state in every run** that host-fit / red-line / hurdle checks are disabled.
- **`BOOTE_GATE blocked`** — no required context and no explicit opt-in. **This is the default for a fresh project, and boote does not do substantive work in this state.** The skill routes to `boote init` (below). Only `init`, `status`, and `help` run while blocked.

This is a **soft gate**: it lives in the skill, not in a hook. It steers the owner to set context up front instead of getting a generic critique by accident; a determined owner can still bypass it (e.g. by opting into context-light), and that's fine — the point is that running without host context is a **deliberate, announced choice**, never a silent default.

## Resolution order

For each slot, resolve in this order and stop at the first hit:

1. **Explicit config.** If `boote.config.md` (or `.boote/config.md`) exists in the host root, read its slot→path map and its `mode`/notes. Preferred and predictable. Schema below.
2. **Auto-discover.** For any slot the config didn't set, scan the host for conventional files:
   - `strategy` → `**/strategy*.md`, `**/current-strategy*`, a `## Strategy` section in `CLAUDE.md`
   - `principles` → `**/vision*.md`, `**/values*.md`, `**/principles*.md`
   - `risks` → `**/risk*register*`, `**/risks/*.md`
   - `workspace` → an existing `boote/` dir (else default `boote/`)
   - `learnings` → `<workspace>/_learnings.md`
   - `output_style` → `**/reporting*pref*`, `**/style-guide*`
   - `voice` → `**/voice*profile*`, `**/tone*`
   - `research_key` → env `GEMINI_API_KEY`
   Tell the owner what auto-discovery found and from where.
3. **Decide the gate.** If the required slots resolved → `resolved`. Else if an explicit context-light opt-in exists → `context-light`. Else → `blocked`.

## `boote init` — collecting context (what happens when blocked)

`boote init` is an interactive setup that lifts the gate. It:
1. Explains the eight slots and why the required ones change a verdict.
2. For each required slot, either points at an existing host file or **captures the answer inline** and writes it into `boote.config.md` (a few sentences of strategy/portfolio framing, the hurdle rate, and the principles / red lines are enough — the owner doesn't need pre-existing docs).
3. Offers the optional slots (`risks`, `output_style`, `voice`, `research_key`).
4. Writes `boote.config.md` at the host root (from `boote.config.example.md`), then re-runs discovery to confirm `BOOTE_GATE resolved`.
5. If the owner declines to provide context, offers the **explicit** context-light opt-in (writes `mode: context-light`) and states what will be disabled.

## `boote.config.md` schema

Drop this at the host repo root (copy `boote.config.example.md`). Plain `slot: path` (or value) lines inside a fenced block; `none` opts a slot out; paths are relative to the host root.

```
mode:         full            # full (default) | context-light
strategy:     path/to/strategy.md
principles:   path/to/values-or-principles.md
risks:        path/to/risk-register.md
learnings:    boote/_learnings.md
workspace:    boote/
output_style: path/to/reporting-style.md
voice:        path/to/voice-profile.md
research_key: env:GEMINI_API_KEY
```

Add free-form notes after the block — boote reads them as additional framing. The **hurdle rate** lives here if it isn't in the strategy doc, e.g.:

- Hurdle rate (opportunity cost for go/no-go): 15%
- Product red lines: no weapons, tobacco, alcohol, adult goods
- Ownership/transfer constraints to check on any sale or structural deal: <describe, or "none">

Setting `mode: context-light` is the explicit opt-in that turns a `blocked` project into `context-light`; it does not require any slot paths.

## How consumers use resolved context

- **skill `boote` (step 1)** runs discovery, reads the gate, and — if `blocked` — routes to `boote init` instead of doing substantive work. When `resolved` or `context-light`, it loads the resolved `strategy`/`principles`/`risks`/`learnings` and threads them into every sub-command. Owner-facing output obeys `output_style`; on-behalf text obeys `voice`.
- **`boote-critic`** loads `methodology.md` + `critique-rubric.md` + resolved `principles`/`strategy`/`risks` + `learnings`. It checks the idea against the host's principles/red-lines and flags conflicts — it carries no built-in company rules. In `context-light` it says the host-fit and red-line checks are disabled.
- **`boote-economist`** loads `economics-methodology.md` + `financial-model-template.md` + resolved context + the idea's research. The **hurdle rate** = the host's opportunity cost; take it from the config notes or `strategy`. In `context-light` it asks for the hurdle inline (it can't model returns against an unknown opportunity cost).
- **`boote-namer`** is context-free except for honoring `output_style` and any host brand/identity.
