# Security Policy

## Reporting a vulnerability

Please report security issues **privately** — do not open a public issue.

- Open a [private security advisory](https://github.com/hengam-io/boote/security/advisories/new)
  with details and steps to reproduce.

Expect an initial response within a few days. Please allow a reasonable window
to address the issue before any public disclosure.

## What boote touches — and what it does not

boote is a context-free Claude Code plugin. A few notes relevant to security:

- **No secrets in the repository.** The only credential boote uses is a Gemini
  API key for the optional deep-research engine. It is read from the environment
  (`GEMINI_API_KEY`), which Claude Code loads from your **gitignored**
  `.claude/settings.local.json`. boote never writes the key to disk and never
  commits it.
- **Research queries are PII-cleaned.** The skill is instructed to strip personal
  and confidential information from any query sent to the external research API.
- **Shareable artifacts are redacted.** Memos and decks pass through a mandatory
  redaction step against the host's `output_style` before they are produced.
- **No telemetry.** The only network calls boote makes are the deep-research
  runs you explicitly invoke, which go to Google's Generative Language API.

## Supported versions

This project follows semantic versioning. Security fixes are applied to the
latest released minor version.
