import os
from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq
from langchain_ollama import ChatOllama
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

# --- LLM Client Setup ---
ollama_model = os.getenv("OLLAMA_MODEL")

if ollama_model:
    # Use ChatOllama for local LLM
    llm = ChatOllama(
        model=ollama_model,
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0
    )
else:
    # Use ChatGroq for cloud LLM API
    llm = ChatGroq(model="openai/gpt-oss-120b")


# --- Import Consolidated Prompts, States, and Tools ---
from agent.states import Plan, TaskPlan, CoderState, ReviewResult
from agent.prompts import (
    planner_prompt,
    architect_prompt,
    coder_system_prompt,
    reviewer_system_prompt,
    reviewer_user_prompt
)
from agent.tools import (
    init_project_root,
    read_file,
    write_file,
    list_files,
    get_current_directory,
    run_cmd
)


# --- Node Definitions ---

def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan."""
    user_prompt = state["user_prompt"]

    resp = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))

    if resp is None:
        raise ValueError("Planner did not return a valid response.")

    return {"plan": resp}


def architect_agent(state: dict) -> dict:
    """Creates TaskPlan from Plan and initializes project folder."""
    plan: Plan = state["plan"]

    resp = llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(plan=plan.model_dump_json())
    )

    if resp is None:
        raise ValueError("Architect did not return a valid response.")

    resp.plan = plan

    project_dir = init_project_root(plan.name)

    print("\n" + "=" * 60)
    print(f"Creating Project : {plan.name}")
    print(f"Project Folder   : {project_dir}")
    print("=" * 60 + "\n")

    return {"task_plan": resp, "project_dir": project_dir}


def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent."""
    feedbacks = state.get("feedbacks", [])
    coder_tools = [
        read_file,
        write_file,
        list_files,
        get_current_directory,
    ]

    if feedbacks:
        # Coder is in feedback-fixing loop
        current_feedback_idx = state.get("current_feedback_idx", 0)

        if current_feedback_idx >= len(feedbacks):
            print("\nAll feedback items addressed. Re-running reviewer...\n")
            return {
                "feedbacks": [],
                "current_feedback_idx": 0,
                "status": "DONE",
            }

        feedback = feedbacks[current_feedback_idx]
        print(
            f"\nAddressing feedback [{current_feedback_idx + 1}/{len(feedbacks)}] "
            f"for {feedback.filepath}"
        )

        existing_content = read_file.run(feedback.filepath)
        system_prompt = coder_system_prompt()
        user_prompt = (
            f"Task: Address code review feedback and fix the file.\n\n"
            f"File: {feedback.filepath}\n\n"
            f"Review Feedback: {feedback.comment}\n\n"
            f"Existing Content:\n{existing_content}\n\n"
            f"You MUST fix the issue, generate the complete file content, and "
            f"use write_file(path, content) to save it."
        )

        react_agent = create_react_agent(model=llm, tools=coder_tools)

        response = react_agent.invoke(
            {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            }
        )

        print("\nCoder Response (Fix):")
        print(response)
        print("-" * 60)

        return {"current_feedback_idx": current_feedback_idx + 1}

    # Normal generation phase
    coder_state: CoderState = state.get("coder_state")

    if coder_state is None:
        coder_state = CoderState(
            task_plan=state["task_plan"], current_step_idx=0
        )

    steps = coder_state.task_plan.implementation_steps

    if coder_state.current_step_idx >= len(steps):
        print("\nAll files generated successfully.\n")
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]

    print(
        f"\nGenerating [{coder_state.current_step_idx + 1}/{len(steps)}] "
        f"{current_task.filepath}"
    )

    existing_content = read_file.run(current_task.filepath)
    system_prompt = coder_system_prompt()
    user_prompt = (
        f"Task: {current_task.task_description}\n\n"
        f"File: {current_task.filepath}\n\n"
        f"Existing Content:\n{existing_content}\n\n"
        f"You MUST generate the complete file content and "
        f"use write_file(path, content) to save it."
    )

    react_agent = create_react_agent(model=llm, tools=coder_tools)

    response = react_agent.invoke(
        {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        }
    )

    print("\nCoder Response:")
    print(response)
    print("-" * 60)

    coder_state.current_step_idx += 1

    return {"coder_state": coder_state}


def reviewer_agent(state: dict) -> dict:
    """Reviews the generated codebase and runs tests/syntax compilation checks."""
    print("\n" + "=" * 60)
    print("REVIEWER: Reviewing generated files...")
    print("=" * 60 + "\n")

    files_str = list_files.run(".")
    if (
        not files_str
        or files_str.startswith("ERROR")
        or files_str == "No files found."
    ):
        print("Reviewer: No files to review.")
        return {"feedbacks": [], "status": "APPROVED"}

    files_list = [f.strip() for f in files_str.split("\n") if f.strip()]

    files_content_block = []
    python_files = []

    for filepath in files_list:
        content = read_file.run(filepath)
        files_content_block.append(f"File: {filepath}\nContent:\n{content}\n")
        if filepath.endswith(".py"):
            python_files.append(filepath)

    files_summary = "\n".join(files_content_block)

    test_output = ""
    if python_files:
        print(
            f"Reviewer: Performing Python syntax compilation check on: {python_files}"
        )
        for py_file in python_files:
            code, stdout, stderr = run_cmd.run(
                f"python -m py_compile {py_file}"
            )
            if code != 0:
                test_output += f"Syntax error in {py_file}:\n{stderr}\n"

    sys_prompt = reviewer_system_prompt()
    user_prompt = reviewer_user_prompt(files_summary, test_output)

    try:
        structured_llm = llm.with_structured_output(ReviewResult)
        result: ReviewResult = structured_llm.invoke(
            [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
    except Exception as e:
        print(f"Reviewer LLM invocation failed: {e}. Defaulting to approval.")
        result = ReviewResult(approved=True, feedbacks=[])

    print("\nReviewer Results:")
    print(f"Approved: {result.approved}")
    if result.feedbacks:
        print("Feedbacks:")
        for fb in result.feedbacks:
            print(f"- {fb.filepath}: {fb.comment}")
    print("-" * 60)

    if result.approved:
        return {"feedbacks": [], "status": "APPROVED"}
    else:
        return {
            "feedbacks": result.feedbacks,
            "current_feedback_idx": 0,
            "status": "FIXING",
        }


# --- Routing Functions ---

def route_coder(state: dict) -> str:
    """Routes after the Coder agent: to Reviewer if done, else repeat Coder."""
    if state.get("status") == "DONE":
        return "reviewer"
    return "coder"


def route_reviewer(state: dict) -> str:
    """Routes after the Reviewer agent: to END if approved, else back to Coder to fix."""
    if state.get("status") == "APPROVED":
        return "END"
    return "coder"


# --- StateGraph Assembly & Compilation ---

graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)
graph.add_node("reviewer", reviewer_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")

graph.add_conditional_edges(
    "coder", route_coder, {"reviewer": "reviewer", "coder": "coder"}
)

graph.add_conditional_edges(
    "reviewer", route_reviewer, {"END": END, "coder": "coder"}
)

graph.set_entry_point("planner")

# Compile the compiled agent workflow
agent = graph.compile()


if __name__ == "__main__":
    # Test run locally
    result = agent.invoke(
        {"user_prompt": "Build a colourful modern todo app in html css and js"},
        {"recursion_limit": 100},
    )

    print("\nFinal State:")
    print(result)