# CLAUDE.md

## Purpose
This repository is for a Week 6 security assignment focused on scanning and fixing vulnerabilities with Semgrep.

The goal is not to build new features or refactor the application.
The goal is to:
1. triage Semgrep findings,
2. fix at least 3 real security issues,
3. keep changes minimal and targeted,
4. verify the app still runs and tests still pass,
5. preserve enough evidence for the final write-up.

---

## High-Level Rules

- Do not treat this as a feature development project.
- Do not refactor unrelated code.
- Do not improve style, architecture, naming, or structure unless strictly required for the security fix.
- Do not change behavior beyond what is necessary to mitigate the specific finding.
- Prefer the smallest safe patch that addresses the root cause.
- Handle one finding at a time.
- Before making code changes, first explain the issue and propose the minimal fix.
- After each fix, explain how to verify the finding is resolved and confirm no obvious regressions were introduced.

---

## Required Workflow For Every Finding

For each Semgrep finding, follow this sequence:

1. **Understand the finding**
   - Identify the file, line(s), Semgrep rule, and risk category.
   - Explain the root cause in plain language.

2. **Propose a minimal remediation plan**
   - Describe the smallest safe code change that resolves the issue.
   - List exactly which file(s) need to be modified.
   - Do not edit yet unless explicitly asked.

3. **Apply the fix**
   - Make only the agreed minimal change.
   - Avoid unrelated cleanup.

4. **Verification**
   - Describe how to re-run Semgrep for the affected code.
   - Describe how to verify the app still runs and tests still pass.
   - Summarize what changed in before/after terms.

5. **Write-up support**
   - For each fix, preserve:
     - file and line(s),
     - Semgrep rule/category,
     - short risk description,
     - summary of the code change,
     - why the fix mitigates the issue.

---

## Change Constraints

When editing code:

- Prefer explicit, readable, and conventional secure patterns.
- Do not silently suppress warnings unless there is a clear justification.
- Do not add unnecessary dependencies unless required for a legitimate fix.
- Do not remove functionality unless the assignment clearly benefits from disabling an unsafe behavior.
- If a fix requires a behavior tradeoff, explain it clearly before implementing.

---

## What To Avoid

Do **not**:

- perform broad rewrites,
- rename files or move folders,
- add unrelated tests,
- rewrite whole modules to eliminate a small finding,
- “fix” issues by hiding them instead of addressing the cause,
- modify multiple findings in one step unless explicitly instructed.

---

## Collaboration Style

When asked to work on a finding:

- Start by analyzing, not editing.
- Be concise and specific.
- Show the root cause clearly.
- Recommend the most practical minimal fix.
- Point out any ambiguity or possible regression risk.
- Wait for confirmation before making larger or riskier changes.

---

## Assignment Context

The assignment expects:
- Semgrep-based security triage,
- at least 3 fixes,
- precise edits,
- explanation of mitigation,
- confirmation that the app still runs and tests still pass.

All changes should support the final `writeup.md`.

---

## Preferred Outcome

A successful contribution should:
- resolve one clearly identified Semgrep finding,
- use a minimal and defensible patch,
- be easy to explain in the final report,
- avoid introducing unrelated changes,
- preserve application stability.
