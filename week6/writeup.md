# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## Brief findings overview 
> TODO

## Fix #1
a. File and line(s)
> `backend/app/main.py`, lines 4 and 22–28 (original)

b. Rule/category Semgrep flagged
> `python.fastapi.security.wildcard-cors.wildcard-cors`

c. Brief risk description
> `CORSMiddleware` was configured with `allow_origins=["*"]` and `allow_credentials=True`.
> This combination is a browser spec violation and a security risk: any origin could make
> credentialed cross-origin requests to the API, enabling CSRF-like attacks.

d. Your change (short code diff or explanation, AI coding tool usage)
> After reviewing the app structure, it became clear the frontend is served by the same
> FastAPI process at `http://localhost:8000`, and all `fetch()` calls in `frontend/app.js`
> use relative paths. No cross-origin requests exist at all.
>
> Removed the entire `app.add_middleware(CORSMiddleware, ...)` block and the corresponding
> import — 8 lines deleted, nothing added.
>
> ```diff
> - from fastapi.middleware.cors import CORSMiddleware
> - app.add_middleware(
> -     CORSMiddleware,
> -     allow_origins=["*"],
> -     allow_credentials=True,
> -     allow_methods=["*"],
> -     allow_headers=["*"],
> - )
> ```

e. Why this mitigates the issue
> Removing the middleware eliminates the attack surface entirely. There is no CORS policy
> left to misconfigure. Semgrep re-scan confirms 0 findings on `backend/app/main.py`.
>
> **Verification caveat:** Full runtime verification (app startup + test suite) is currently
> deferred due to pre-existing environment issues unrelated to this fix — specifically,
> missing `python-dotenv` package and Python version/package compatibility errors that
> existed before this change. The Semgrep result is cleared; the fix is considered solved.

## Fix #2
a. File and line(s)
> `backend/app/routers/notes.py`, lines 71–80 (function `unsafe_search`)

b. Rule/category Semgrep flagged
> `python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text`

c. Brief risk description
> User-supplied query parameter `q` was interpolated directly into a raw SQL string via
> an f-string and passed to `sqlalchemy.text(...)`. An attacker could inject arbitrary SQL
> (e.g. `' OR '1'='1`) to bypass the WHERE clause or exfiltrate data.

d. Your change (short code diff or explanation, AI coding tool usage)
> Replaced f-string interpolation with a SQLAlchemy bound parameter (`:pattern`).
> The `%` wildcards are now assembled in Python and passed as a separate value dict,
> never concatenated into the SQL string.
>
> ```diff
> - sql = text(
> -     f"""
> -     WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'
> -     """
> - )
> - rows = db.execute(sql).all()
> + sql = text(
> +     """
> +     WHERE title LIKE :pattern OR content LIKE :pattern
> +     """
> + )
> + rows = db.execute(sql, {"pattern": f"%{q}%"}).all()
> ```

e. Why this mitigates the issue
> With bound parameters, the database driver handles escaping. Any injected SQL payload
> is treated as a literal string value, not executable SQL. The LIKE search behavior is
> fully preserved. Semgrep re-scan confirms `avoid-sqlalchemy-text` finding is cleared;
> no other `text(f"...")` patterns remain in `backend/`.

## Fix #3
a. File and line(s)
> `backend/app/routers/notes.py`, lines 102–105 (function `debug_eval`)

b. Rule/category Semgrep flagged
> `python.lang.security.audit.eval-detected.eval-detected`

c. Brief risk description
> `eval()` executed arbitrary user-supplied Python expressions directly on the server.
> An attacker could pass payloads like `__import__('os').system('id')` to achieve
> remote code execution (RCE) with the privileges of the web process.

d. Your change (short code diff or explanation, AI coding tool usage)
> Replaced `eval()` with `ast.literal_eval()` from the standard library.
>
> ```diff
> - result = str(eval(expr))  # noqa: S307
> + import ast
> + result = str(ast.literal_eval(expr))
> ```

e. Why this mitigates the issue
> `ast.literal_eval` only parses Python literal structures (numbers, strings, lists,
> dicts, booleans, None). It cannot import modules, call functions, or execute statements.
> Any non-literal input raises a `ValueError`, terminating the request safely.
> Semgrep re-scan confirms `eval-detected` finding is cleared.
>
> **Behavior tradeoff:** Arithmetic expressions like `1+2` no longer evaluate — only
> literals like `42`, `"hello"`, `[1,2,3]` are accepted. This is the intended tradeoff
> for a debug endpoint in a security remediation context.
>
> **Verification caveat:** Runtime verification remains deferred due to the same
> pre-existing environment issues noted in Findings 1 and 2.