---
name: data-script-patterns
description: Common anti-patterns in data analysis/visualization scripts (hardcoded paths, non-reproducibility, repeated code, fragile dimension logic).
metadata:
  type: feedback
---

## Pattern: Data Script Anti-Patterns

**Rule:** In data analysis/visualization scripts (pandas, matplotlib), watch for:
1. Hardcoded file paths with timestamps (breaks portability)
2. Missing np.random.seed() → non-reproducible results
3. Fragile dimension logic (assumptions about min/max values)
4. Repeated visualization code blocks (extract into helpers)
5. No input validation or schema checks
6. Magic numbers for figure sizes, DPI, font sizes

**Why:** The `kpi_analysis.py` review found all 6 patterns. These are systematic issues in data scripts that break reusability, reproducibility, and maintainability. The hardcoded path with timestamp is especially problematic—makes the script a one-time-use tool instead of a reusable script.

**How to apply:**
- Paths should be configurable via environment variables or CLI args
- Always add `np.random.seed(SEED)` at module start if randomness is used
- Add a `validate_data()` function that checks required columns exist
- For repeated viz patterns, suggest refactoring into `create_chart_helper()` type functions
- Extract config (figsize, dpi, colors) into constants at top of file
- Date/dimension logic should include comments explaining assumptions (or add assertions)

This is specific to data analysis scripts; general Python code has different patterns.
