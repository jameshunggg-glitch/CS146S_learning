# PROJECT_BRIEF.md

## Project Name
AI News Digest Agent

## Project Purpose
This project is a small personal knowledge-base tool for collecting topic-based news.

The user provides a topic such as `AI`, and the tool will:
1. search for a few related news articles,
2. fetch the article content,
3. clean the raw article text,
4. generate a short summary for each article,
5. save both the digest and cleaned article content as Markdown files.

This is not intended to be a production-ready app.
The main goal is to build a useful personal tool while practicing human-agent collaborative development with Claude Code.

---

## Learning Goal
The main learning goal of this project is to practice a new development workflow:

- use documentation to define scope before coding,
- let a coding agent help implement small tasks,
- keep the human responsible for direction and review,
- avoid the old copy-paste style workflow as the default approach.

This project is inspired by the CS146S week4 theme, but it does not need to follow the assignment exactly.

---

## Repository Structure
The project should follow this structure in the first version:

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
  AGENTS.md
  PROJECT_BRIEF.md
```

This structure should be treated as the default working layout for the agent.

---

## MVP Scope
The first version should support the following flow:

1. Input a topic from the command line, for example:
   `python main.py --topic "AI"`
2. Search for a few related news articles.
3. Fetch article content from each result.
4. Clean the fetched text by removing obvious noise.
5. Generate a short summary for each cleaned article.
6. Save two Markdown outputs:
   - one digest file for quick reading,
   - one articles file containing cleaned article text.

---

## Target User
The primary user is the project owner.

This tool is meant for:
- personal reading,
- collecting topic-based news,
- building a personal Markdown knowledge base.

---

## Non-Goals
The first version will **not** focus on:

- building a frontend UI,
- scheduling or full automation,
- database storage,
- vector database / RAG,
- exporting to multiple formats,
- perfect article extraction for every site,
- advanced deduplication,
- production deployment.

---

## Functional Requirements

### 1. Topic Input
The tool should accept a single topic as input from CLI.

Example:
```bash
python main.py --topic "AI"
```

---

### 2. News Search
The tool should retrieve a few news articles related to the topic.

Each article should ideally include:
- title
- url
- source
- published date (if available)

---

### 3. Article Fetching
The tool should fetch article content from each news link.

The fetched result does not need to be perfect in v1, but it should return enough readable text to continue the pipeline.

---

### 4. Text Cleaning
The tool should clean noisy article text before summarization and storage.

Examples of noise to remove:
- `Continue reading`
- `Read more`
- `Subscribe`
- `Sign up`
- `Advertisement`
- broken empty lines
- obviously meaningless short lines

Goal:
preserve the main article body in a cleaner, more readable form.

---

### 5. Summarization
The tool should generate a short summary for each cleaned article.

v1 summary target:
- 3 to 5 bullet points, or
- a short 3 to 5 sentence summary

The goal is readability, not deep analysis.

---

### 6. Markdown Output
The tool should save all outputs as Markdown files.

#### Digest file
Purpose: quick reading

Suggested filename:
`output/{topic}_{date}_digest.md`

Suggested contents:
- topic
- generated time
- article count
- for each article:
  - title
  - source
  - date
  - link
  - short summary

#### Articles file
Purpose: personal knowledge-base storage

Suggested filename:
`output/{topic}_{date}_articles.md`

Suggested contents:
- title
- source
- date
- link
- cleaned article text

---

## Definition of Success
The MVP is successful if:

- the user can input a topic,
- the tool can retrieve a few related articles,
- the tool can extract readable article text,
- the tool can clean the text,
- the tool can generate short summaries,
- the tool can save two Markdown files,
- the final files are useful enough to keep as personal knowledge-base notes.

---

## Initial Testing Plan
This project does not need a heavy testing system in the first stage, but it should include a few small tests to protect the most important parts.

### Testing Philosophy
The first tests should focus on the most stable and important parts of the pipeline:
- text cleaning
- Markdown output
- one small end-to-end flow using fake data

The goal is not perfect coverage.
The goal is to make sure the core text-processing pipeline does not easily break.

### Initial Test Scope

#### 1. `clean.py` tests
Test that the cleaner can:
- remove common noise strings such as `Continue reading`
- reduce excessive blank lines
- remove obviously meaningless short lines
- preserve normal article content

#### 2. `writer.py` tests
Test that the Markdown writer can:
- generate a digest file with the expected sections
- include title, source, link, and summary
- generate an articles file with cleaned article text

#### 3. small integration test
Use fake article data to verify that:
- cleaned text can be passed into the writer,
- both Markdown outputs can be generated successfully.

### What Not to Test Yet
The first version does **not** need to focus on:
- live network-based search tests,
- strict summary quality tests,
- full end-to-end tests against real websites.

Those can be added later if needed.

---

## Final Note
This project is both:
1. a small personal AI news knowledge-base tool,
2. a practice project for human-agent collaborative development.

The product matters, but the workflow also matters.
The repo should gradually become more agent-friendly over time.
