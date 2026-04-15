# week4_agent — Progress Notes

## Current Status
MVP is complete. All six modules are implemented and the real pipeline is fully wired.
Running `python -m app.main --topic "AI"` executes the full search → fetch → clean → summarize → write flow using real network calls.
85 tests passing; no remaining stubs. Minor stability patch applied: `fetch_article()` now sends a User-Agent header consistent with `search_articles()`.

---

## Completed So Far
- Project structure bootstrapped: `app/`, `output/`, `tests/`
- `CLAUDE.md` and `PROJECT_BRIEF.md` define scope and working rules
- `app/clean.py` — fully implemented: noise phrase removal, pure-punctuation line removal, excessive blank-line collapsing
- `tests/test_clean.py` — 11 passing tests covering all cleaning rules and false-positive guards
- `app/writer.py` — fully implemented: `write_digest()` and `write_articles()` write Markdown files to `output/`
- `tests/test_writer.py` — 20 passing tests covering file creation, filename format, content presence, and edge cases
- `app/main.py` — fake-data CLI wired up: accepts `--topic`, cleans raw text, summarizes, writes both Markdown outputs
- `tests/test_integration.py` — 6 passing tests verifying the clean → write pipeline end-to-end using fake data
- `app/summarize.py` — extractive summarizer implemented: picks first 3 lines >= 20 chars from cleaned text; no network calls required
- `tests/test_summarize.py` — 11 passing tests covering normal text, sentence limit, short-line filtering, and edge cases
- `app/fetch.py` — implemented as two layers: `extract_text(html)` pure function strips HTML tags using `html.parser`; `fetch_article(url)` thin urllib HTTP layer with User-Agent header, delegates to `extract_text()`, returns "" on any error
- `tests/test_fetch.py` — 16 passing tests: 10 pure-function tests for `extract_text()`, 6 mock-based tests for `fetch_article()` including User-Agent header assertion; no live network calls
- `app/search.py` — implemented as two layers: `parse_rss(xml_text)` pure function parses Google News RSS XML using `xml.etree.ElementTree`; `search_articles(topic)` thin urllib HTTP layer fetches RSS and delegates to `parse_rss()`, returns [] on any error
- `tests/test_search.py` — 16 passing tests: 11 pure-function tests for `parse_rss()`, 5 mock-based tests for `search_articles()`; no live network calls; search source is Google News RSS (no API key required)
- `app/main.py` — real pipeline wired: `search_articles()` → `fetch_article()` → `clean_text()` → `summarize()` → writer; per-article fetch failures are skipped gracefully; empty search or all-fail exits with a clear message without writing files
- `tests/test_integration.py` — extended to 11 tests: original 6 clean→write tests plus 5 mock-based `run_pipeline()` tests covering success, empty search, all-fetch-fail, partial-fetch-fail, and no-write-on-failure
- `.gitignore` — excludes `__pycache__/`, `.claude/`, and generated `output/*.md`

---

## File Status

| File | Status |
|---|---|
| `app/clean.py` | Done — real implementation, 11 tests passing |
| `app/writer.py` | Done — real implementation, 20 tests passing |
| `app/main.py` | Done — real pipeline wired, graceful error handling, 5 pipeline tests passing |
| `tests/test_integration.py` | Done — 11 passing tests (clean→write pipeline + run_pipeline mock tests) |
| `app/summarize.py` | Done — extractive summarizer, 11 tests passing |
| `app/fetch.py` | Done — two-layer implementation with User-Agent header, 16 tests passing |
| `app/search.py` | Done — two-layer implementation, 16 tests passing |

---

## Next Recommended Step
MVP is complete. If continuing, the highest-value next improvements are:
1. Improve `extract_text()` in `fetch.py` to prefer `<article>` / `<main>` content over full-page text, reducing noise in real fetches.
2. Write a short README covering how to run the CLI and what output to expect.
3. Optionally upgrade `summarize.py` to use the Claude API for real summarization.

---

## Notes for a New Session
- Read `CLAUDE.md` and `PROJECT_BRIEF.md` before making any changes.
- Run all current tests with: `python -m pytest tests/ -v` from `week4_agent/` (85 tests total).
- Smoke-test the CLI with: `python -m app.main --topic "AI"` — writes two files to `output/`.
- The repo root is one level up: `/CS146S/`, remote is `CS146S_learning` on GitHub.
- Do not add new dependencies or expand scope beyond the MVP defined in `PROJECT_BRIEF.md`.
- The article dict shape used across modules: `title`, `url`, `source`, `published_date`, `cleaned_text`, `summary`.
