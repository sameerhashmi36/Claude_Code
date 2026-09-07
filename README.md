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

![Claude Code Overview](./images/screenshots/Screenshot-1-Claude_code.png)

*Figure: Claude Code environment with LLM integrations and tool execution*


---

### 1. Agent-Driven Project Automation
Created `my_claudecode.ipynb` to demonstrate practical agent automation. Built a ReAct agent using LangGraph that binds three custom tools:
- **create_directory**: Creates directories programmatically
- **create_file**: Writes Python code to files
- **install_package**: Installs Python packages via pip

Following the project standards defined in `CLAUDE.md`, the agent orchestrated these tools to create `my_project/dataframe.py` — a well-structured pandas DataFrame generator with 3 columns and 5 rows, automatically installing dependencies as needed. The generated code adheres to PEP 8 standards, uses clear variable naming (`snake_case`), and includes type hints and docstrings as specified in the project's coding guidelines.

### 2. API Data Fetching & Logging
Implemented the **fetch-api skill** to handle external data integration:
- Fetches CSV data from remote GitHub repositories using async httpx
- Automatically creates timestamped directories (`YYYY-MM-DD_HH-MM-SS` format) in `.claude/skills/fetch-api/data/`
- Stores fetched data as CSV files for downstream processing
- Generates detailed logs in `.claude/skills/fetch-api/logs/` tracking API calls, success/failure status, and error details

### 3. Data Migration Using Claude Skills

Implemented the **migrate skill** to convert and manage data formats:
- Automatically locates the latest timestamped folder in `.claude/skills/fetch-api/data/`
- Converts CSV files to Parquet format using pandas and PyArrow for improved compression and query performance
- Creates organized output in `.claude/skills/migrate/data/` maintaining the same folder structure


![Claude code with skills](./images/screenshots/Screenshot-2-SKILLS-migration.png)

*Figure: Extension of Claude Code with skills (data migration)*

---

### 4. Automated Code Review Using Subagents & Agent Memory

**What are Subagents?**
Subagents are specialized AI helpers that work independently on specific tasks. Instead of Claude doing everything at once, you can create multiple subagents that work in parallel (at the same time) to complete different parts of a job faster.

**Why Use Subagents?**
- **Speed**: Multiple subagents work simultaneously instead of one-by-one
- **Focus**: Each subagent specializes in one type of task (like code review)
- **Efficiency**: Keeps the main conversation organized and less cluttered

**What is Agent Memory?**
Agent Memory lets Claude remember important information across different conversations. It's like a notebook where Claude writes down:
- What you're working on and your goals
- Patterns and rules you've established ("always do X this way")
- Project context and technical decisions
- External resources and where to find information

This way, Claude doesn't forget your preferences or project details between conversations.

**What I Did:**
I set up two code-reviewer subagents to review Python scripts in `.claude/skills/` directory:
- **Script 1** (`convert_to_parquet.py`): Converts CSV files to Parquet format
- **Script 2** (`kpi_analysis.py`): Creates sales analysis visualizations

Each subagent independently reviewed its script against project standards (from `CLAUDE.md`) and checked for issues like missing type hints, error handling problems, hardcoded values, and code duplication. Both subagents ran in parallel and completed within 2-3 minutes, flagging 20+ issues. The subagents also saved findings to agent memory so future reviews can learn from these patterns.

**Results:**
- 1 Critical + 7 High-severity issues in `convert_to_parquet.py`
- 5 Critical + 7 Major issues in `kpi_analysis.py`
- Both scripts need refactoring to meet project standards
- Memory updated with "standards compliance gaps" and "data script patterns" for future guidance

---


### 5. Data Pipeline Orchestration (2026-09-07):
Orchestrated an end-to-end data pipeline combining fetch-api and migrate skills:

1. **Fetch Phase**: Fetched CSV data from remote GitHub repositories using async httpx
   - Source URLs:
     - `dim_customer.csv` (3.7 KB, 40 rows)
     - `fact_sales.csv` (328 KB, 7173 rows)
   - Data saved to: `.claude/skills/fetch-api/data/2026-09-07_18-47-48/`
   - Logs created: `.claude/skills/fetch-api/logs/2026-09-07_18-47-48/fetchAPI.log`

2. **Migration Phase**: Converted CSV files to Parquet format
   - `dim_customer.csv` → `dim_customer.parquet` (40 rows, 7.32 KB)
   - `fact_sales.csv` → `fact_sales.parquet` (7173 rows, 140.16 KB)
   - Parquet files saved to: `.claude/skills/migrate/data/2026-09-07_18-47-48/`

3. **Pipeline Features**:
   - Asynchronous API calls for efficient data fetching
   - Timestamped folder organization (YYYY-MM-DD_HH-MM-SS format)
   - Comprehensive logging with API call status and conversion metrics
   - Automatic detection of latest fetch folder for migration
   - Error handling and detailed reporting for each step

---