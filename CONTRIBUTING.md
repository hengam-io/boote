# Contributing to boote

Thanks for your interest in improving **boote**. It is a Claude Code plugin — a
skill, three subagents, a reference knowledge base, and two helper scripts — so
contributing usually means editing Markdown prompts and small Bash/Python
scripts rather than a large application codebase.

## Ways to contribute

- **Sharpen the mentor brain** — improve the methodology, critique rubric, or
  economics framework under [`skills/boote/references/`](skills/boote/references/).
- **Improve the prompts** — make the skill ([`SKILL.md`](skills/boote/SKILL.md))
  or an agent ([`agents/`](agents/)) clearer, more reliable, or better calibrated.
- **Harden the scripts** — [`discover-context.sh`](scripts/discover-context.sh),
  [`deep-research.sh`](scripts/deep-research.sh),
  [`research_engine.py`](scripts/research_engine.py).
- **Docs & examples** — anything that lowers the cost of adopting boote.
- **Bug reports & ideas** — open an issue.

## Local setup

boote has no build step. To develop against a live Claude Code, install the
plugin from your local checkout:

```bash
git clone https://github.com/hengam-io/boote.git
cd boote
```

Then, inside Claude Code (run from the repo root):

```
/plugin marketplace add ./
/plugin install boote
```

Editing `SKILL.md` takes effect immediately in the current session. Changes to
`plugin.json`, agents, or scripts take effect after `/reload-plugins` or a
restart.

## Before opening a pull request

Run the same checks CI runs:

```bash
claude plugin validate . --strict           # plugin & marketplace manifests
shellcheck scripts/*.sh                      # Bash linting
ruff check scripts/                          # Python linting
python3 -m py_compile scripts/research_engine.py
```

## Conventions

- **English, no emoji** — in everything the plugin produces and in the repo
  itself.
- **Keep `SKILL.md` lean.** Deep material lives in `references/` and is loaded on
  demand (progressive disclosure). Link to it; do not inline it.
- **One idea, one folder.** The `dossier.md` is the only living source; rounds,
  economics, and presentations *link* to it — they never copy it.
- **No company data in the plugin.** boote is context-free; host context is
  discovered at runtime, never hardcoded.
- **Secrets stay out of git.** `GEMINI_API_KEY` belongs in the gitignored
  `.claude/settings.local.json`.
- **Commits** follow [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`).

## Code of Conduct

By participating, you agree to uphold this project's
[Code of Conduct](CODE_OF_CONDUCT.md).
