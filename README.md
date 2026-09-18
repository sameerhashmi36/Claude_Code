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

## What is Cursor?

**Cursor** is a purpose-built AI code editor that integrates Claude directly into your development workflow. It's designed specifically for coding tasks and provides:

- **Real-time AI assistance** — get instant code suggestions, refactorings, and debugging help as you type
- **Tab autocomplete** — AI-powered code completion that understands your project context
- **Command palette** — quick access to AI actions like "Fix this," "Explain," "Generate tests," etc.
- **Codebase awareness** — Claude understands your entire project and can reference files and patterns you're using
- **Diff review** — AI helps review changes before you commit them
- **Built-in chat** — side panel for longer conversations while you code

### How Cursor Works

Cursor acts as a bridge between Claude and your code editor:

1. **Context-aware**: It sends your open files, selection, and project structure to Claude
2. **Bidirectional**: Claude can read your code and write changes back directly to files
3. **IDE features**: Full IDE integration including debugging, git support, and extensions
4. **Multiple models**: Choose between Claude models, GPT-4, or other LLMs

### Key Features

- **@mention files**: Reference specific files with `@filename` in chat — Claude reads the full content
- **CMD/CTRL K**: Open the quick edit dialog to refactor or generate code
- **CMD/CTRL L**: Open the code edit mode for multi-file refactoring
- **Indexed codebase search**: Find functions, classes, and patterns across your project
- **Terminal integration**: Run commands and see output directly in the editor
- **Agent mode**: Let Claude autonomously write, test, and iterate on code

### Cursor vs Claude Code

| Feature | Cursor | Claude Code |
|---------|--------|-------------|
| **Purpose** | AI-first code editor | AI assistant for terminal/CLI |
| **UI** | Full IDE (VS Code-based) | Terminal-based REPL |
| **Real-time editing** | Yes (as you type) | No (you run commands) |
| **Codebase indexing** | Yes (fast @mentions) | Via grep/search agents |
| **Git integration** | Native (diff, staging) | Via Bash commands |
| **Best for** | Daily coding, refactoring, pair programming | Scripting, automation, server work |

**Cursor link**: [cursor.com](https://cursor.com)

---

## MCP Servers in Claude Code

**MCP** (Model Context Protocol) is a framework that lets Claude interact with external systems — databases, APIs, file systems, dev tools — by connecting to specialized servers that expose capabilities as **tools**.

### What are MCP Servers?

MCP servers are lightweight programs that:
- Expose **resources** (files, data sources Claude can read)
- Expose **tools** (functions Claude can call to perform actions)
- Run locally (on your machine) or remotely (via HTTP/SSE)
- Connect to Claude Code, Claude Desktop, or the Claude API

Think of them as **plugins that extend Claude's abilities** beyond just text. Instead of manually copying output, Claude can directly interact with:
- Your Git repository
- Databases
- APIs (GitHub, Slack, weather, etc.)
- Web browsers (screenshot pages, fill forms)
- File systems (index large codebases)

### How MCP Works - Visual Flow

```
Your Terminal (Claude Code)
         ↓
    [You ask Claude a question]
         ↓
  Claude Code detects you need external tools
         ↓
  Sends request to MCP Server(s)
         ↓
MCP Server talks to the actual service
  (Git repo, Database, API, Playwright, etc.)
         ↓
  Server returns results to Claude
         ↓
Claude processes & shows you the answer
```

**Example**: You ask "Show me git commits from this week"
1. Claude Code sends this request to the Git MCP server
2. Git server runs `git log --since="7 days ago"`
3. Returns the commit list to Claude
4. Claude formats it nicely for you

### Types of MCP Servers

**1. Stdio Servers (Local)**
- Run as child processes directly on your machine
- Communicate via JSON-RPC over stdin/stdout
- No network overhead, fastest
- Examples: git helper, local database client, file indexer

**2. HTTP/SSE Servers (Remote or Local Web Service)**
- Run as web services (could be local `localhost:8000` or remote cloud)
- Use HTTP requests + Server-Sent Events for streaming
- Good for: cloud APIs, shared team servers
- Examples: GitHub API wrapper, Slack integration, OpenWeather

**3. Plugin-bundled Servers (Built-in)**
- Included with Claude Code plugins
- Example: `plugin:playwright:playwright` (web automation tool)
- Just enable the plugin, server connects automatically

### Step-by-Step: Setting Up MCP Servers

#### Step 1: Create or Edit `.mcp.json` in Your Project Root

Create a file named `.mcp.json` at the root of your project (same level as `.git/`):

```bash
cd /home/sameer/Documents/Claude_Code
touch .mcp.json
```

#### Step 2: Add a Server Configuration

Here's a **complete beginner example** with multiple server types:

```json
{
  "mcpServers": {
    "git": {
      "command": "python",
      "args": ["-m", "mcp_server_git"]
    },
    
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropics/mcp-server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_token_here"
      }
    },
    
    "sqlite": {
      "command": "python",
      "args": ["-m", "mcp_server_sqlite", "--db-path", "./data.db"]
    },
    
    "weather": {
      "type": "sse",
      "url": "https://weather-mcp.example.com",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

Let me explain each part:

**Server Name** (`"git"`, `"github"`, etc.)
- This is what you'll reference when asking Claude to use it
- Can be any name you choose

**For Local (Stdio) Servers**:
```json
{
  "command": "python",           // What interpreter to use
  "args": ["-m", "mcp_server_git"],  // What to run
  "env": {}                       // Optional: environment variables
}
```

- `"command"`: The executable on your system (python, node, npx, etc.)
- `"args"`: Arguments passed to that command (like `python -m mcp_server_git`)
- `"env"`: Optional environment variables (secrets, API keys, paths)

**For Remote (HTTP/SSE) Servers**:
```json
{
  "type": "sse",                  // Server-Sent Events protocol
  "url": "https://...",           // Full URL to the server
  "headers": {                    // HTTP headers (auth, etc.)
    "Authorization": "Bearer ..."
  }
}
```

#### Step 3: Install Required Server Software

Before you can use a server, you need to install it. Here are common examples:

**Git MCP Server**:
```bash
pip install mcp-server-git
# or if using npm:
npm install -g @anthropics/mcp-server-git
```

**GitHub MCP Server** (Node.js):
```bash
npm install -g @anthropics/mcp-server-github
```

**SQLite MCP Server**:
```bash
pip install mcp-server-sqlite
```

**Custom Server** (if you wrote one):
```bash
# Just make sure it's executable
chmod +x ./my_mcp_server.py
```

#### Step 4: Start Claude Code and Approve Servers

When you run Claude Code with `.mcp.json` present:

```bash
claude code
```

Claude Code will show:
```
⚠️  New MCP servers found. Do you want to enable them?
  ✓ git
  ✓ github  
  ✓ sqlite
```

Choose:
- **Approve all** if you trust them all
- **Approve individually** for security
- **Skip** to disable for now

#### Step 5: Use the Servers

Once approved, just ask Claude naturally:

```bash
$ claude code
> List all commits from this week
> Create a GitHub issue for the bug we just found
> Query the database for users created today
```

Claude will automatically use the right MCP server for each request.

### Creating Your Own MCP Server (Beginner Example)

Let's create a simple MCP server that tells you the current time:

**File: `my_time_server.py`**

```python
#!/usr/bin/env python3
"""
Simple MCP server that provides time-related tools
"""

import json
import sys
import datetime

def process_request(request):
    """Handle incoming JSON-RPC requests from Claude Code"""
    
    method = request.get("method")
    
    if method == "initialize":
        # Claude Code is asking what capabilities this server has
        return {
            "result": {
                "name": "time-server",
                "version": "1.0.0",
                "tools": [
                    {
                        "name": "get_current_time",
                        "description": "Get the current time",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "timezone": {
                                    "type": "string",
                                    "description": "Timezone (e.g., 'UTC', 'US/Eastern')"
                                }
                            }
                        }
                    },
                    {
                        "name": "get_date",
                        "description": "Get today's date",
                        "inputSchema": {"type": "object"}
                    }
                ]
            }
        }
    
    elif method == "get_current_time":
        # Claude wants to know the current time
        args = request.get("params", {})
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return {
            "result": f"Current time: {current_time}"
        }
    
    elif method == "get_date":
        # Claude wants today's date
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        return {
            "result": f"Today's date: {today}"
        }
    
    else:
        return {"error": f"Unknown method: {method}"}

