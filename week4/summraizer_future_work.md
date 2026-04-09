# Future Work

## Purpose

This note captures a possible expansion path for the week4 project.
It is **not** the current implementation target.
The current project should stay focused on the original week4 learning goal:

1. Search for articles
2. Fetch article pages
3. Extract usable text
4. Summarize the article

This document is only a blueprint for future extension if the project grows later.

---

## Why this future direction may be useful

As the project becomes more realistic, the current `summarizer` responsibility may become too broad.
Right now it is acceptable for learning purposes, but in a larger project it may be better to separate:

* article fetching / extraction
* summarization
* writing / persistence

This separation would make the system easier to debug, test, and extend.

---

## Possible future architecture

### 1. Search layer

Responsible for finding candidate articles.

**Input:** topic or user query
**Output:** `ArticleCandidate`

Example responsibilities:

* search news feeds or APIs
* normalize metadata
* return article candidates with title, URL, source, and date

---

### 2. Fetch / Extract layer

Responsible for turning an article URL into usable article text.

**Input:** `ArticleCandidate`
**Output:** `ArticleRaw` (or similarly named intermediate model)

Possible responsibilities:

* fetch article page
* clean noisy page content
* extract usable text
* return extraction status and warnings
* optionally save processed raw article text as markdown

This layer should focus on **getting trustworthy source text**, not summarizing.

---

### 3. Summarize layer

Responsible for generating a digest from already extracted article text.

**Input:** `ArticleRaw`
**Output:** `ArticleDigest`

Possible responsibilities:

* create summary
* produce key points
* add warnings when extraction quality is weak
* later support LLM-based summarization

This layer should not be responsible for web fetching.

---

### 4. Write / Persist layer

Responsible for saving outputs.

Possible responsibilities:

* save raw article markdown
* save digest markdown
* control file names and output structure
* separate temporary artifacts from final deliverables

---

## Suggested future data flow

`ArticleCandidate`
→ `ArticleRaw`
→ `ArticleDigest`

### ArticleCandidate

Represents a search result candidate.

Possible fields:

* title
* url
* source
* published_date
* note

### ArticleRaw

Represents extracted article content.

Possible fields:

* title
* url
* source
* published_date
* extraction_status
* content_md
* warnings

### ArticleDigest

Represents the final summarized output.

Possible fields:

* title
* url
* source
* published_date
* extraction_status
* summary
* key_points
* warnings

---

## Why keep raw article text

Keeping extracted raw text in markdown may be useful later because it can:

* make debugging easier
* allow summary regeneration without refetching the page
* preserve a readable intermediate artifact
* support comparison across different summarization strategies

For this project, raw text should ideally mean **processed readable article text**, not raw HTML.

---

## Suggested future file layout

A possible future layout could be:

* `search.py` → find article candidates
* `extractor.py` → fetch page and extract usable article text
* `summarizer.py` → summarize extracted article text
* `writer.py` → save raw and digest outputs

This is only a future direction and does not need to be implemented now.

---

## Current decision

For now, the project will stay aligned with the original week4 scope.
We will continue using the simpler path where the `summarizer` skill evolves to do:

1. take article URL
2. fetch article page
3. extract usable text
4. summarize it

This keeps the current implementation manageable and appropriate for the assignment.

---

## When to revisit this plan

This future architecture becomes worth implementing when one or more of these happen:

* the summarizer becomes too large or hard to maintain
* raw extracted article text becomes important for debugging
* multiple summarization strategies need to be compared
* LLM integration is introduced
* agent orchestration needs clearer skill boundaries

Until then, this document should be treated as a reference, not a requirement.
