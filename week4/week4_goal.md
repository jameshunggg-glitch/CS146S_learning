# Week 4 Project Blueprint — AI News Digest System

## 1. Project Overview

This project is a small, skills-oriented workflow system for collecting and summarizing news articles.

The user provides:
- a topic, such as `AI news`
- a target number of articles, such as `5`

The system then:
1. searches for the latest or top search-result articles related to the topic
2. selects the top `n` results
3. extracts article information and usable text
4. generates a structured summary for each article
5. saves the results into Markdown files

This project is designed as a **Week 4 engineering practice project**, with the focus on:
- reusable skills
- workflow boundaries
- structured outputs
- repeatable execution
- documentation and validation

---

## 2. Project Goal

Build a small system that can:

- search for the latest or top `n` news articles on a user-provided topic
- summarize each article in a consistent format
- save each article summary as a Markdown file
- use clearly separated skills for searching and summarization

This is **not** a general-purpose crawler or large-scale news platform.  
It is a small, controlled workflow project meant to practice engineering with AI skills.

---

## 3. Version 1 Scope

### Included in Version 1
- Topic-based news search
- User-defined article count `n`
- Select latest `n` articles or top `n` returned search results
- Extract basic article metadata when available
- Generate article summaries
- Save outputs as Markdown files
- Clear handling for failed extraction cases

### Excluded from Version 1
- Popularity scoring based on social metrics
- OCR/image input
- Reverse search from screenshots
- Multi-language translation workflow
- Full website crawling
- Paywall bypass
- Automatic posting to social media or blogs
- Rewriting articles into marketing copy

---

## 4. Skills Design

## Skill A — Topic News Search

### Purpose
Search for the latest `n` or top-result `n` articles for a given topic and return a structured candidate list.

### Inputs
- `topic`: string  
  Example: `AI news`, `semiconductor news`, `Taiwan tech news`
- `n`: integer  
  Example: `5`

### Responsibilities
- Search for articles related to the topic
- Prefer the latest results or top search-returned results
- Return a structured list of candidate articles
- Include basic metadata if available

### Expected Output
A structured list of article candidates, such as:
- title
- url
- source
- published date (if available)
- short relevance note (optional)

### Boundaries
This skill **can**:
- search for news articles
- select top `n` candidates
- return URLs and metadata

This skill **cannot**:
- summarize full article content
- save Markdown files
- fabricate missing URLs
- bypass paywalls or logins
- crawl an entire website

### Failure Handling
If fewer than `n` usable results are found:
- return the available results
- clearly report that fewer than `n` valid articles were found

---

## Skill B — Article Digest Writer

### Purpose
Take article URLs from Skill A, extract usable content, summarize each article, and save the result as a Markdown file.

### Inputs
- structured article list from Skill A
- output directory path
- summary format specification

### Responsibilities
- open each article
- extract usable article information
- generate a concise summary
- generate key points
- record warnings if content is incomplete
- save each result as a Markdown file

### Expected Output
For each article:
- one Markdown file with a consistent structure

### Boundaries
This skill **can**:
- read article pages
- extract usable content
- summarize the article
- save Markdown files
- mark warnings or extraction limits

This skill **cannot**:
- search for new articles outside the provided list
- invent article text that could not be extracted
- bypass paywalls
- perform deep site crawling
- rewrite into ads/marketing copy in Version 1

### Failure Handling
If an article cannot be fully extracted:
- still save a result if basic metadata is available
- mark the file with a clear warning
- state whether the issue was likely:
  - paywall
  - login required
  - extraction failure
  - insufficient content

---

## 5. Workflow Design

### End-to-End Flow
1. User provides a topic and `n`
2. Skill A searches and returns latest/top `n` article candidates
3. Skill B processes each candidate
4. Skill B generates summaries and saves Markdown files
5. System reports:
   - how many articles were requested
   - how many were found
   - how many were successfully summarized
   - which ones failed and why

---

## 6. Output File Design

Each article should be saved as one Markdown file.

Suggested file naming:
- `001_article_title_slug.md`
- `002_article_title_slug.md`

### Markdown Template
```md
# {Article Title}

- Source: {Source Name}
- URL: {Article URL}
- Published Date: {Published Date or Unknown}
- Extraction Status: {Success / Partial / Failed}

## Summary
{2 to 5 paragraph summary or concise summary block}

## Key Points
- Point 1
- Point 2
- Point 3

## Extracted Text Notes
{Short note about extracted content quality}

## Warnings
- Paywall suspected
- Content incomplete
- Published date unavailable
```

---

## 7. Guardrails and Boundaries

### General Project Guardrails
The workflow should:
- prefer clarity over aggressive automation
- report uncertainty honestly
- avoid fabricating content
- treat extraction failure as a valid result state

### Safety / Reliability Rules
The workflow must:
- not invent article content
- not claim a page was read if it was not successfully read
- not bypass paywalls or login gates
- not silently skip failed articles without reporting them

### Engineering Boundaries
The workflow should:
- work on a small number of articles
- avoid large-scale crawling
- keep processing deterministic and inspectable
- save outputs in a fixed structure for later review

---

## 8. Validation and Testing Plan

### Functional Checks
- Can the system accept a topic and `n`?
- Can Skill A return article candidates?
- Can Skill B produce Markdown files?
- Are failed articles clearly marked?

### Output Quality Checks
- Does every successful file contain:
  - title
  - source
  - URL
  - summary
  - key points
- Is the Markdown format consistent?
- Are warnings shown when extraction is incomplete?

### Failure Scenario Checks
Test cases should include:
- an article page with incomplete extraction
- an invalid or broken URL
- fewer than `n` valid search results
- duplicate or near-duplicate search results

### Example Acceptance Criteria
Version 1 is acceptable if:
- a user can request `n=5` articles on a topic
- the system can return and process available results
- Markdown files are generated consistently
- failed cases are reported honestly
- the workflow can be repeated with another topic

---

## 9. Why This Project Fits Week 4

This project is suitable for Week 4 because it practices:
- reusable workflow design
- skill boundaries
- structured outputs
- documentation-first engineering
- testable automation
- controlled project scope

It is a good training project because it is:
- small enough to finish
- practical enough to reuse later
- extensible for future versions

---

## 10. Possible Future Extensions

After Version 1, the project could be extended with:
- image input / OCR workflow
- screenshot-to-article recovery
- topic clustering across multiple articles
- comparison summaries across sources
- sentiment or stance tagging
- social post / newsletter generation
- Markdown index page generation
- MCP tool integration for custom search or storage

---

## 11. Recommended Initial Repo Structure

```text
week4/
├── app/
│   ├── main.py
│   ├── search.py
│   ├── summarizer.py
│   ├── writer.py
│   └── models.py
├── skills/
│   ├── topic-news-search/
│   │   └── SKILL.md
│   └── article-digest-writer/
│       └── SKILL.md
├── outputs/
├── tests/
│   ├── test_search.py
│   ├── test_summarizer.py
│   └── test_writer.py
├── CLAUDE.md
├── README.md
└── week4_project_blueprint.md
```

---

## 12. Final Version 1 Definition

**Project Name:** AI News Digest System

**Version 1 Goal:**  
Given a topic and a number `n`, search for the latest or top-result `n` news articles, summarize them, and save the results as structured Markdown files using two clearly separated skills.

**Core Skills:**  
- Skill A: Topic News Search  
- Skill B: Article Digest Writer

This defines a clean, realistic, and manageable first version for Week 4.
