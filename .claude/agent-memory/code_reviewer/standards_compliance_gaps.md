---
name: standards-compliance-gaps
description: This project has persistent gaps between CLAUDE.md requirements and actual code (missing type hints, error handling, docstrings). Track patterns to prioritize in reviews.
metadata:
  type: feedback
---

## Pattern: Systematic Non-Compliance with Project Standards

**Rule:** Prioritize type hints, comprehensive docstrings (PEP 257), and error handling as blocking issues in code reviews for this project. They are explicitly required by CLAUDE.md but consistently absent.

**Why:** The project has clear coding standards documented, but scripts in-the-wild don't follow them. The `kpi_analysis.py` review revealed:
- Zero type hints on 6+ functions (all functions)
- Zero try-except blocks (all file I/O unprotected)
- Incomplete docstrings (one-liners instead of PEP 257 format with parameters/returns/raises)

These aren't style nitpicks—they're violations of explicit project governance.

**How to apply:** 
- When reviewing code from this project, treat missing type hints as a CRITICAL blocker (project requirement)
- Treat bare file I/O without error handling as CRITICAL
- Treat docstrings that don't include parameter/return/raises sections as MAJOR (not minor)
- Don't accept "style review only" — enforce standards compliance as part of review

This differs from typical Python projects where these are nice-to-have; here they are must-have.
