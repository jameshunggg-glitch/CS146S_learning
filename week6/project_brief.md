# project_brief.md

## Project
Week 6 assignment: Scan and fix vulnerabilities with Semgrep.

## Objective
Use Semgrep to scan the provided application, triage the findings, and fix at least 3 real security issues with minimal, targeted changes.

This is not a feature development project.
This is a security remediation assignment.

## Assignment Requirements
The project must satisfy the following requirements:

1. Run Semgrep against the provided app.
2. Review and triage the findings.
3. Fix at least 3 issues identified by Semgrep.
4. Keep edits precise and minimal.
5. Ensure the app still runs after the fixes.
6. Ensure tests still pass after the fixes.
7. Document the findings and fixes in `writeup.md`.

## Scope of Scanning
Semgrep findings may come from:

- `backend/` (FastAPI / Python)
- `frontend/` (JavaScript)
- `requirements.txt` (dependency issues)
- repo-level config or environment-related files

## Current Scan Status
Semgrep scan has already been run locally.

Current findings identified:

1. `backend/app/main.py`
   - Rule: `python.fastapi.security.wildcard-cors.wildcard-cors`
   - Issue: CORS allows any origin using `allow_origins=["*"]`

2. `backend/app/routers/notes.py`
   - Rule: `python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text`
   - Issue: raw SQL built with f-string and `sqlalchemy.text(...)`, creating SQL injection risk

3. `backend/app/routers/notes.py`
   - Rule: `python.lang.security.audit.eval-detected.eval-detected`
   - Issue: use of `eval()` on dynamic input

4. `backend/app/routers/notes.py`
   - Rule: `python.lang.security.audit.subprocess-shell-true.subprocess-shell-true`
   - Issue: `subprocess.run(..., shell=True, ...)`

5. `backend/app/routers/notes.py`
   - Rule: `python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected`
   - Issue: dynamic URL used with `urlopen(...)`

## Current Remediation Priority
The current preferred first-pass fixes are:

1. wildcard CORS
2. SQL injection risk from raw SQL + f-string
3. eval usage

These three are currently preferred because they are:
- high-confidence security findings,
- relatively clear to explain,
- suitable for minimal targeted fixes,
- likely easier to document in the final write-up.

The other two findings remain valid candidates, but are currently lower priority until code intent is reviewed more carefully.

## Working Strategy
The work should be done one finding at a time.

For each finding:

1. analyze the root cause,
2. propose the smallest safe fix,
3. wait for review before editing,
4. implement only the agreed patch,
5. re-run Semgrep,
6. verify app/tests still work,
7. record before/after notes for `writeup.md`.

## Deliverables
The final submission should include:

### 1. Findings overview
A short summary of:
- SAST findings
- secrets findings if any
- dependency/SCA findings if any
- false positives or ignored noisy rules, if applicable

### 2. Three documented fixes
For each fix, record:
- file and line(s)
- Semgrep rule/category
- brief risk description
- what was changed
- why the fix mitigates the issue

## Constraints
- No broad refactors
- No unrelated cleanup
- No unnecessary dependency changes
- No behavior changes beyond what is needed to fix the issue
- No fixing multiple findings in one step unless explicitly requested

## Success Criteria
The project is successful if:

- at least 3 real findings are fixed,
- the fixes are minimal and defensible,
- Semgrep confirms the targeted findings are resolved,
- the app still runs,
- tests still pass,
- `writeup.md` can be completed directly from the recorded evidence.
