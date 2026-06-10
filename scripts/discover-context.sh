#!/usr/bin/env bash
#
# discover-context.sh — resolve boote's host-context slots for a project.
#
# DESCRIPTION
#   boote is context-free: it ships zero company data. Instead, at the start
#   of every run it discovers the host project's own context. This script
#   resolves eight context slots, in order:
#
#     1. Explicit config — boote.config.md or .boote/config.md (slot: path).
#     2. Auto-discover  — scan for conventional files in the host.
#     3. Context-light  — leave empty; the skill runs generic + asks the owner.
#
#   It prints a human-readable manifest plus machine-parsable lines of the
#   form  BOOTE_CTX <slot> <value>|<source>  so callers can grep easily.
#
# USAGE
#   discover-context.sh [HOST_ROOT]   # default: current working directory
#
# EXIT STATUS
#   0  always — discovery never "fails", it just reports what was found.
#
# COMPATIBILITY
#   POSIX-ish; runs on macOS stock bash 3.2 (no associative arrays).
#
set -uo pipefail

ROOT="${1:-$PWD}"
ROOT="$(cd "$ROOT" 2>/dev/null && pwd || echo "$ROOT")"

SLOTS="strategy principles risks learnings workspace output_style voice research_key"

# slot value/source backing storage — bash 3.2 has no assoc arrays, so we
# synthesize variable names instead (v_<slot> = value, s_<slot> = source).
set_v() { printf -v "v_$1" '%s' "$2"; printf -v "s_$1" '%s' "$3"; }
get_v() { local n="v_$1"; printf '%s' "${!n:-}"; }
get_s() { local n="s_$1"; printf '%s' "${!n:-}"; }
for s in $SLOTS; do set_v "$s" "" ""; done

# ---- 1) explicit config ---------------------------------------------------
CFG=""
for c in "$ROOT/boote.config.md" "$ROOT/.boote/config.md"; do
  if [[ -f "$c" ]]; then CFG="$c"; break; fi
done
if [[ -n "$CFG" ]]; then
  for s in $SLOTS; do
    line="$(grep -iE "^[[:space:]]*${s}[[:space:]]*:" "$CFG" 2>/dev/null | head -1)"
    [[ -z "$line" ]] && continue
    rawval="$(printf '%s' "$line" | sed -E "s/^[[:space:]]*[a-zA-Z_]+[[:space:]]*:[[:space:]]*//; s/[[:space:]]*$//")"
    [[ -n "$rawval" ]] && set_v "$s" "$rawval" "config"
  done
fi

# parse the optional `mode:` line from config (full | context-light)
CFG_MODE=""
if [[ -n "$CFG" ]]; then
  CFG_MODE="$(grep -iE "^[[:space:]]*mode[[:space:]]*:" "$CFG" 2>/dev/null \
    | head -1 | sed -E 's/^[^:]*:[[:space:]]*//; s/[[:space:]]*$//' \
    | tr '[:upper:]' '[:lower:]')"
fi

# ---- helpers --------------------------------------------------------------
# find1 <iname-pattern> -> first match path relative to ROOT, skipping noise.
# Samples/examples are not canonical.
find1() {
  find "$ROOT" \
    \( -name .git -o -name node_modules -o -name .claude \
       -o -name archive -o -name _archive \
       -o -name samples -o -name examples \) -prune \
    -o -type f -iname "$1" -print 2>/dev/null \
  | head -1 | sed "s#^$ROOT/##"
}

# ---- 2) auto-discover unset slots -----------------------------------------
if [[ -z "$(get_v workspace)" ]]; then
  if [[ -d "$ROOT/boote" ]]; then set_v workspace "boote/" "auto"
  else                            set_v workspace "boote/" "default"
  fi
fi
WS="$(get_v workspace)"; WS="${WS%/}"

if [[ -z "$(get_v strategy)" ]]; then
  for p in '*current-strateg*.md' '*strateg*.md'; do
    m="$(find1 "$p")"
    if [[ -n "$m" ]]; then set_v strategy "$m" "auto"; break; fi
  done
fi
if [[ -z "$(get_v principles)" ]]; then
  for p in '*vision*value*.md' '*principle*.md' '*values*.md' '*vision*.md'; do
    m="$(find1 "$p")"
    if [[ -n "$m" ]]; then set_v principles "$m" "auto"; break; fi
  done
