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

### 6. Airflow Project Documentation (2026-09-15):

Created a comprehensive **Apache Airflow project** demonstrating asset-based scheduling with producer and consumer DAGs. Claude assisted in generating the `./airflow_project/README.md` by:

1. **Analyzing DAG Structure**: Examined `data_fetch.py` and `data_report.py` to understand task dependencies and asset outlets
2. **Documenting Concepts**: Provided clear explanations of Airflow fundamentals (DAGs, tasks, operators, executors, assets)
3. **Creating Workflow Diagrams**: Generated ASCII visualizations of task dependencies and data flow
4. **Setup Instructions**: Wrote step-by-step installation and execution guides with code examples
5. **Asset-Based Scheduling**: Documented modern scheduling patterns using data availability instead of cron schedules

**Key Documentation Elements**:
- Overview of Apache Airflow concepts and architecture
- Detailed task breakdown for `data_fetch` (producer) and `data_report` (consumer) DAGs
- Complete setup, installation, and running instructions
- Asset-based scheduling benefits and best practices
- File locations and project structure

This approach ensures anyone reading the airflow_project README can understand the entire workflow, from DAG design to execution.

---

## Using the `/btw` Command

**What is `/btw`?**

`/btw` (short for "by the way") is a Claude Code command that allows you to ask **side questions or tangential topics** without interrupting your main workflow. Instead of breaking context or starting a new conversation, you can ask Claude about related topics in the same session.

**Purpose**:
- Ask clarifying questions about concepts you encounter
- Get quick explanations on tangential topics
- Maintain conversation flow while exploring related ideas
- Keep your main task's context intact

**How to Use**:

In Claude Code, type `/btw` followed by your side question:

```
/btw What's the difference between asset-based scheduling and time-based scheduling in Airflow?
```

Claude will answer your side question while keeping track of your main task context, so you can smoothly return to what you were working on.

**Example Workflow**:
```
Main task: Writing Airflow documentation
↓
You ask: /btw Can you explain what outlets mean in Airflow?
↓
Claude answers your side question
↓
You continue: Can we add that explanation to the README?
```

This keeps conversations organized, reduces context-switching, and makes it easier to learn as you build.

---

## Scheduling with Claude Code

**What is Claude Code Scheduling?**

Claude Code provides powerful scheduling capabilities through two complementary features:

1. **`/loop` Command**: Run a prompt repeatedly on a fixed interval or dynamically based on events
   - Fixed-interval mode: `1m /your-prompt` runs every minute
   - Dynamic mode: `/loop /your-prompt` (no interval) lets Claude self-pace based on task progress
   
2. **CronCreate**: Schedule tasks using standard 5-field cron expressions for precise timing
   - Example: `"0 9 * * *"` runs at 9am daily (local timezone)
   - Automatically fired by the scheduler; tasks expire after 7 days

**How to Use Scheduling**

### Fixed-Interval Loops
```
/loop 5m /code-review --check branch
```
This runs `/code-review --check branch` every 5 minutes. The loop continues until you stop it manually.

### Dynamic Self-Pacing Loops
```
/loop check the deploy
```
Claude self-paces iterations — deciding when to check next based on what changed (e.g., if a deploy is in progress, it checks more frequently; when idle, it waits longer).

### One-Shot Reminders
Schedule a task for a specific time using the CronCreate tool directly:
- `0 14 * * *` = 2:00 PM every day
- `30 8 * * 1-5` = 8:30 AM on weekdays (Monday-Friday)

**How to Stop a Cron Job**

When you schedule a task with `/loop` or CronCreate, you get a **job ID**. To cancel it:

```
/cron delete <job_id>
```

Or use the CronDelete tool with the job ID returned when the task was created.

**Example Output**:
```
Scheduled recurring job 43b4383a (Every minute). 
Session-only (not written to disk, dies when Claude exits). 
Auto-expires after 7 days. 
Use CronDelete to cancel sooner.
```

To stop job `43b4383a`, call: `CronDelete(job_id="43b4383a")`

**Important Notes**:
- Jobs are **session-only** — they disappear when Claude exits (no persistent storage)
- Recurring tasks **auto-expire after 7 days** (this is a safety feature)
- The scheduler adds small jitter (up to 10% of the period late) to avoid thundering herd at :00/:30
- Jobs only fire when the REPL is idle, not during active prompts

---