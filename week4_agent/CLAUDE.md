# CLAUDE.md

## Project Context
This repository is a small AI news digest tool and a practice repo for human-agent collaborative development.

The product goal is to build a simple CLI tool that:
- accepts a topic,
- finds a few related news articles,
- fetches article content,
- cleans noisy text,
- generates short summaries,
- saves Markdown outputs for personal knowledge-base use.

The workflow goal is equally important:
this repo is meant to practice a documentation-first, human-agent collaboration style of software development, instead of a copy-paste coding workflow.

This project is currently in the MVP stage.

---

## Read This First
Before making changes, read `PROJECT_BRIEF.md`.

Use `PROJECT_BRIEF.md` as the main source of truth for:
- project purpose,
- MVP scope,
- functional expectations,
- initial testing direction,
- repository structure.

Use `week4_agent_progress.md` for:
- current project status,
- what has already been implemented,
- what is still placeholder/stub,
- the next recommended step for the next session.

Do not assume extra features beyond the current MVP unless the user explicitly asks for them.

If the current code and the brief conflict, prefer conservative changes and explain the mismatch.

---

## Current Repo Structure
The repository is expected to follow this structure in the first version:

```text
week4/
  app/
    main.py
    search.py
    fetch.py
    clean.py
    summarize.py
    writer.py
  output/
  tests/
    test_clean.py
    test_writer.py
    test_integration.py
  CLAUDE.md
  PROJECT_BRIEF.md
```

Expected file responsibilities:

- `app/main.py`: CLI entry point
- `app/search.py`: search for relevant news articles
- `app/fetch.py`: fetch article content from URLs
- `app/clean.py`: clean noisy article text
- `app/summarize.py`: summarize cleaned article text
- `app/writer.py`: write Markdown outputs
- `tests/`: small focused tests for core behaviors

Prefer working within this structure.
Do not introduce unnecessary new files, frameworks, or architectural layers unless clearly needed.

---

## Working Rules
When working in this repository, follow these rules:

1. Start with the smallest useful change.
2. Do not redesign the whole project unless explicitly asked.
3. Keep implementations simple, readable, and modular.
4. Prefer focused edits over large rewrites.
5. Respect the MVP scope defined in `PROJECT_BRIEF.md`.
6. Do not silently expand the project scope.
7. Avoid adding new dependencies unless there is a clear need.
8. Prefer practical solutions over overengineering.
9. Keep functions easy to read and easy to test.
10. When unsure, choose the more conservative implementation.

Important constraints:
- Do not add frontend code unless explicitly requested.
- Do not add database, RAG, scheduling, or deployment features unless explicitly requested.
- Do not optimize prematurely.
- Do not replace the repo structure with a different one unless the user approves it.

---

## Testing Expectations
This project should include small, practical tests, but not a heavy testing system in the first stage.

Priorities:
1. `clean.py` tests
2. `writer.py` tests
3. one small integration test using fake article data

Good first tests include:
- removing noise strings such as `Continue reading`
- reducing excessive blank lines
- preserving normal article content
- verifying Markdown output contains expected sections
- verifying two Markdown outputs can be generated from fake data

Not a priority yet:
- live network-based search tests
- brittle tests against real websites
- strict summary quality tests

The goal of testing in this stage is to protect the core text-processing pipeline from obvious breakage.

---

## Communication Style
When completing a task, report back clearly and briefly.

A good task summary should include:
- what files were changed,
- what was implemented,
- any assumptions made,
- anything still incomplete,
- how the user can run or verify the result.

If something is uncertain, say so directly.
Do not hide assumptions.
Do not imply that unverified behavior is confirmed.

---

## Human-Agent Boundary
The human is responsible for:
- project direction,
- scope decisions,
- priorities,
- final review and acceptance.

The agent is responsible for:
- reading project documents,
- proposing focused implementation steps,
- making small code changes,
- adding small tests where appropriate,
- explaining what changed.

The agent should not:
- silently expand scope,
- make major product decisions alone,
- perform broad refactors without approval,
- replace the intended workflow with a different one.

When uncertain, ask for clarification only if it is truly blocking.
Otherwise, make the smallest reasonable assumption and state it clearly.

---

## Default Mindset
This repository is not about building the biggest system as fast as possible.

It is about:
- building a useful small tool,
- keeping the repo understandable,
- letting the human stay in control,
- using the agent as a careful implementation partner.

Optimize for clarity, momentum, and collaboration.