fi
if [[ -z "$(get_v risks)" ]]; then
  for p in '*risk*register*.md' '*risk*.md'; do
    m="$(find1 "$p")"
    if [[ -n "$m" ]]; then set_v risks "$m" "auto"; break; fi
  done
fi
if [[ -z "$(get_v output_style)" ]]; then
  for p in '*report*pref*.md' '*style-guide*.md'; do
    m="$(find1 "$p")"
    if [[ -n "$m" ]]; then set_v output_style "$m" "auto"; break; fi
  done
fi
if [[ -z "$(get_v voice)" ]]; then
  for p in '*voice*profile*.md' '*voice*.md' '*tone*.md'; do
    m="$(find1 "$p")"
    if [[ -n "$m" ]]; then set_v voice "$m" "auto"; break; fi
  done
fi
if [[ -z "$(get_v learnings)" ]]; then
  if [[ -f "$ROOT/$WS/_learnings.md" ]]; then
    set_v learnings "$WS/_learnings.md" "auto"
  else
    set_v learnings "$WS/_learnings.md" "default"
  fi
fi
if [[ -z "$(get_v research_key)" ]]; then
  if [[ -n "${GEMINI_API_KEY:-}" ]]; then
    set_v research_key "env:GEMINI_API_KEY (set)" "env"
  else
    set_v research_key "env:GEMINI_API_KEY (unset)" "env"
  fi
fi

# ---- verify file-backed slots exist ---------------------------------------
show_val() {
  local v="$1"
  case "$v" in
    env:*|none|"—"|"") printf '%s' "$v" ;;
    */)                printf '%s' "$v" ;;
    *)
      if [[ -f "$ROOT/$v" ]]; then printf '%s' "$v"
      else                          printf '%s  (MISSING)' "$v"
      fi ;;
  esac
}

# ---- gate -----------------------------------------------------------------
# Required-to-lift-the-gate slots: strategy (incl. hurdle) + principles (red
# lines). These are the verdict-changing ones; the rest have safe defaults.
req_ok=1
for s in strategy principles; do
  case "$(get_s "$s")" in config|auto) ;; *) req_ok=0 ;; esac
done

# explicit context-light opt-in: `mode: context-light` in config, or a marker
# file at <workspace>/.context-light.
optin=0
[[ "$CFG_MODE" = "context-light" ]] && optin=1
[[ -f "$ROOT/$WS/.context-light" ]] && optin=1

if   (( req_ok )); then GATE="resolved"
elif (( optin ));  then GATE="context-light"
else                    GATE="blocked"
fi

if [[ -n "$CFG" ]]; then SRC="configured ($CFG)"; else SRC="auto-discovery"; fi

# ---- output ---------------------------------------------------------------
echo "# boote context manifest"
echo "host: $ROOT"
echo "gate: $GATE"
echo "source: $SRC"
[[ -n "$CFG_MODE" ]] && echo "config mode: $CFG_MODE"
echo
printf '%-14s %-10s %s\n' "slot" "source" "value"
printf '%-14s %-10s %s\n' "----" "------" "-----"
for s in $SLOTS; do
  v="$(get_v "$s")"; [[ -z "$v" ]] && v="—"
  src="$(get_s "$s")"; [[ -z "$src" ]] && src="none"
  printf '%-14s %-10s %s\n' "$s" "$src" "$(show_val "$v")"
done
echo
echo "# machine-readable"
echo "BOOTE_GATE $GATE"
for s in $SLOTS; do
  v="$(get_v "$s")"; [[ -z "$v" ]] && v="-"
  src="$(get_s "$s")"; [[ -z "$src" ]] && src="none"
  echo "BOOTE_CTX $s $v|$src"
done

case "$GATE" in
  blocked)
    cat <<'EOF'

NOTE: gate=blocked — no host strategy/principles (and hurdle) found, and no
      explicit context-light opt-in. boote will NOT critique/model/present in
      this state; the skill routes to `boote init` to collect the required
      context. Run `boote init`, or set `mode: context-light` in
      boote.config.md to proceed without host context (host-fit / red-line /
      hurdle checks off).
EOF
    ;;
  context-light)
    cat <<'EOF'

NOTE: gate=context-light (explicit opt-in) — running on generic YC/Techstars
      methodology. Host-fit, red-line, and hurdle checks are DISABLED. Add
      strategy + principles to boote.config.md (or run `boote init`) to enable.
EOF
    ;;
esac
