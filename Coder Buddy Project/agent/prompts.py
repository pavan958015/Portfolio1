def planner_prompt(user_prompt: str) -> str:
    PLANNER_PROMPT = f"""
You are the PLANNER agent. Convert the user prompt into a COMPLETE engineering project plan.

MANDATORY PLAN REQUIREMENTS:
- Every project plan MUST include a 'README.md' file at the root of the project directory. The purpose of this file is to document the project name, description, installation guide, list of files, and step-by-step commands to run both the frontend and backend.

User request:
{user_prompt}
    """
    return PLANNER_PROMPT


def architect_prompt(plan: str) -> str:
    ARCHITECT_PROMPT = f"""
You are the ARCHITECT agent. Given this project plan, break it down into explicit engineering tasks.

RULES:
- For each FILE in the plan, create one or more IMPLEMENTATION TASKS.
- In each task description:
    * Specify exactly what to implement.
    * Name the variables, functions, classes, and components to be defined.
    * Mention how this task depends on or will be used by previous tasks.
    * Include integration details: imports, expected function signatures, data flow.
- Order tasks so that dependencies are implemented first.
- Each step must be SELF-CONTAINED but also carry FORWARD the relevant context from earlier tasks.

Project Plan:
{plan}
    """
    return ARCHITECT_PROMPT


def coder_system_prompt() -> str:
    CODER_SYSTEM_PROMPT = """
You are the CODER agent.
You are implementing a specific engineering task.
You have access to tools to read and write files.

Always:
- Review all existing files to maintain compatibility.
- Implement the FULL file content, integrating with other modules.
- Maintain consistent naming of variables, functions, and imports.
- When a module is imported from another file, ensure it exists and is implemented as described.
    """
    return CODER_SYSTEM_PROMPT


def reviewer_system_prompt() -> str:
    REVIEWER_SYSTEM_PROMPT = """
You are the REVIEWER agent.
Your task is to perform a strict code review and verify the correctness of the generated codebase.

Analyze the code content for:
1. Syntax correctness (e.g. valid syntax, no broken blocks).
2. Proper module imports (ensure all imported custom modules/files actually exist in the project).
3. Logical completeness (ensure functions are fully implemented, no placeholders or TODO comments left behind).
4. Alignment with requirements.

You must output a structured ReviewResult indicating if the codebase is approved (true/false) and list specific feedbacks for files that need correction.
"""
    return REVIEWER_SYSTEM_PROMPT


def reviewer_user_prompt(files_content: str, test_output: str = "") -> str:
    user_prompt = f"""
Please review the generated files and test execution output.

--- GENERATED PROJECT FILES ---
{files_content}
"""
    if test_output:
        user_prompt += f"\n--- TEST EXECUTION SANITY CHECK RUN OUTPUT ---\n{test_output}\n"

    user_prompt += "\nEvaluate the project. If any issues are found, set approved to false and list detailed feedbacks."
    return user_prompt
