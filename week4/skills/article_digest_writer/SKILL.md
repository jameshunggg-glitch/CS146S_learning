# Article Digest Writer

## Purpose

Take a structured list of article candidates, extract usable article content, generate summaries, and save each result as a Markdown file.

This skill is intended to convert article candidates into readable digest files.

---

## When to Use This Skill

Use this skill when:
- article candidates have already been collected
- the goal is to extract, summarize, and save results
- a consistent Markdown output format is required

Do not use this skill for:
- searching for new articles from scratch
- broad crawling
- generating marketing copy
- rewriting articles in a different tone

---

## Inputs

Expected inputs:
- a structured list of article candidates
- an output directory
- a fixed Markdown template

Each article candidate should ideally include:
- `title`
- `url`
- `source`
- `published_date`

---

## Expected Output

For each article, create one Markdown file.

Each Markdown file should contain:
- title
- source
- URL
- published date if available
- extraction status
- summary
- key points
- warnings or notes

---

## Workflow

1. Read the provided article candidate list.
2. Process each article one by one.
3. Attempt to extract usable article text and metadata.
4. Generate a concise summary.
5. Generate key points.
6. Record any warnings if extraction is partial or weak.
7. Save the result as a Markdown file using a consistent format.

---

## Markdown Structure

Use a structure similar to:

# {Article Title}

- Source: {Source Name}
- URL: {Article URL}
- Published Date: {Published Date or Unknown}
- Extraction Status: {Success / Partial / Failed}

## Summary
{summary}

## Key Points
- point 1
- point 2
- point 3

## Warnings
- warning 1
- warning 2

---

## Boundaries

This skill can:
- read provided article pages
- extract usable text
- summarize extracted content
- save Markdown files
- mark partial or failed extraction states

This skill cannot:
- search for unrelated new articles
- fabricate content that was not extracted
- bypass paywalls
- perform deep crawling
- silently discard failures

---

## Failure Handling

If article extraction fails:
- still record the article if metadata is available
- mark extraction status clearly
- include a warning describing the likely issue

Possible warning examples:
- extraction failed
- insufficient content
- paywall suspected
- published date unavailable

If summary quality is weak due to low text quality:
- say so explicitly
- do not pretend the summary is complete

---

## Quality Guidelines

Prefer:
- concise and readable summaries
- structured Markdown
- honest reporting
- consistency across files

Avoid:
- invented details
- overly long summaries
- inconsistent formatting
- missing warning states for failed extraction

---

## Completion Criteria

This skill is complete when:
- each usable article produces one Markdown file
- output structure is consistent
- failures are recorded honestly
- no fabricated content is introduced