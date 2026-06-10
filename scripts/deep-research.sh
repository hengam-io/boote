#!/usr/bin/env bash
#
# deep-research.sh — thin entry point over boote's grounded research engine.
#
# DESCRIPTION
#   The original engine used Gemini's Deep-Research *background Interactions*
#   API. With this project's key those background jobs were accepted but
#   never executed — they hung at status=in_progress forever. The current
#   engine (rebuilt 2026-06-01) is synchronous: it runs an agentic loop on
#   the grounded `generateContent` path (gemini-* + google_search), which is
#   fast and reliably cited. All real work lives in research_engine.py.
#
# USAGE
#   deep-research.sh run \
#     --query "QUESTION" \
#     --out research/YYYY-MM-DD-slug.md \
#     [--depth fast|deep] [--model MODEL]
#
#     fast (default) ~4 sub-questions, ~1–3 min.
#     deep            ~8 sub-questions, ~3–6 min.
#
#   Run in the background (Bash run_in_background) so it survives across
#   turns; on completion it prints a single line:  STATUS_JSON: {...}
#
# ENVIRONMENT
#   GEMINI_API_KEY  required — read from .claude/settings.local.json (env
#                   block, gitignored). Never committed.
#
# EXIT STATUS
#   0  success
#   1  handled failure (missing key, total research failure)
#   2  argument error
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENGINE="$SCRIPT_DIR/research_engine.py"

die()    { printf 'ERROR: %s\n' "$1" >&2; exit "${2:-1}"; }
usage()  { sed -n '2,/^set -euo/p' "$0" | sed -n '/^#/!q; s/^#\s*//;p'; }

CMD="${1:-}"
shift || true

case "$CMD" in
  run)
    [[ -n "${GEMINI_API_KEY:-}" ]] || die \
      "GEMINI_API_KEY not set. Add it to .claude/settings.local.json (env
       block). If it was working and stopped (401/403), re-issue it from your
       Gemini API provider (e.g. Google AI Studio)."
    [[ -f "$ENGINE" ]] || die "engine not found at $ENGINE"
    exec python3 "$ENGINE" "$@"
    ;;
  ""|-h|--help|help)
    usage
    ;;
  *)
    die "unknown command: $CMD (use: run | help). Async start/poll/wait/check
       were removed with the dead background engine — the new engine is
       synchronous." 2
    ;;
esac
