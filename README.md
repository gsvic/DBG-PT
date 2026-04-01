# DBG-PT: LLM-Powered Query Regression Debugger

DBG-PT is a tool for diagnosing and fixing PostgreSQL query plan regressions using Large Language Models. When a query suddenly slows down, DBG-PT compares the fast and slow execution plans, explains what changed, and recommends configuration settings or indexes to restore performance.

## Features

- **Online Debugger** — tracks query execution history and automatically surfaces regressions
- **Offline Debugger** — paste any two query plans manually for instant LLM analysis
- **Agentic Debugger** — an autonomous LLM agent iteratively tries different Postgres settings via `EXPLAIN ANALYZE` until it finds an optimal configuration

## Prerequisites

- Python 3.9+
- PostgreSQL (running locally or remotely)
- An OpenAI API key

## Installation

```bash
# macOS: install pkg-config for psycopg2
brew install pkg-config

# Create and activate a virtual environment
virtualenv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .
```

## Configuration

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=sk-...
```

Edit `resources/config.ini` with your Postgres credentials:

```ini
[DBGPT]
llm = gpt-4
database = tpch

[POSTGRES]
user = your_postgres_user
# password = your_postgres_password
```

## Running

```bash
streamlit run dbgpt/ui/Home.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

## How It Works

1. **Explore queries** — use the Interactive Query Explorer to run TPC-H or JOB benchmark queries (or your own) with custom Postgres settings. Each execution is recorded with its plan and runtime.

2. **Detect regressions** — the Online Regression Debugger shows execution time trends per query and highlights the fastest vs. most recent plan.

3. **Get recommendations** — send the plans to GPT-4. It returns a diff of the plans, its reasoning, and a list of SQL commands to apply (`SET` parameters and/or `CREATE INDEX`).

4. **Apply and verify** — apply the recommended settings in-browser and immediately re-run the query to confirm the improvement.

5. **Agentic mode** — hand off to the autonomous agent, which calls `EXPLAIN ANALYZE` in a loop with different settings until it finds a configuration that matches or beats the fast plan.

## Project Structure

```
dbgpt/
├── agents/
│   └── debugger.py          # LangGraph ReAct agent + PostgresDBExplorer tool
├── benchmarks/
│   ├── tpch.py              # TPC-H query loader
│   ├── job.py               # Join Order Benchmark query loader
│   └── resources/queries/   # SQL files
├── drivers/
│   ├── postgres.py          # psycopg2 wrapper
│   └── mysqldriver.py       # MySQL connector wrapper
├── ui/
│   ├── Home.py              # Streamlit entry point
│   ├── common.py            # SQLite metadata handler
│   ├── test.py              # LLM prompt builders
│   └── pages/               # Streamlit multi-page app
├── llm.py                   # OpenAI API wrapper
└── utils.py                 # Driver factory, config reader
resources/
└── config.ini               # Database credentials and LLM settings
```

## Citation
```bibtex
@article{giannakouris2024dbg,
  title={Dbg-pt: A large language model assisted query performance regression debugger},
  author={Giannakouris, Victor and Trummer, Immanuel},
  journal={Proceedings of the VLDB Endowment},
  volume={17},
  number={12},
  pages={4337--4340},
  year={2024},
  publisher={VLDB Endowment}
}
```
