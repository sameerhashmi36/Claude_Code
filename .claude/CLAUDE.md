# Claude Code - Project Standards & Instructions
## Overview

This project documents my learning journey integrating Claude AI with Python using LangChain. It focuses on clear code, reproducible notebooks, and safe handling of API keys.

---
## Project Purpose
- Learn to initialize and call Claude models (`ChatAnthropic`)
- Build custom tools using the `@tool` decorator
- Practice agent-based programming (binding tools to models)
- Experiment with data processing using pandas
- Keep a clean, readable record of progress
---
## Project Structure
- `notebooks/` - Jupyter notebooks for experiments
- `scripts/` - Standalone Python scripts
- `tools/` - Reusable `@tool` functions
- `images/` - Screenshots and figures for docs
- `requirements.txt` - Project dependencies
- Keep notebooks, scripts, and reusable code in separate folders
---
## Coding Standards
- Follow PEP 8 for style
- Use type hints for all functions, especially `@tool` functions
- Write clear docstrings (PEP 257) - for tools, this is what the LLM reads
- Use `snake_case` for functions and variables
- Catch specific exceptions only, never bare `except:`
- Prefer immutable/non-mutating operations where possible
---
## Claude & LangChain Practices
- Load `ANTHROPIC_API_KEY` from environment variables, never hardcode it
- Keep model settings (name, temperature, max_tokens) in one place
- Keep `@tool` functions small and single-purpose
- Test each tool on its own before binding it to the model
---
## Notebooks
- One clear purpose per notebook
- Use Markdown cells to explain reasoning, not just steps
- Clear large outputs before committing
- Move stable code out of notebooks into `tools/` or `scripts/`
---
## Dependency Management
- List dependencies in `requirements.txt`
- Pin versions for key packages (`langchain`, `langchain-anthropic`, `anthropic`, `pandas`)
- Use a virtual environment (`.venv`) for isolation
---
## Version Control
- Commit often with meaningful messages
- Never commit `.env` or API keys
- Keep the main branch stable
---
## Useful Resources
- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [LangChain Documentation](https://python.langchain.com/)
- [Anthropic API Documentation](https://docs.claude.com)
---
*A personal learning project - update this file as new patterns emerge.*