def main():
    """Read requests from stdin, process them, write responses to stdout"""
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = process_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
```

**Register it in `.mcp.json`**:

```json
{
  "mcpServers": {
    "my-time-server": {
      "command": "python",
      "args": ["./my_time_server.py"]
    }
  }
}
```

**Use it**:
```bash
$ claude code
> What time is it?
[Claude calls your MCP server's get_current_time tool]
> Today's date?
[Claude calls your MCP server's get_date tool]
```

### Understanding Resources vs Tools

**Resources** = Read-only information Claude can request
- Example: Git commit history, file contents, API documentation
- Claude asks: "Show me this resource"
- Server responds: "Here's the data"

**Tools** = Actions Claude can perform
- Example: Create a git commit, send a Slack message, update a database row
- Claude asks: "Please call this tool with these arguments"
- Server executes the action and returns the result

Most beginner servers start with tools. Resources come later when you want Claude to inspect larger datasets efficiently.

### Troubleshooting MCP Connection Issues

**Problem**: MCP server connection fails or times out

**Solution Steps**:

1. **Verify the server is installed**:
   ```bash
   python -m mcp_server_git --help
   # or
   npm list -g @anthropics/mcp-server-git
   ```

2. **Test manually**:
   ```bash
   # Start the server in another terminal
   python -m mcp_server_git
   
   # If it starts without errors, it's working
   ```

3. **Reload Claude Code configuration**:
   ```bash
   # In Claude Code, run:
   /hooks
   # This reloads all MCP configurations
   ```

4. **Check server logs**:
   ```bash
   # MCP logs are usually here:
   ~/.claude/logs/
   
   # Look for errors
   cat ~/.claude/logs/mcp.log
   ```

5. **Restart Claude Code**:
   ```bash
   # Exit and restart
   exit
   claude code
   ```

6. **For HTTP/SSE servers**, verify connectivity:
   ```bash
   # Check if the server is running
   curl https://your-mcp-server-url/health
   ```

### Common Pre-built MCP Servers

Here are popular servers you can use:

| Server | Install | Use Case |
|--------|---------|----------|
| **git** | `pip install mcp_server_git` | Git operations (commits, diffs, logs) |
| **github** | `npm install -g @anthropics/mcp-server-github` | GitHub PRs, issues, workflows |
| **sqlite** | `pip install mcp_server_sqlite` | Query local SQLite databases |
| **postgres** | `pip install mcp_server_postgres` | PostgreSQL database queries |
| **slack** | `npm install -g @anthropics/mcp-server-slack` | Send/read Slack messages |
| **playwright** | Built into Claude Code plugin | Web automation, screenshots |
| **file-search** | `npm install -g @anthropics/mcp-server-file-search` | Index & search files |

---