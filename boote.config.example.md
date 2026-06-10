# boote.config — host context map

Copy this file to your repository root as **`boote.config.md`** (or
`.boote/config.md`) and point each slot at YOUR project's files. boote reads it
at the start of every run so it can use your company's real strategy,
principles, and hurdle instead of generic placeholders. The easiest way to
create it is to run **`boote init`**, which fills this in interactively. See
[`skills/boote/references/context-discovery.md`](skills/boote/references/context-discovery.md)
for the full model.

> **boote requires context.** Without `strategy` (incl. a hurdle rate) and
> `principles` (your red lines), boote runs **blocked** and will not critique,
> model, or present — it routes you to `boote init`. To deliberately run on
> pure YC/Techstars methodology with host-fit/red-line/hurdle checks **off**,
> set `mode: context-light` (an explicit, announced opt-in — never a silent
> default).

Paths are relative to the repo root. Use `none` to opt a slot out. Omit a slot
to let boote auto-discover it.

```
mode:         full            # full (default) | context-light
strategy:     path/to/strategy.md          # REQUIRED (portfolio fit + hurdle)
principles:   path/to/values-or-principles.md   # REQUIRED (values + red lines)
risks:        path/to/risk-register.md     # recommended
learnings:    boote/_learnings.md
workspace:    boote/
output_style: path/to/reporting-style.md
voice:        path/to/voice-profile.md
research_key: env:GEMINI_API_KEY
```

Free-form notes after the block become extra framing for this host. Put the
hurdle rate and red lines here if they aren't in a dedicated doc, for example:

- Hurdle rate (opportunity cost for go/no-go): 15%
- Product red lines: no weapons, tobacco, alcohol, adult goods
- Ownership/transfer constraints to check on any sale or structural deal:
  <describe, or "none">
