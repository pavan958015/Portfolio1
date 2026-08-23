<div align="center">

<img src="https://img.shields.io/badge/LangGraph-Multi--Agent-7F77DD?style=for-the-badge&logoColor=white" />
<img src="https://img.shields.io/badge/Groq-LLM-0F6E56?style=for-the-badge&logoColor=white" />
<img src="https://img.shields.io/badge/LangChain-Framework-993C1D?style=for-the-badge&logoColor=white" />
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />

<br/><br/>

```
  ╔═══════════════════════════════╗
  ║   🤖  C O D E R  B U D D Y   ║
  ║   AI Multi-Agent Dev Team     ║
  ╚═══════════════════════════════╝
```

### *Natural language in → working project out*

*A multi-agent AI development team that turns your request into a complete, working codebase — file by file — using real developer workflows.*

</div>

<div>
Coder Buddy Project/
├── .junie/                       # Junie agent related files
├── .vscode/                      # VS Code configurations
└── Coder Buddy Project/          # Main codebase
    ├── .env                      # API keys & Env variables
    ├── .venv/                    # Main python virtual environment
    ├── Projects/                 # Folder containing your generated projects (e.g. dashboards, portfolios)
    ├── agent/                    # Code logic / Refactored multi-agent structure
    ├── resources/                # Assets/Diagrams for readme
    ├── main.py                   # Main entry file
    ├── pyproject.toml            # Dependencies metadata
    └── README.md                 # Project documentation

</div>

---

## 🏗️ Architecture

Four specialized agents work in a cyclic workflow to plan, outline, generate, and self-heal the code using a feedback loop:

```text
                               ┌─────────────────┐
                               │   User Prompt   │
                               └────────┬────────┘
                                        ▼
                              ┌───────────────────┐
                              │   Planner Agent   │  ==> Creates High-Level Plan
                              └────────┬──────────┘
                                        ▼
                              ┌───────────────────┐
                              │  Architect Agent  │  ==> Outlines Files & Tasks
                              └────────┬──────────┘
                                        ▼
                       ┌───────────────►├───────────────┐
                       │                ▼               │
                       │      ┌───────────────────┐     │
                       │      │    Coder Agent    │     │  ==> Writes Code using Tools (ReAct)
                       │      └────────┬──────────┘     │
                       │                ▼               │
                       │      ┌───────────────────┐     │
                       │      │  Reviewer Agent   │     │  ==> Runs Compilation & Logic Checks
                       │      └────────┬──────────┘     │
                       │                │               │
                       │     Fail       ▼      Pass     │
                       └────────── [Approved?] ─────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │  Finished App   │
                               └─────────────────┘
```

---

## 📂 Module Structure

The multi-agent system has been refactored into a clean, consolidated **5-file layout** under `agent/`:

```text
agent/
├── __init__.py   # Package initialization
├── graph.py      # LangGraph workflow orchestration & agent node definitions
├── prompts.py    # Consolidated agent prompts (Planner, Architect, Coder, Reviewer)
├── states.py     # Pydantic validation schemas & Agent State definitions
└── tools.py      # Integrated file system & terminal tools (read/write files, run commands)
```

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Notes |
|---|---|
| `uv` package manager | Install from [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) |
| Groq API key | Create one at [console.groq.com/keys](https://console.groq.com/keys) |

### ⚙️ Installation

```bash
# 1. Create & activate virtual environment
uv venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

# 2. Install dependencies
uv pip install -r pyproject.toml

# 3. Configure environment
cp .sample_env .env              # then fill in your values

# 4. Run
python main.py
```

---

## 🧪 Example Prompts

Try these out of the box:

> 🌤️ **Weather Dashboard**
> Build a responsive modern Weather Dashboard in HTML/CSS/JS that displays current forecasts, features sleek dark mode styling, handles search input errors gracefully, and persists search history using localStorage.

> ✅ **Task Planner**
> Create a comprehensive Task Planner web app using HTML, CSS, and JS with priority tags (High/Medium/Low), category filtering, smooth slide-out transition animations, and robust localStorage state.

> 📚 **FastAPI Book Catalog**
> Implement a fully functional RESTful FastAPI backend for a Book Catalog system with a SQLite database, SQLAlchemy models, Pydantic input schemas, and complete CRUD endpoints.

> 📇 **Full-Stack Contact Manager**
> Build a full-stack Contact Manager with a React (Vite) + Tailwind CSS frontend, integrated with a Spring Boot REST API backend and a PostgreSQL database.

> 🛍️ **E-Commerce Explorer**
> Create a modern full-stack E-commerce product explorer with a Next.js frontend and a Node.js/Express backend connected to MongoDB.

---

## 🔧 How the Coder Agent Works

The Coder Agent uses a **ReAct (Reason + Act)** loop — it plans, executes, observes, and iterates until the task is complete:

```
  ┌─────────────┐
  │  Task Input │
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐     ┌─────────────────────────────────────┐
  │   Reason    │────▶│  What file do I need? What's next?  │
  └──────┬──────┘     └─────────────────────────────────────┘
         │
         ▼
  ┌─────────────┐     ┌────────────────────────────────────────┐
  │     Act     │────▶│  write_file · read_file · run_cmd · …  │
  └──────┬──────┘     └────────────────────────────────────────┘
         │
         ▼
  ┌─────────────┐
  │   Observe   │──── loop until done ──┐
  └──────┬──────┘                       │
         │                              │
         ▼                              │
  ┌─────────────┐                       │
  │   Output    │◀──────────────────────┘
  └─────────────┘
```

---

## 🛠️ Available Tools

| Tool | Description |
|---|---|
| `write_file` | Safely writes content to a path-validated file |
| `read_file` | Reads an existing file from the output project |
| `list_files` | Lists all files in a directory |
| `run_cmd` | Executes shell commands (linting, formatting, etc.) |

---

<div align="center">

<!-- Copyright © Codebasics Inc. All rights reserved. -->
Thanks for visiting

</div>