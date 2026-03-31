# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

**DBG-PT** is a query regression debugging tool powered by LLMs. Given two execution plans for the same query (a fast one and a slow one), it uses GPT-4 to explain the regression and recommend configuration changes or indexes to restore performance.

It offers three debugging modes:
- **Online** — compares plans from a history of executed queries stored in SQLite
- **Offline** — paste two plans manually, no DB connection needed
- **Agentic** — a LangGraph ReAct agent autonomously tries different Postgres settings via `EXPLAIN ANALYZE` until it finds one that recovers performance

## Setup

```bash
# macOS prerequisites (for psycopg2)
brew install pkg-config

# Python environment
virtualenv .venv
source .venv/bin/activate
pip install -e .

# Set OpenAI key (required)
export OPENAI_API_KEY=sk-...

# Set Postgres credentials
# Edit resources/config.ini with your username (and optionally password)
```

`resources/config.ini` structure:
```ini
[DBGPT]
llm = gpt-4
database = tpch        # default DB when none is specified

[POSTGRES]
user = your_pg_user
# password = optional
```

## Running

```bash
streamlit run dbgpt/ui/Home.py
```

Streamlit will auto-discover the pages under `dbgpt/ui/pages/`.

## Architecture

**Entry point:** `dbgpt/ui/Home.py` — Streamlit home page. Run this directly.

**UI pages** (`dbgpt/ui/pages/`):
- `1_Interactive Query Explorer.py` — execute queries with custom settings, records results to SQLite
- `2_Online Regression Debugger.py` — picks two executions from history, sends plans to LLM
- `3_Offline Regression Debugger.py` — freeform plan paste, LLM analysis only
- `4_Agentic Regression Debugger.py` — invokes `DebuggingAgent` which runs autonomously

**LLM layer:**
- `dbgpt/llm.py` — `get_response(text, temperature)` wraps the OpenAI chat completions API
- `dbgpt/ui/test.py` — `prompt()` and `prompt_single_plan()` build the plan-comparison prompts and parse JSON responses from the LLM

**Agent** (`dbgpt/agents/debugger.py`):
- `PostgresDBExplorer` — LangChain `BaseTool` that applies settings then runs `EXPLAIN ANALYZE`
- `DebuggingAgent` — wraps a LangGraph `create_react_agent` with GPT-4-turbo; calls `debug()` to get back a message list

**Persistence** (`dbgpt/ui/common.py`):
- `QueryMetadataHandler` — SQLite-backed store for queries and their execution history; auto-initializes TPC-H and JOB benchmark queries on first run; DB file is `lambda_pi.db` in the working directory

**Database drivers** (`dbgpt/drivers/`):
- `PostgresDriver` — psycopg2 wrapper; `cursor` attribute used directly by UI pages
- `MySQLDriver` — mysql-connector wrapper (not used by current UI pages)
- `get_dbms_driver(system, db, user, password)` in `dbgpt/utils.py` reads credentials from `resources/config.ini` and returns the appropriate driver

**Benchmarks** (`dbgpt/benchmarks/`):
- `get_tpch_queries()` and `get_job_queries()` load SQL files from `dbgpt/benchmarks/resources/queries/`; called once at startup by `QueryMetadataHandler` to seed the SQLite DB
