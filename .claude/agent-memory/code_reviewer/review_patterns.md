---
name: recurring-code-review-patterns
description: Patterns and recurring issues discovered during code reviews in this project
metadata:
  type: feedback
---

## Recurring Code Quality Issues in This Project

### Pattern 1: Bare Exception Handlers
**Rule:** Project CLAUDE.md explicitly forbids bare `except Exception` or bare `except:`. Must catch specific exception types.

**Why:** Masks programming errors, catches unrecoverable exceptions (KeyboardInterrupt, SystemExit), makes debugging harder.

**How to apply:** When reviewing Python scripts, flag any `except Exception as e:` or bare `except:` clauses. Recommend specific exception types from the context (e.g., for pandas I/O: `ParserError`, `EmptyDataError`, `ValueError`, `IOError`).

---

### Pattern 2: Path Inconsistency Between Documentation and Code
**Rule:** Keep path references synchronized between docstrings, comments, and actual code. Discrepancies cause runtime failures.

**Why:** Users follow documentation, code runs from different paths. Mismatch (e.g., `fetchAPI` vs `fetch-api`) causes silent failures when paths don't exist.

**How to apply:** Cross-check hardcoded paths in code against docstring descriptions and comments. Flag mismatches as Critical severity.

---

### Pattern 3: Hardcoded Relative Paths Reduce Portability
**Rule:** Avoid hardcoding relative paths like `"./.claude/skills/data"`. Use environment variables or function parameters instead.

**Why:** Script breaks when run from different directories or is moved. Prevents reuse and makes deployment fragile.

**How to apply:** Flag hardcoded paths as Medium severity. Recommend environment variables (e.g., `os.getenv('DATA_PATH')`) or command-line arguments.

---

### Pattern 4: Missing Type Hints
**Rule:** Project CLAUDE.md requires type hints for all functions, especially for parameters and return types.

**Why:** Enables static type checking, improves IDE support, documents expected types for caller.

**How to apply:** Scan function definitions. Flag missing parameter types or return type hints (`-> ReturnType`). Include all functions, not just entry points.

---

### Pattern 5: Unused Imports
**Rule:** Remove unused imports (`import os` if never called).

**Why:** Code clutter, confuses readers, suggests incomplete refactoring.

**How to apply:** Flag as High severity when part of a pattern (bare exceptions + unused os suggest incomplete cleanup).

---

### Pattern 6: CSV Encoding Not Specified
**Rule:** Always specify encoding when reading CSV files. Default behavior varies and silently fails on non-UTF-8 files.

**Why:** Data loss or silent corruption when CSV has encoding other than system default (latin-1, cp1252, etc.).

**How to apply:** Flag `pd.read_csv(file)` without `encoding=` parameter. Recommend `encoding='utf-8'` or graceful fallback logic.

---

### Pattern 7: Empty Data Handling
**Rule:** Validate DataFrames are non-empty before processing. Document intended behavior for edge cases.

**Why:** Silent data loss when empty CSVs are written to parquet without warning.

**How to apply:** Flag when CSV/DataFrame is read but not validated. Recommend `if df.empty: ...` check or explicit documentation of why empty data is acceptable.

---

### Pattern 8: Folder Sorting by Name vs. Datetime
**Rule:** If selecting "latest" folder by datetime, parse timestamps explicitly rather than relying on lexicographic sort.

**Why:** Lexicographic sort works for ISO format by accident (`2026-09-07` sorts correctly), but breaks if naming changes or is inconsistent.

**How to apply:** For folder selection based on datetime: check if `max(folders, key=lambda x: x.name)` is used. Recommend parsing actual datetimes.

---

### Pattern 9: Missing Output Validation
**Rule:** After writing files, validate output (existence, size, row count if applicable).

**Why:** Corrupted or incomplete files may silently pass if only exception handling is present.

**How to apply:** Flag when `.to_parquet()` or similar writes are not followed by validation. Recommend `assert file.exists()` or verify row counts match.

---

### Pattern 10: Print Statements vs. Logging
**Rule:** Production scripts should use Python's `logging` module, not `print()`.

**Why:** Enables audit trails, log levels, file persistence, and proper error handling.

**How to apply:** Flag heavy use of `print()` in scripts. Recommend `logging.basicConfig()` and `logger.info()` / `logger.error()`.

---

## Applied to convert_to_parquet.py Review
This script exhibited patterns 1, 2, 3, 4, 5, 6, 7, 8, 9, and 10 — all identified issues.
