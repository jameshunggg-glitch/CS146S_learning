# workflow.md

## Purpose
This document defines the step-by-step workflow for handling Week 6 Semgrep findings.

The goal is to ensure that each security issue is handled in a controlled, minimal, and verifiable way.

This workflow must be followed one finding at a time.

---

## Core Principle

For every finding:

- analyze first,
- propose the minimal safe fix,
- review before editing,
- implement only the agreed patch,
- verify the finding is resolved,
- confirm the app still runs and tests still pass,
- record evidence for the final write-up.

Do not skip steps.

---

## Standard Workflow Per Finding

### Step 1: Read the finding
Start by identifying:

- file path
- line(s)
- Semgrep rule name
- category/type of issue
- short risk summary

At this stage, do not modify code.

Output expected:
- plain-language explanation of what Semgrep found
- short explanation of why it is risky

---

### Step 2: Analyze root cause
Determine why the issue exists.

Focus on:
- what unsafe pattern is present,
- whether user-controlled input is involved,
- whether the issue is real or possibly noisy,
- how directly the flagged code contributes to the risk.

At this stage, still do not edit code.

Output expected:
- root cause explanation
- confidence level of the finding
- any ambiguity or behavior tradeoff worth noting

---

### Step 3: Propose the smallest safe remediation
Propose the smallest code change that addresses the root cause.

Requirements:
- keep behavior changes as small as possible,
- avoid unrelated cleanup,
- avoid broad refactors,
- avoid changing multiple findings at once,
- do not implement yet unless explicitly asked.

Output expected:
- minimal remediation plan
- exact file(s) to modify
- short explanation of why this fix is preferred

---

### Step 4: Review before editing
Before making any change, the proposed fix should be reviewed.

The reviewer should confirm:
- the fix addresses the actual root cause,
- the change is small and targeted,
- the patch is suitable for the assignment write-up,
- the risk of regression is acceptable.

If the fix is too broad, simplify it before editing.

---

### Step 5: Implement only the agreed patch
Once approved, apply the smallest agreed change.

Rules:
- do not refactor unrelated code,
- do not rename files or move code,
- do not add unnecessary dependencies,
- do not hide the warning without fixing the cause,
- do not bundle multiple fixes together unless explicitly requested.

Output expected:
- concise summary of what changed
- before/after explanation in plain language

---

### Step 6: Re-run Semgrep
After the code change, re-run Semgrep to confirm the targeted finding is resolved.

Preferred verification:
- re-run a scan on the project
- confirm the targeted finding no longer appears
- check whether any new findings were introduced

Output expected:
- whether the specific finding is resolved
- whether any new relevant finding appeared

---

### Step 7: Verify application stability
After resolving the finding, verify that the application still behaves correctly.

Check:
- app startup still works,
- relevant flows still work,
- tests still pass if available.

Output expected:
- brief verification summary
- mention of any limitation if full verification is not possible

---

### Step 8: Record evidence for write-up
For each completed fix, preserve the following information:

- file and line(s)
- Semgrep rule/category
- risk description
- root cause summary
- what changed
- why the fix mitigates the issue
- Semgrep verification result
- app/test verification result

This information should be sufficient to populate `writeup.md` later.

---

## Finding Triage Rules

When choosing which findings to fix first, prefer findings that are:

- high-confidence,
- clearly security-relevant,
- explainable in plain language,
- fixable with small targeted changes,
- easy to verify after the fix,
- suitable for final write-up documentation.

Lower-priority findings may be postponed if:
- the code intent is unclear,
- the safe fix is ambiguous,
- the change is likely to be larger or riskier.

---

## Escalation Rules

Pause and ask for review before proceeding if:

- the finding may be a false positive,
- the fix requires disabling or changing behavior significantly,
- multiple safe fix options exist,
- the minimal fix is not obvious,
- the change may affect other features,
- the issue cannot be verified easily.

---

## Non-Negotiable Constraints

Do not:

- skip analysis,
- edit before proposing a fix,
- fix more than one finding in a single step,
- perform broad code cleanup,
- introduce unrelated improvements,
- suppress a warning without justification,
- claim verification without actually describing how it was checked.

---

## Definition of Done Per Finding

A finding is considered done only when all of the following are true:

1. the issue was analyzed,
2. the minimal remediation plan was reviewed,
3. the agreed patch was implemented,
4. Semgrep confirms the targeted finding is resolved,
5. the app still runs,
6. tests still pass if available,
7. enough evidence is recorded for `writeup.md`.

---

## Preferred Working Style

Use this workflow in short cycles:

1. one finding,
2. one analysis,
3. one approved patch,
4. one verification pass,
5. one write-up record.

Repeat until at least 3 valid findings are fully resolved.
