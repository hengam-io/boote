# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.2.1] - 2026-09-10

### Fixed

- **`discovery` and `gemini-research-paid` were loading with no metadata at
  all.** Both wrote `description:` as an unquoted YAML scalar containing
  `": "` -- inside a plain scalar YAML reads that as a nested mapping and
  rejects the whole block. The loader's answer to unparseable frontmatter is
  not to complain but to drop **every** field, so both skills shipped with no
  name, no description and no triggers: they never fired on their own, and
  nothing on disk looked wrong. Both descriptions are now single-quoted,
  byte-for-byte the same text.

### Added

- **A release gate in CI, and tagging that is no longer a thing to remember.**
  `claude plugin validate --strict` reads only the marketplace manifest and
  passed both broken skills, so `claude plugin tag --dry-run` now runs on
  every pull request: it is the check that reads the repo the way Claude Code
  does, failing on frontmatter the loader cannot parse and on a `plugin.json`
  version that disagrees with the marketplace entry. A new `release.yml` cuts
  and pushes the `boote--v<version>` tag (and a GitHub release from this file)
  whenever a merge to `main` lands a version that has no tag yet.

## [2.2.0] — 2026-08-14

### Added

- **`/boote:discovery`** — a separate skill (`skills/discovery/`) that turns
  customer-discovery conversations into evidence the validation ladder accepts.
  Three modes, auto-detected from the ask:
  - **`kit`** (default) generates a ready-to-run, Mom Test-disciplined
    interview kit from the idea's dossier: screener, 60-second opening +
    consent, a JTBD-style timeline reconstruction of the last real episode,
    non-leading probes mapped to each pain hypothesis — each carrying a
    "signal we listen for" and a "what would disprove it" line — workaround
    and cost digging, a commitment ladder (time / reputation / money), a
    snowball close, and a post-interview debrief form. Written in the language
    the interviews actually run in; learning goals (max 3) confirmed with the
    owner first.
  - **`debrief`** logs a completed interview as a structured evidence file
    (facts / verbatim quotes / pain signals / commitment given / interpretation
    kept strictly separate) and updates the dossier's `evidence_level`
    honestly — `interviews:N` counts only conversations that surfaced specific
    past behavior; `commitments` only once real time/reputation/money
    accumulated. Never bumps the dossier version (that stays `refine`'s job).
  - **`synth`** finds patterns across three or more logged interviews (pain
    repetition, hypothesis verdicts, persona heat, the four forces,
    commitments collected) and proposes — never applies — the consequences
    for `refine`/`critique`.
  Ships a sourced methodology reference
  (`references/interview-methodology.md`: The Mom Test, YC's "How to Talk to
  Users", Steve Blank's customer discovery, Cindy Alvarez's Lean Customer
  Development, Michele Hansen's Deploy Empathy, JTBD switch/timeline
  interviews, and interview-bias traps) plus the kit / evidence-file /
  synthesis skeletons (`references/kit-template.md`). Reuses
  `discover-context.sh` (workspace / output_style / voice); the context gate
  is noted, not enforced — the real precondition is a dossier with a persona
  and at least one pain hypothesis. Hard rules: never pitch the idea in a
  discovery interview, never count praise or hypotheticals as evidence,
  consent + anonymization by default, PII minimized per the host
  `output_style`.

### Changed

- **`boote` now routes to `/boote:discovery`** wherever the honest next step
  is talking to users: `clarify` and `critique` point at the kit generator
  instead of leaving "go talk to ~10 users" abstract, and the methodology's
  evidence section (§5) references the skill. README documents the new skill;
  plugin and marketplace manifests bumped to 2.2.0.

## [2.1.0] — 2026-06-09

### Added

- **`/boote:gemini-research-paid`** — a separate, standalone skill
  (`skills/gemini-research-paid/`) that exposes boote's **paid Gemini research
  engine** on its own, for researching **any** topic with no idea-incubation
  attached. It runs the same `scripts/deep-research.sh` →
  `scripts/research_engine.py` loop (plan → research → synthesize → cite) that
  `boote research` uses, but carries **no dossier, no validation ladder, and no
  host-context gate** — it never calls `discover-context.sh` or touches a boote
  idea folder, so you can invoke it in any project without pulling in the mentor
  pipeline. The name makes it explicit that this is **Gemini (paid, billed
  `GEMINI_API_KEY`)** — distinct from Anthropic's built-in `/deep-research`
  (which fans out Claude's own WebSearch); its **free** counterpart is
  `yar:gemini-research-free` (Gemini CLI). Scopes ambiguous questions first,
  queries the engine in English with PII stripped, runs in the background,
  writes a cited report to `research/<date>-<slug>.md` (overridable by a
  caller), and reports a TL;DR with sources. Shares the engine with boote (no
  duplicated code). The report is raw researched facts, not professional legal /
  medical / financial advice.
- **`/reply`** — a separate skill (`skills/reply/`) that drafts the email back
  to the person who brought you an idea, written like a YC/Techstars mentor:
  direct, specific, sourced, and human — no flattery, no fake warmth, no vague
  "maybe later." Two modes, auto-detected from the idea's verdict and confirmed
  with the owner: **`iterate`** (critique + the one concrete thing to go prove
  next, door open) and **`pass`** (a clean no with the specific reason and at
  most one objective re-open criterion). Every flaw/finding cites its **exact
  source** (the original URLs pulled from the idea's `research/`), strips all
  boote jargon, honors `voice` + redaction, and is written in the recipient's
  language. Produces a draft for the owner to send — it never sends. Reuses
  `discover-context.sh`; its precondition is a critiqued idea, not the context
  gate. Grounded in the Techstars Mentor Manifesto, Paul Graham's *How to
  Disagree*, and feedback research (HBR; the Center for Creative Leadership's
  SBI model) — no VC blogs or commercial content.
- **`/distill`** — a separate, manual-only skill (`skills/distill/`) that
  collapses an idea into a single self-contained brief written in the founder's
  own voice (`idea.md`), then permanently deletes the rest of that idea's folder
  (dossier, rounds, research, economics, presentations, feedback log).
  Destructive and irreversible by design: `disable-model-invocation` (never
  auto-invoked), it writes and shows the brief *before* deleting anything, and
  erases only after the owner confirms by typing the idea's slug. No backup —
  leaving no trace is the point. Reuses `discover-context.sh` for
  workspace/voice resolution and does not enforce the context gate.

### Changed

- **`boote research` now routes through the `boote:gemini-research-paid` skill**
  instead of shelling out to `scripts/deep-research.sh` directly — one canonical
  invocation path for the paid Gemini engine. The skill still runs the research
  in the background, writes into the idea's `research/` folder, and folds the
  findings into the dossier exactly as before.
- Git history squashed to a single public release commit; the version history
  lives in this changelog. Tags restart at `v2.1.0`, and the changelog link
  references were fixed (the previously referenced tags were never published).

### Removed

- Personal contact email from the plugin/marketplace manifests and the
  conduct/security policies — private reporting now goes through GitHub
  (security advisories / the repository's Security tab).

## [2.0.0] — 2026-06-03

A methodology and structure overhaul to make boote behave like a senior (10y+)
YC/Techstars mentor, and to require host context instead of silently running
without it. **Breaking:** default behavior changes — a project with no host
context is now `blocked` until `boote init` runs (or context-light is opted
into explicitly).

### Added

- **Validation ladder** — every idea is tracked on a 7-rung ladder
  (customer/problem → why-now → value → solution/RAT → business-model → GTM →
  PMF). The critique places the idea on a rung, gates progress on evidence, and
  names the rung to advance to — or, more often, the rung to send the founder
  **back** to (`methodology.md` §3–§4).
- **The evidence gate** — an idea with no real user conversations
  (`evidence_level: none`) is raw by definition: the rubric Problem score is
  capped and the verdict may not be a confident `continue`; the default next
  step is customer discovery (the Mom Test), not a higher score.
- **`boote init`** — interactive host-context setup that writes
  `boote.config.md` (strategy + hurdle, principles + red lines, optional
  risks/style/voice/research key).
- **`boote office-hours`** — a recurring re-anchor loop (the YC office-hours
  rhythm: the one most important thing · what users *did* · the riskiest
  assumption + this week's test · default alive?).
- **`references/dossier-template.md`** — the required dossier schema with
  `validation_stage` / `evidence_level` and the blocking fields a critique
  needs before a verdict.

### Changed

- **Context is now required, not optional.** `discover-context.sh` emits a
  `BOOTE_GATE resolved | context-light | blocked` signal; the skill refuses
  substantive work while `blocked`. Context-light is now an **explicit,
  announced opt-in** (`mode: context-light`), never a silent default.
- **`methodology.md`** rewritten around the mentor operating model, the ladder,
  the iteration/backward loops, pivot-vs-persevere, and the office-hours
  cadence — grounded in YC Startup School, the Techstars Mentor Manifesto, the
  Mom Test, RAT, Disciplined Entrepreneurship, and Sequoia.
- **`critique-rubric.md`** adds preconditions, the evidence gate, and a
  stage-aware verdict format.
- **`boote-critic`** now reports the current rung + evidence level and the rung
  to advance/return to; **`boote-economist`** refuses to model an unlocked or
  unvalidated idea (precision theater).
- **Version bumped to 2.0.0** in both `plugin.json` and `marketplace.json`.

## [1.0.0] — 2026-06-03

Initial public release.

### Added

- **`boote` skill** — orchestrates the phase-1 incubation lifecycle:
  `new` · `clarify` · `critique` · `research` · `refine` · `economics` ·
  `name` · `present` · `feedback` · `status` · `graduate` · `park`.
- **Three bundled subagents:**
  - `boote-critic` — harsh-but-fair YC/Techstars critique with a rubric score
    and a continue/pivot/kill verdict.
  - `boote-economist` — bottom-up financial model, Base/Bear/Bull scenarios,
    sensitivity tables, and an economic verdict against the host's hurdle rate.
  - `boote-namer` — five to seven candidate names with positioning, taglines,
    and a light collision check.
- **Context discovery** (`scripts/discover-context.sh`) — resolves eight
  host-context slots from an explicit `boote.config.md`, then auto-discovery,
  then a context-light fallback. boote ships zero company data.
- **Grounded deep-research engine** (`scripts/deep-research.sh` +
  `scripts/research_engine.py`) — a synchronous, web-grounded, cited research
  loop (plan → research → synthesize → write) over the Gemini
  `generateContent` API. No third-party Python dependencies.
- **Reference knowledge base** (`skills/boote/references/`) — mentor
  methodology, critique rubric, economics methodology, financial-model
  template, intake questions, one-page memo template, and a self-contained
  interactive HTML deck template.
- **`boote.config.example.md`** — documented template for the host-context map.

[Unreleased]: https://github.com/hengam-io/boote/compare/v2.2.0...HEAD
[2.2.0]: https://github.com/hengam-io/boote/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/hengam-io/boote/releases/tag/v2.1.0
