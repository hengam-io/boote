---
name: gemini-research-paid
description: PAID, web-grounded deep research on ANY topic via Google's **Gemini API** (`generateContent` + google_search; a billed GEMINI_API_KEY, can escalate to a Pro model for high-stakes work). Gemini-powered — distinct from Anthropic's built-in `/deep-research` (which fans out Claude's own WebSearch). Its FREE sibling is `yar:gemini-research-free` (Gemini CLI). Standalone and boote-free: no dossier, ladder, or host-context gate. Use it on its own for a researched, cited Markdown report, or let boote's `research` step / `ceo-deep-research` route to it for deep / high-stakes work (board, M&A, idea graduation). Invoke as `/boote:gemini-research-paid <question>`, or natural language "paid gemini research on …", "deep gemini research", Persian "تحقیق پولی/عمیق با جمینای". NOT for incubating or critiquing an idea (that is `boote`); the report is raw researched facts, not professional legal / medical / financial advice.
---

# gemini-research-paid — paid Gemini deep research

Run a **deep, multi-source, cited web investigation** on any topic via Google's **Gemini API** and hand back a sourced Markdown report. This is the **paid engine that lives in boote** (`scripts/deep-research.sh` → `scripts/research_engine.py`), exposed as its **own standalone skill** so you can research a topic on its own — **without** the incubator: no dossier, no validation ladder, no host-context gate.

> **It is Gemini, and it is paid.** The engine calls Google's Gemini `generateContent` with the `google_search` tool, billed against your `GEMINI_API_KEY` (and can escalate to a Pro model). This is **not** Anthropic's built-in `/deep-research` (that one fans out Claude's own WebSearch and needs no key).

> **Free vs paid vs the three doors.**
> - **Free sibling:** `yar:gemini-research-free` — same idea over the **Gemini CLI** (free tier). Reach for it for routine research.
> - **This skill (paid):** sharper/deeper, billed; reach for it for high-stakes or numeric work.
> - **Callers that route here:** `boote research "<q>"` (research *inside* an idea's workspace — folds findings into the dossier) and `ceo-deep-research` (Ali's smart router) both invoke this skill rather than the raw script. Same engine, one canonical door.

> **What the engine does** (one agentic pass over Gemini's grounded `generateContent`, Python std-lib only): **plan** the question into focused sub-questions → **research** each with a real web-search call (concurrent, retried) → **synthesize** a structured English report → **write** a `.md` with an `<!-- EXECUTIVE_SUMMARY -->` marker, the full report, and a deduped **Sources** list.

## The contract

1. **Scope it.** If the question is ambiguous (no region / time range / budget / criteria), ask **2–3 short clarifying questions** first, then proceed. If it is already clear, go straight ahead.
2. **Clean the query.** Send the engine **one English question with private / identifying details stripped** — it researches the public web. You can report back in the user's language.
3. **Pick depth from the ask.** `fast` (~4 sub-questions, ~1–3 min) is the default for a focused question or a quick fact-check; `deep` (~8 sub-questions, ~3–6 min) for a broad or high-stakes investigation. Escalate the model with `--model` (a Pro model) only for high-stakes or heavily numeric work. **A caller may pass an output path and depth** (e.g. boote's `research` step directs the report into an idea folder at `--depth deep`) — honor them.
4. **Run it in the background** so it survives across turns:
   ```
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/deep-research.sh" run \
     --query "<English question, PII removed>" \
     --out "research/$(date +%F)-<q-slug>.md" \
     --depth fast
   ```
   Use Bash `run_in_background: true`. For several questions, launch ≤ 2–3 in parallel, then collect. On completion the script prints one line to stdout — `STATUS_JSON: {...}` (`status: completed|failed`, `out`, `sources`, `sub_questions_ok`, …); all diagnostics go to stderr. Exit `0` = success, `1` = handled failure (missing key / total research failure).
5. **Finish the report.** When it completes, open the `--out` file, write a tight one-paragraph **executive summary into the `<!-- EXECUTIVE_SUMMARY -->` marker** at the top, and skim the **Sources**.
6. **Answer in chat.** Give a short **TL;DR + 3–5 key points (each with its source) + the path to the full report**. Be honest about confidence and gaps.

## Output

- Default path: **`research/<YYYY-MM-DD>-<slug>.md`** in the current project (the engine creates the folder if missing). Override the `--out` path on request (a caller routes it elsewhere). The report is a plain `.md` — never write secrets or personal data into it.

## Setup

Needs **`GEMINI_API_KEY`** in the environment (a billed key). The harness loads it from the project's `.claude/settings.local.json` **env block** (gitignored by Claude Code). If it is unset, the run exits with a clear error — tell the user to add it there (`{ "env": { "GEMINI_API_KEY": "…" } }`) and retry. Do **not** silently fall back to a different research engine; this skill is the paid Gemini-API one by design. (For a free run, that is the separate `yar:gemini-research-free` skill.)

## Guardrails

- **Cite everything.** Every important claim rides on a source. If a URL looks invented or suspicious, verify *that one* with WebFetch before relying on it — the engine must not fabricate sources.
- **Raw facts, not a verdict.** For legal / medical / financial / regulatory questions the report is **facts to gather**, not professional advice — route the interpretation to a qualified human and say so.
- **English in, any language out.** Query the engine in English with PII removed; summarize back in the user's language.
- **Stay standalone.** Don't invoke boote, `discover-context.sh`, a dossier, or the context gate — being boote-free is the entire point of this skill.

## Self-check before delivery
- [ ] Ambiguous scope → asked 2–3 clarifiers first; the query actually sent was English + PII-clean?
- [ ] Ran the bundled engine in the background; read the `STATUS_JSON` line and handled a `failed` status (missing key / total failure) honestly instead of inventing a report?
- [ ] Wrote the executive summary into the `<!-- EXECUTIVE_SUMMARY -->` marker; every key claim cites a real source; suspicious URLs verified with WebFetch?
- [ ] Chat answer = TL;DR + 3–5 sourced points + path to the report; confidence and gaps stated; no boote idea folder / dossier / context gate touched?

## Dependencies
- **Bundled paid engine (shared with boote, unchanged):** `scripts/deep-research.sh` (thin entry; checks `GEMINI_API_KEY`) → `scripts/research_engine.py` (plan → research → synthesize → write; no third-party Python dependencies). Full behavior is documented in the script headers.
- **Environment:** `GEMINI_API_KEY` (Google Generative Language API, billed). No boote host-context is required.
- **Free sibling:** `yar:gemini-research-free` (Gemini CLI). **Not** Anthropic's built-in `/deep-research`.
