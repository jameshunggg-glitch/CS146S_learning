# AGENTS.md

## Project Overview

This repository contains the Week 4 project: **AI News Digest System**.

The goal of this project is to:
1. search for the latest or top-result `n` news articles on a given topic
2. extract usable article information
3. generate structured summaries
4. save the results as Markdown files

This is a small engineering practice project focused on reusable workflows, skills, boundaries, and testable automation.

---

## Current Scope

This project is currently limited to **Version 1**.

Version 1 includes:
- topic-based news search
- selecting the top `n` latest or top-result articles
- summarizing article content
- saving article digests as Markdown files

Version 1 does **not** include:
- OCR or image input
- popularity scoring from social media
- paywall bypass
- large-scale crawling
- article rewriting into marketing copy
- publishing results to external platforms

Do not expand scope unless explicitly asked.

---

## Repository Structure

- `app/`
  - core application logic
  - search, summarization, writing, and data models
- `skills/`
  - reusable skill instructions
- `tests/`
  - test files for search, summarization, and markdown writing
- `outputs/`
  - generated Markdown files
- `week4_goal.md`
  - project blueprint and scope definition

---

## Engineering Principles

- Keep the implementation simple and inspectable.
- Prefer small functions and clear module boundaries.
- Do not fabricate article content.
- If extraction fails, report failure honestly.
- If fewer than `n` valid articles are found, return the available results and report that clearly.
- Treat incomplete extraction as a valid result state.
- Use structured outputs whenever possible.

---

## Expected Module Responsibilities

- `app/search.py`
  - search for topic-related news articles
  - return structured candidate results
- `app/summarizer.py`
  - summarize extracted article text
  - return summary and key points
- `app/writer.py`
  - save digest results as Markdown
- `app/models.py`
  - define shared data structures
- `app/main.py`
  - provide a minimal entrypoint for running the workflow

Keep responsibilities separated. Do not merge unrelated logic into one file unless explicitly needed.

---

## Testing Expectations

When modifying code:
- add or update relevant tests
- keep test scope focused
- prefer small deterministic tests

At minimum, validate:
- search output structure
- summarizer output structure
- markdown file generation

---

## Output Expectations

Each processed article should produce a Markdown file with a consistent structure.

Each output should include:
- title
- source
- URL
- published date if available
- extraction status
- summary
- key points
- warnings if needed

Do not claim successful extraction if the content was not actually extracted.

---

## Guardrails

Do not:
- bypass paywalls
- invent missing article text
- silently skip failed results
- perform broad crawling outside the requested task
- add unrelated features without being asked

Do:
- keep the workflow narrow
- report uncertainty clearly
- preserve readability
- keep Version 1 manageable

---

## Working Style

When implementing features:
1. understand the target file and module responsibility
2. make the smallest useful change
3. keep outputs structured
4. update tests if needed
5. avoid unnecessary refactors

Prefer incremental progress over large speculative rewrites.