#!/usr/bin/env python3
"""boote deep-research engine — multi-step, web-grounded, cited research.

Why this exists
---------------
The previous engine used Gemini's Deep-Research *background Interactions* API.
Verified empirically (2026-06-01) that, with this project's Antigravity key, those
background jobs are ACCEPTED but NEVER EXECUTED — they sit at status=in_progress
with only the user_input step, `updated` never moving, even days later. So nothing
ever came back. This engine uses the synchronous grounded `generateContent` path.

This engine instead uses the grounded `generateContent` path — a Gemini model with
the `google_search` tool — which is synchronous, fast, and reliably cited. To get
real depth (not a single shallow answer) it runs an agentic loop:

  1. PLAN       decompose the question into focused, search-friendly sub-questions
  2. RESEARCH   one grounded web-search call per sub-question (real sources)
  3. SYNTHESIZE combine the findings into a structured, cited English report
  4. WRITE      research/<...>.md = executive-summary marker + report + Sources

The skill (Claude) then reads the .md and writes a one-page executive summary into
the <!-- EXECUTIVE_SUMMARY --> marker.

Usage
-----
    research_engine.py --query "QUESTION" --out research/YYYY-MM-DD-slug.md \\
        [--depth fast|deep] [--model MODEL]

Environment
-----------
    GEMINI_API_KEY   required. Read from the .claude/settings.local.json env block
                     (which is gitignored), never committed.
    GEMINI_MODEL     optional. Default model when --model is not passed.

The script prints a single machine-readable line to stdout for the wrapper / Claude
to parse:  STATUS_JSON: {...}  . All diagnostics go to stderr. Exit code is 0 on
success, 1 on a handled failure (missing key, total research failure).

No third-party dependencies — standard library only.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import logging
import os
import re
import sys
import time
import urllib.error
import urllib.request

API_ROOT = "https://generativelanguage.googleapis.com/v1beta/models"

# Cheap default (~10x cheaper than Pro), fine for routine research. Escalate via
# --model (or the GEMINI_MODEL env var) to a Pro model for high-stakes work —
# sharper and more numeric, but materially pricier per deep run on a billed key.
DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

DEPTHS = {"fast": 4, "deep": 8}            # number of sub-questions
RESEARCH_CONCURRENCY = 3                    # gentle parallelism for the search calls
MAX_RETRIES = 4
RETRY_BASE = 3                              # seconds, exponential backoff

logger = logging.getLogger("boote.research")


class ResearchError(Exception):
    """A handled, user-facing error (missing key, total research failure)."""


def log(msg: str) -> None:
    """Emit a diagnostic line to stderr (stdout is reserved for STATUS_JSON)."""
    logger.info(msg)


def api_key() -> str:
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if not k:
        raise ResearchError(
            "GEMINI_API_KEY not set. Add it to .claude/settings.local.json "
            "(env block). If it was working and stopped (401/403), re-issue it "
            "from your Gemini API provider (e.g. Google AI Studio)."
        )
    return k


def _post(model: str, body: dict, timeout: int = 120) -> dict:
    """POST to generateContent; return parsed JSON. Raises on HTTP error."""
    url = f"{API_ROOT}/{model}:generateContent"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("x-goog-api-key", api_key())
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def call_model(
    prompt: str,
    grounded: bool = True,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.4,
    timeout: int = 120,
) -> tuple[str, list[dict], list[str]]:
    """One generateContent call with retries. Returns (text, sources, queries).

    sources: list of {"uri", "title"}.  queries: web-search queries the model ran.
    Transient failures (timeout, 429, 5xx) are retried with backoff; on permanent
    failure raises RuntimeError so the caller can decide how to degrade."""
    body: dict = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temperature},
    }
    if grounded:
        body["tools"] = [{"google_search": {}}]

    last_err: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            d = _post(model, body, timeout=timeout)
            if "error" in d:
                code = d["error"].get("code")
                # 429 / 5xx are transient; everything else is fatal
                if code in (429, 500, 503) and attempt < MAX_RETRIES:
                    raise urllib.error.HTTPError(
                        url=None, code=code, msg=str(d["error"].get("message", "")),
                        hdrs=None, fp=None,
                    )
                raise RuntimeError(f"API error {code}: {d['error'].get('message', '')[:300]}")
            return _parse(d)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError,
                json.JSONDecodeError, ConnectionError) as e:
            last_err = e
            if attempt < MAX_RETRIES:
                wait = RETRY_BASE * attempt
                log(f"    transient error ({type(e).__name__}); retry {attempt}/{MAX_RETRIES - 1} in {wait}s")
                time.sleep(wait)
            else:
                raise RuntimeError(f"call failed after {MAX_RETRIES} attempts: {last_err}") from last_err
    raise RuntimeError(f"call failed: {last_err}")  # unreachable, satisfies type checkers


def _parse(d: dict) -> tuple[str, list[dict], list[str]]:
    cands = d.get("candidates") or []
    if not cands:
        return "", [], []
    c = cands[0]
    text = " ".join(
        p.get("text", "") for p in c.get("content", {}).get("parts", []) if isinstance(p, dict)
    ).strip()
    gm = c.get("groundingMetadata", {}) or {}
    sources: list[dict] = []
    for ch in gm.get("groundingChunks", []) or []:
        w = ch.get("web", {}) or {}
        uri = w.get("uri")
        if uri:
            sources.append({"uri": uri, "title": w.get("title") or uri})
    queries = gm.get("webSearchQueries", []) or []
    return text, sources, queries


# ----------------------------------------------------------------------------- plan

def make_plan(query: str, n: int, model: str) -> list[str]:
    """Ask the model for n focused, search-friendly sub-questions (JSON array)."""
    prompt = (
        "You are a senior research analyst planning a deep-research report. "
        f"Decompose the following research request into exactly {n} focused, "
        "non-overlapping sub-questions that together cover it comprehensively. "
        "Each sub-question must be self-contained and good for a web search "
        "(specific entities, timeframe, geography where relevant). "
        "Return ONLY a JSON array of strings, nothing else.\n\n"
        f"RESEARCH REQUEST:\n{query}"
    )
    text, _, _ = call_model(prompt, grounded=False, model=model, temperature=0.3)
    subqs = _extract_json_array(text)
    # Fallbacks so we never hard-fail at the planning stage.
    if not subqs:
        log("    plan parse failed; falling back to single-question research")
        return [query]
    return subqs[:n]


def _extract_json_array(text: str) -> list[str]:
    if not text:
        return []
    # strip code fences if present
    m = re.search(r"\[.*\]", text, re.DOTALL)
    if not m:
        return []
    try:
        arr = json.loads(m.group(0))
        return [str(x).strip() for x in arr if str(x).strip()]
    except (json.JSONDecodeError, TypeError):
        return []


# ------------------------------------------------------------------------- research

def research_one(idx: int, subq: str, model: str) -> dict:
    prompt = (
        "Research the following question using up-to-date web sources. "
        "Give a thorough, factual answer with concrete figures, names, and dates "
        "where available. Note any conflicting information or uncertainty explicitly. "
        "Do not speculate beyond the sources.\n\n"
        f"QUESTION: {subq}"
    )
    try:
        text, sources, queries = call_model(prompt, grounded=True, model=model, temperature=0.4)
        log(f"    [{idx}] done — {len(text)} chars, {len(sources)} sources")
        return {"subq": subq, "text": text, "sources": sources, "queries": queries, "ok": bool(text)}
    except RuntimeError as e:
        log(f"    [{idx}] FAILED: {e}")
        return {"subq": subq, "text": "", "sources": [], "queries": [], "ok": False, "error": str(e)}


def run_research(subqs: list[str], model: str) -> list[dict]:
    results: list[dict | None] = [None] * len(subqs)
    with concurrent.futures.ThreadPoolExecutor(max_workers=RESEARCH_CONCURRENCY) as ex:
        futs = {ex.submit(research_one, i + 1, sq, model): i for i, sq in enumerate(subqs)}
        for fut in concurrent.futures.as_completed(futs):
            results[futs[fut]] = fut.result()
    return [r for r in results if r is not None]


# ------------------------------------------------------------------------ synthesize

def synthesize(query: str, findings: list[dict], model: str) -> tuple[str, list[dict]]:
    """Combine sub-findings into a structured English report. Grounded so it can
    reconcile/fill small gaps, but instructed to rely on the gathered material."""
    blocks = []
    for i, f in enumerate(findings, 1):
        if f and f.get("text"):
            blocks.append(f"### Finding {i}: {f['subq']}\n{f['text']}")
    material = "\n\n".join(blocks)
    prompt = (
        "You are writing the final deep-research report for a CEO. Below is research "
        "material gathered from multiple web searches on sub-questions of the main "
        "request. Synthesize it into a single, well-structured English report.\n\n"
        "Requirements:\n"
        "- Open with a short '## Executive Summary' (the key findings, 4-8 bullet points).\n"
        "- Then organized sections with '##' headers covering the substance.\n"
        "- Be specific: keep concrete figures, names, dates. Note conflicts/uncertainty.\n"
        "- Do NOT invent facts beyond the material. If something is unknown, say so.\n"
        "- No emoji. Plain professional prose and bullets.\n\n"
        f"MAIN RESEARCH REQUEST:\n{query}\n\n"
        f"GATHERED MATERIAL:\n{material}"
    )
    text, sources, _ = call_model(prompt, grounded=True, model=model, temperature=0.5, timeout=180)
    return text, sources


# ------------------------------------------------------------------------------ write

def dedupe_sources(all_sources: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for s in all_sources:
        uri = s.get("uri")
        if uri and uri not in seen:
            seen.add(uri)
            out.append(s)
    return out


def write_report(
    out_path: str,
    query: str,
    model: str,
    depth: str,
    report_text: str,
    sources: list[dict],
    findings: list[dict],
    ok_count: int,
    total: int,
) -> None:
    def esc(s: object) -> str:
        return str(s).replace('"', "'").replace("\n", " ")[:600]

    fm = [
        "---",
        f'query: "{esc(query)}"',
        "engine: gemini-grounded-research",
        f"model: {model}",
        f"depth: {depth}",
        f"sub_questions: {total}",
        f"sub_questions_ok: {ok_count}",
        f"source_count: {len(sources)}",
        "status: completed",
        "---",
        "",
    ]
    body = ["<!-- EXECUTIVE_SUMMARY -->", ""]
    if report_text:
        body += ["# Full Research Report (Gemini grounded research)", "", report_text, ""]
    else:
        body += ["# (No report text produced)", "",
                 "Synthesis returned empty. Sub-question findings are preserved below.", ""]
        for f in findings:
            if f.get("text"):
                body += [f"## {f['subq']}", "", f["text"], ""]

    if sources:
        body += ["## Sources", ""]
        for n, s in enumerate(sources, 1):
            label = s.get("title") or s.get("uri")
            body.append(f"{n}. [{label}]({s['uri']})")
        body.append("")

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(fm) + "\n".join(body) + "\n")


# ------------------------------------------------------------------------------- main

def _print_status(payload: dict) -> None:
    """The single machine-readable contract line, on stdout."""
    print("STATUS_JSON: " + json.dumps(payload))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="research_engine.py",
        description="boote grounded deep-research engine "
        "(plan → research → synthesize → write).",
        epilog="Requires GEMINI_API_KEY in the environment. "
        "Writes a single STATUS_JSON: {...} line to stdout on completion; "
        "diagnostics go to stderr.",
    )
    ap.add_argument("--query", required=True, help="the research question, in English")
    ap.add_argument("--out", required=True, help="output Markdown path (created if missing)")
    ap.add_argument(
        "--depth",
        choices=list(DEPTHS),
        default="fast",
        help="fast = ~4 sub-questions, deep = ~8 sub-questions (default: fast)",
    )
    ap.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Gemini model id (default: %(default)s, or $GEMINI_MODEL)",
    )
    args = ap.parse_args(argv)

    api_key()  # fail fast if missing (raises ResearchError)
    n = DEPTHS[args.depth]
    t0 = time.time()

    log(f"[1/3] planning — decomposing into {n} sub-questions ({args.depth})")
    subqs = make_plan(args.query, n, args.model)
    log(f"      {len(subqs)} sub-questions:")
    for i, s in enumerate(subqs, 1):
        log(f"        {i}. {s}")

    log(f"[2/3] researching {len(subqs)} sub-questions (concurrency={RESEARCH_CONCURRENCY})")
    findings = run_research(subqs, args.model)
    ok = [f for f in findings if f and f.get("ok")]
    ok_count = len(ok)

    if ok_count == 0:
        # total research failure — emit a clear status, don't write a fake report
        _print_status({
            "status": "failed", "reason": "all sub-question searches failed",
            "out": args.out, "sub_questions": len(subqs), "sub_questions_ok": 0,
            "elapsed_s": round(time.time() - t0),
        })
        return 1

    log(f"[3/3] synthesizing report from {ok_count}/{len(subqs)} findings")
    report_text, synth_sources = synthesize(args.query, findings, args.model)

    all_sources: list[dict] = []
    for f in findings:
        all_sources += (f.get("sources") or [])
    all_sources += synth_sources
    sources = dedupe_sources(all_sources)

    write_report(args.out, args.query, args.model, args.depth,
                 report_text, sources, findings, ok_count, len(subqs))

    _print_status({
        "status": "completed",
        "out": args.out,
        "report_chars": len(report_text),
        "sources": len(sources),
        "sub_questions": len(subqs),
        "sub_questions_ok": ok_count,
        "depth": args.depth,
        "elapsed_s": round(time.time() - t0),
    })
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stderr)
    try:
        sys.exit(main())
    except ResearchError as exc:
        logger.error("ERROR: %s", exc)
        _print_status({"status": "failed", "reason": str(exc)})
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error("interrupted")
        sys.exit(130)
