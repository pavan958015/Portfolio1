# Coder Buddy - Project Flow & Architecture (Interview-Friendly Guide)

This document explains the architecture, design choices, and execution flow of **Coder Buddy** in a structured format suitable for technical interviews.

---

## 🚀 1. Core Architectural Concept: Multi-Agent Collaboration

### What is Coder Buddy?
Coder Buddy is a **multi-agent autonomous development system**. Instead of asking a single LLM to generate an entire project at once (which often fails on complex tasks due to context limits and hallucinations), Coder Buddy splits the task among specialized agents operating in a structured pipeline.

### Why this approach?
* **Separation of Concerns:** Each agent has a single, well-defined responsibility (planning, architecting, coding, or reviewing).
* **Iterative Self-Healing:** The system can detect its own compilation/test failures and route them back to the coder for automatic bug fixing.
* **Context Preservation:** By breaking a large task into smaller implementation steps, the model generates code with much higher precision.

---

## 🏛️ 2. System Architecture & Tech Stack

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
                       │      │    Coder Agent    │     │  ==> Writes Code using Tools
                       │      └────────┬──────────┘     │
                       │                ▼               │
                       │      ┌───────────────────┐     │
                       │      │  Reviewer Agent   │     │  ==> Runs Compilation Checks
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

* **Orchestration Framework:** **LangGraph** (StateGraph) & **LangChain**.
* **LLM Engine:** Local **Ollama** (`gemma4:e2b-it-qat` via LangChain-Ollama) or Cloud **Groq** APIs.
* **State Management:** Enforced using **Pydantic** structured models.
* **Runtime/Execution Environment:** Standard Python shell running test suites locally inside a sandboxed target folder.

---

## 🔄 3. Step-by-Step Data Flow

The workflow models the development lifecycle as a State Machine using `StateGraph(dict)`:

### Step 1: Planning Node (`planner_agent`)
* **Input:** Raw user prompt (e.g., *"Create a personal portfolio website"*).
* **Process:** The Planner analyzes the prompt and returns a structured `Plan` (Pydantic model).
* **Output Plan Schema:**
  - `name`: Name of the app.
  - `techstack`: Selected language and libraries.
  - `features`: List of high-level features.
  - `files`: List of files to be created and their purposes.

### Step 2: Architecture Node (`architect_agent`)
* **Input:** The generated `Plan`.
* **Process:** The Architect translates the high-level plan into a sequential roadmap of tasks (`TaskPlan` Pydantic model).
  - It orders tasks logically so that dependencies (e.g., helpers, DB files) are created *before* files that depend on them (e.g., main application logic, tests).
  - It initializes a clean project folder under the `Projects/` directory.
* **Output Task Schema:** A list of `ImplementationTask` objects (each having `filepath` and a highly detailed `task_description`).

### Step 3: Coding Node (`coder_agent`)
* **Input:** The `TaskPlan` and the current task index.
* **Process:** The Coder is a **ReAct Agent** (Reasoning + Acting loop). It takes one task at a time and is equipped with filesystem tools:
  - `write_file(path, content)`
  - `read_file(path)`
  - `list_files(directory)`
  - `get_current_directory()`
* **Behavior:** It writes the complete code for the file and increments the step index, looping back to itself until all files in the roadmap are written.

### Step 4: Reviewing Node (`reviewer_agent`)
* **Input:** Generated files content.
* **Process:** 
  - It compiles all `.py` files using `python -m py_compile` to catch syntax errors.
  - It invokes LLM-based logical review comparing the code against the planner requirements.
* **Decision Path:**
  - **APPROVED:** If the code is correct, it returns `status = APPROVED`, terminating the graph (`END`).
  - **REJECTED (Self-Healing Loop):** If there are compiler errors or logical bugs, it generates a list of `FileFeedback` items (file paths and error comments). The graph routes back to the `coder_agent` to fix the specific issues.

---

## 💡 4. Top Interview Questions & Answers

### Q1. Why did you choose LangGraph instead of a simple sequential LLM Chain?
> **Answer:** Software development is inherently non-linear and iterative. If a coder makes a syntax mistake or logic bug, a standard sequential LLM chain has no way to turn back and fix it. LangGraph allows us to build **cyclic graphs**. This lets us route execution back to the Coder Agent with specific compiler logs/feedback from the Reviewer Agent, enabling autonomous self-healing.

### Q2. How do you handle LLM security risks, like writing files outside the project workspace?
> **Answer:** We implemented a path-sandboxing function called `safe_path_for_project`. Whenever the Coder Agent calls `write_file` or `read_file` with a relative path, this helper resolves the absolute path and explicitly verifies that the resolved path starts with the initialized `PROJECT_ROOT` directory. If the model attempts to write to a path like `../../etc/passwd`, it raises a `ValueError` preventing directory traversal attacks.

### Q3. How does the Coder Agent interact with the file system?
> **Answer:** The Coder Agent is configured as a **ReAct Agent** using LangChain's `create_react_agent`. We wrap standard Python filesystem operations as LangChain `@tool` objects (with clear docstrings describing parameters). The LLM decides when to call these tools, parses the tool responses, and continues its reasoning loop until it writes the complete code successfully.

### Q4. What is "Structured Output" and why is it important in this project?
> **Answer:** LLMs naturally generate unstructured text. For orchestration logic (e.g., knowing exactly what files to create or what tests failed), we need structured JSON schemas. We use Pydantic models (like `Plan` and `TaskPlan`) and bind them to the LLM using `.with_structured_output()`. This forces the LLM to output valid JSON conforming exactly to our schema, preventing parser crashes.

### Q5. How does the self-healing cycle prevent infinite loops?
> **Answer:** In `main.py`, the graph is executed with a `recursion_limit` parameter (default: 100). If the Coder and Reviewer get stuck in a feedback loop due to a hard-to-solve bug, LangGraph automatically halts execution once the transition count exceeds the limit, preventing resource exhaustion and infinite API billing.

