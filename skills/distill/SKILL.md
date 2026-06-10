---
name: distill
description: Collapse one boote idea into a SINGLE self-contained brief written in the founder's own voice (saved as idea.md), then PERMANENTLY DELETE all of that idea's working history — the dossier, every round, all research, the economics, the presentations, and the feedback log — leaving only the brief. Use it when you want a clean, portable write-up of the latest version of an idea (even an imperfect one) to share for outside opinions or to re-seed into boote fresh, with no history or critique trail left behind. DESTRUCTIVE and IRREVERSIBLE — manual-only (never auto-invoked), it writes and shows the brief first and deletes only after you confirm by typing the idea's slug. Run as /distill [idea-slug].
disable-model-invocation: true
---

# distill — collapse an idea into one founder brief, then erase its history

> **DESTRUCTIVE & IRREVERSIBLE. MANUAL-ONLY.** This skill is never auto-invoked by the model and is never reached from a conversational "boote …" message — it runs only when the owner explicitly types `/distill`. It deliberately breaks boote's append-only, *history-is-never-deleted* principle: that is its whole purpose, so it lives in its own skill, fenced behind an explicit typed confirmation.

`distill` takes the **latest concluded version** of one boote idea, rewrites it **from the founder's own perspective** into a single self-contained brief (`idea.md`) the owner can share for outside opinions or re-seed into boote fresh — then **permanently deletes everything else in that idea's folder**: the `dossier.md`, every round, all research, the economics, the presentations, and the feedback log. No backup, no archive, no trace. Only `idea.md` survives.

## The contract (never reorder)

1. Resolve the workspace and pick **exactly one** idea.
2. Read its `dossier.md` (the single living source) and skim the latest round.
3. Write the founder-voice brief to `<workspace>/<slug>/idea.md`.
4. Show the full brief **and** the exact list of paths about to be deleted.
5. **Require the owner to confirm by typing the idea's slug.** Anything else aborts.
6. Delete every other file/folder under `<workspace>/<slug>/`, keeping only `idea.md`.
7. Report what remains.

The brief is always written and shown **before** anything is deleted, so an accidental run can be aborted with nothing lost.

## Step 1 — resolve the workspace and pick the idea

Resolve the workspace the same way boote does (reuse the bundled discovery):

```
bash "${CLAUDE_PLUGIN_ROOT}/scripts/discover-context.sh" "$PWD"
```

Read the `BOOTE_CTX workspace …` line for the workspace dir (default `boote/`), plus the `voice` and `output_style` lines (used for the brief's tone). `distill` does **not** enforce the context gate — it is a file utility, not substantive mentor work, so a `blocked` gate does not stop it. If discovery can't run, fall back to `boote/`.

Then pick the idea:
- If the owner passed a slug (`/distill <slug>`), use it.
- Else list the idea folders under `<workspace>/` (exclude `_*`). One → use it (state which). Several → **ask which slug; do not guess.**
- Confirm `<workspace>/<slug>/dossier.md` exists. If the folder holds only `idea.md` and no dossier, it is **already distilled** — say so and stop (only rewrite the brief from `idea.md` if explicitly asked).

## Step 2 — read the latest concluded idea

The `dossier.md` is the latest concluded state (it is bumped on every refine), so it is the **primary source**. Skim the most recent `rounds/round-N.md` only to catch any conclusion not yet folded into the dossier. Inline any key number you intend to keep **with its source + date** — the research files are about to be deleted and links would dangle.

## Step 3 — write the founder brief

Load `${CLAUDE_PLUGIN_ROOT}/skills/distill/references/founder-brief-template.md` and write `idea.md` into `<workspace>/<slug>/`.

The brief is the **founder's own voice**, not the mentor's. Honor the resolved `voice` slot if present (as `present`/memo do); else a neutral, confident-but-honest founder tone. Hard rules:
- **Faithful, not idealized.** Represent the idea as last concluded — *including its rough edges*. The owner asked for the real idea "even if it has problems." Do not silently fix flaws, and do not fold the mentor's recommendations in as if they were already resolved.
- **No critique trail.** Strip every boote artifact: no rubric scores, no `validation_stage`/`evidence_level` jargon, no `continue`/`pivot`/`kill` verdict, no mention of boote, the critic, or rounds. It must read like a founder wrote it.
- **Self-contained.** No links to rounds/research/economics (they are about to vanish). Inline the facts that matter with source + date.
- **Honest about the unknowns** in the founder's own words (the "what I'm still figuring out" section) — this is where the problems live, owned by the founder, not framed as a verdict.
- **Re-ingestable.** Cover the same ground `boote new` needs (customer, problem, why-now, why-you, how it works, alternatives, model, evidence) so the owner can paste it straight into a fresh `boote new`.
- English, no emoji (house style); honor `output_style`. About one page, scannable.

## Step 4 — show the brief and the deletion plan; get explicit confirmation

1. Print the full `idea.md` content back to the owner.
2. List the **exact** paths that will be permanently deleted — everything under `<workspace>/<slug>/` except `idea.md`:
   ```
   ls -A "<workspace>/<slug>"
   ```
   State plainly that all of it except `idea.md` will be erased with **no backup**.
3. Ask the owner to **type the idea's slug** to confirm. Proceed ONLY if the reply is *exactly* the slug. Any other reply — "yes", "ok", "go", a typo — aborts with nothing deleted.

## Step 5 — purge (only after the slug was typed)

Erase everything in the idea folder except `idea.md`. Use the guarded command below — it refuses to run unless the brief exists and the path is a real directory, and it deletes depth-first via `find -delete` (**no `rm -rf`**, so it also works in hardened environments that deny force-recursive deletes):

```
IDEA_DIR="<absolute workspace path>/<slug>"
[ -n "$IDEA_DIR" ] && [ -d "$IDEA_DIR" ] && [ -f "$IDEA_DIR/idea.md" ] \
  || { echo "refuse: brief missing or bad path"; exit 1; }
find "$IDEA_DIR" -mindepth 1 ! -name 'idea.md' -delete
```

`-mindepth 1` protects the folder itself, `! -name idea.md` preserves the brief, and `-delete` removes the files and the now-empty subfolders (rounds/research/economics/presentations) depth-first. Never run this with an unset or empty `IDEA_DIR`, never widen the scope beyond the one idea folder, and never run it before `idea.md` is written.

## Step 6 — report

Confirm what remains (`<workspace>/<slug>/idea.md` only) and that the history is gone. Point the owner at the file, and note they can now share it or re-seed a fresh idea with its contents via `boote new`.

## Safety rules (always)
- Manual-only; produce-and-show before delete; explicit slug confirmation; **no backup/archive** — the owner wants no trace, and that is the point.
- Operate on **exactly one** idea folder, scoped under the resolved workspace. Never delete the workspace root, a sibling idea, `_learnings.md`, `_archive/`, or anything outside `<workspace>/<slug>/`.
- If anything is ambiguous (which idea, missing dossier, can't resolve the workspace), **stop and ask** — never guess on a destructive operation.

## Self-check before deleting
- [ ] `idea.md` written — founder's voice, self-contained, no boote/critique traces, faithful to the last concluded idea (problems included)?
- [ ] Full brief shown to the owner, plus the exact deletion list, with "no backup" stated?
- [ ] Owner confirmed by typing the **exact slug** (not "yes")?
- [ ] Delete scoped to `<workspace>/<slug>/` (everything except `idea.md`); path verified non-empty and real?

## Dependencies
- Reuses the bundled `scripts/discover-context.sh` (workspace + `voice` + `output_style` only; no gate enforcement).
- `references/founder-brief-template.md` — the founder-voice brief structure.
