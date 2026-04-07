# Topic News Search

## Purpose

Search for the latest or top-result `n` news articles for a user-provided topic and return a structured candidate list.

This skill is intended to be reusable across different topics, not only AI news.

Examples:
- AI news
- semiconductor news
- Taiwan tech news
- shipping news

---

## When to Use This Skill

Use this skill when the task requires:
- finding recent news articles on a topic
- collecting top search-returned articles
- preparing article candidates for downstream summarization

Do not use this skill for:
- summarizing full article content
- writing Markdown output files
- broad web crawling
- popularity ranking based on social metrics

---

## Inputs

Expected inputs:
- `topic`: a user-provided topic string
- `n`: the desired number of articles

Example:
- topic = `AI news`
- n = `5`

---

## Expected Output

Return a structured list of article candidates.

Each candidate should include, when available:
- `title`
- `url`
- `source`
- `published_date`
- `status`
- optional short note about relevance

If fewer than `n` usable results are found, return the available results and clearly say so.

---

## Workflow

1. Read the requested topic and target count `n`.
2. Search for recent or top-result news articles related to the topic.
3. Prefer results that appear to be legitimate news or article pages.
4. Avoid obvious duplicates where possible.
5. Return the top usable candidates in a structured list.

---

## Boundaries

This skill can:
- search for topic-related articles
- collect candidate links
- return article metadata

This skill cannot:
- summarize full article text
- save Markdown files
- fabricate URLs
- bypass paywalls or logins
- crawl large portions of websites

---

## Failure Handling

If search quality is poor:
- still return the best available candidates
- clearly indicate limitations

If fewer than `n` valid results are found:
- return fewer than `n`
- explain that the requested number could not be fully satisfied

If duplicates appear:
- prefer distinct sources when possible
- but do not force low-quality substitutions just to increase count

---

## Quality Guidelines

Prefer:
- recent results
- clear article pages
- recognizable sources
- structured outputs

Avoid:
- low-information landing pages
- obvious category pages
- broken links
- fabricated metadata

---

## Completion Criteria

This skill is complete when it returns:
- a structured list of article candidates
- up to `n` usable results
- clear reporting if any limitation occurred