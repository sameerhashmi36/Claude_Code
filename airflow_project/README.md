# Airflow Project

## What is Apache Airflow?

**Apache Airflow** is an open-source workflow orchestration platform that allows you to programmatically author, schedule, and monitor workflows. Instead of managing cron jobs or other scheduling tools, Airflow provides a clean, Pythonic way to define complex data pipelines.

### Key Concepts

- **DAG (Directed Acyclic Graph)**: A collection of tasks with dependencies. Each task is a node, and edges represent dependencies between tasks.
- **Task**: A unit of work—it could be running a Python function, executing a SQL query, or any other operation.
- **Operator**: A template for a predefined task (e.g., `PythonOperator`, `BashOperator`, `EmailOperator`).
- **Scheduler**: Airflow's scheduler monitors all DAGs and triggers task execution based on dependencies and schedules.
- **Executor**: Responsible for running tasks (LocalExecutor, CeleryExecutor, KubernetesExecutor, etc.).
- **Assets**: (Airflow 2.8+) A way to track data outputs and create dependencies between DAGs based on data availability rather than time.

### How Airflow Works

1. You define a DAG in Python code with tasks and their dependencies.
2. Airflow parses all DAG files in the `dags/` folder at regular intervals.
3. The scheduler checks if tasks are ready to run based on their dependencies and schedule.
4. When conditions are met, the scheduler submits tasks to an executor.
5. The executor runs the tasks and reports the results back.
6. You can monitor everything through the Airflow web UI.

---

## Project Overview

This project demonstrates **asset-based scheduling** in Airflow, where downstream DAGs are triggered when upstream DAGs produce specific data outputs (assets).

### Project Structure

```
airflow_project/
├── dags/
│   ├── data_fetch.py      # Producer DAG - fetches and materializes data
│   └── data_report.py     # Consumer DAG - triggered when asset is available
├── .env                   # Environment variables (empty template)
└── README.md             # This file
```

---

## DAGs Overview

### 1. **data_fetch.py** (Producer DAG)

**Purpose**: Fetches data from an API, transforms it, and materializes it as a JSON asset.

**Tasks**:
- `prepare_storage()`: Creates the necessary directory structure for storing data
- `fetch_api_data()`: Simulates an API call and returns raw data (city, temperature, unit)
- `transform_data()`: Cleans/transforms the raw data by adding metadata (processed timestamp, status)
- `materialize_asset()`: Writes the final data to a JSON file and marks it as an **asset**

**Key Feature**: Uses `@task(outlets=[weather_data_asset])` to declare that this task produces an asset. This allows downstream DAGs to depend on it.

**Output**: 
```json
{
  "city": "New York",
  "temp": 22,
  "unit": "C",
  "processed_at": "2026-09-15T12:34:56.789123",
  "status": "cleansed"
}
```

---

### 2. **data_report.py** (Consumer DAG)

**Purpose**: Reads the materialized asset and performs analysis on it.

**Schedule**: Triggered automatically whenever the `weather_data_asset` from `data_fetch` is updated (asset-based scheduling).

**Tasks**:
- `read_asset()`: Reads the JSON asset and prints analysis (city and temperature)

**Key Feature**: Uses `@dag(schedule=[weather_data_asset])` to subscribe to the asset produced by `data_fetch`. When the asset is materialized, this DAG automatically runs.

---

## Workflow

```
data_fetch DAG:
  prepare_storage() 
        ↓
  fetch_api_data() ──→ transform_data() ──→ materialize_asset() [produces weather_data_asset]
                                                      ↓
                                          (Asset materialized to file)
                                                      ↓
data_report DAG:
  (triggered by asset) → read_asset() [consumes weather_data_asset]
```

---

## Setup & Running

### Prerequisites
- Python 3.8+
- Apache Airflow installed
- Environment variables configured (if needed)

### Installation

1. **Install Airflow** (if not already installed):
   ```bash
   pip install apache-airflow
   ```

2. **Navigate to the project**:
   ```bash
   cd airflow_project
   ```

### Running Airflow

1. **Initialize Airflow database** (first time only):
   ```bash
   airflow db init
   ```

2. **Create a user** (first time only):
   ```bash
   airflow users create --username admin --password admin \
     --firstname Admin --lastname User --role Admin --email admin@example.com
   ```

3. **Start the scheduler** (in one terminal):
   ```bash
   airflow scheduler
   ```

4. **Start the web server** (in another terminal):
   ```bash
   airflow webserver --port 8080
   ```

5. **Access the UI**:
   - Open `http://localhost:8080`
   - Login with `admin` / `admin`
   - Navigate to the "DAGs" tab to see `data_fetch` and `data_report`

### Triggering DAGs

- **Manually trigger** `data_fetch` DAG from the UI
- `data_report` will automatically trigger once `data_fetch` completes and the asset is materialized

---

## Asset-Based Scheduling

This project uses **asset-based scheduling** (Airflow 2.8+), which is a modern approach to DAG dependencies:

- **Traditional scheduling**: DAGs run on a fixed schedule (cron-like)
- **Asset-based scheduling**: DAGs run when their upstream dependencies produce data

Benefits:
- More reliable: DAGs trigger only when data is actually available
- Eliminates cascading failures: If data production fails, dependent DAGs won't run unnecessarily
- Data-driven: Scheduling depends on data, not just time

---

## File Locations

- **Data files**: `/opt/airflow/data/weather_report.json`
- **Logs**: `$AIRFLOW_HOME/logs/`
- **Database**: `$AIRFLOW_HOME/airflow.db` (SQLite by default)

---

## Next Steps

1. **Modify task logic**: Edit the `fetch_api_data()` function to call a real API
2. **Add more tasks**: Extend the DAGs with additional data processing steps
3. **Error handling**: Add retry logic and alerting for production use
4. **Scaling**: Switch to a production executor (Celery, Kubernetes) for parallel task execution

---

## Resources

- [Apache Airflow Documentation](https://airflow.apache.org/)
- [Airflow Concepts](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html)
- [Asset-based Scheduling](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/assets.html)
- [Decorators (TaskFlow API)](https://airflow.apache.org/docs/apache-airflow/stable/concepts/taskflow.html)

---

*Created to document and understand the Airflow project structure and asset-based scheduling patterns.*
