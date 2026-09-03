# Claude Code - Learning & Exploration

## Introduction

Claude Code is a powerful tool for integrating Claude AI with Python applications using the LangChain framework. Through exploration and hands-on practice, I've learned how to:

- **Initialize Claude LLM**: Set up ChatAnthropic with API key management using environment variables
- **Build Custom Tools**: Create reusable tools with the `@tool` decorator for file operations and package management
- **Work with Jupyter Notebooks**: Use interactive notebooks to test Claude integrations and build AI-powered workflows
- **Data Processing**: Generate and manipulate pandas DataFrames for data-driven applications
- **Agent-based Programming**: Understand how to bind tools to Claude models and enable agentic workflows

This repository documents my learning journey with Claude Code through practical examples and implementations.

## Setting Up with uv

**Note:** This project uses `uv` for Python dependency management — it's significantly faster than conda.

To get started:
- **Install dependencies:** `uv sync`
- **Add a new library:** `uv add package_name`
- **Run scripts:** `uv run python script.py`
- **Activate the environment:** `source .venv/bin/activate` (or use `uv run` to automatically use the virtual environment)

For more details, visit the [uv documentation](https://docs.astral.sh/uv/).

### Key Files

- `1_llm_call.ipynb` - Basic LLM interaction with ChatAnthropic
- `my_claudecode.ipynb` - Tool definitions for directory, file, and package operations
- `dataframe_example.py` - Pandas DataFrame creation example

---

![Claude Code Overview](./images/screenshots/Screenshot-1-Claude_code.png)

*Figure: Claude Code environment with LLM integrations and tool execution*
