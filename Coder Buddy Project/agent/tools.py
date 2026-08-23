import os
import pathlib
import subprocess
from datetime import datetime
from typing import Tuple
from langchain_core.tools import tool

# --- Dynamic Project Root Management ---
PROJECT_ROOT = None


def init_project_root(project_name: str) -> str:
    """Initializes the output project root directory in workspace/Projects/."""
    global PROJECT_ROOT

    safe_name = (
        project_name.lower()
        .replace(" ", "_")
        .replace("-", "_")
    )

    folder_name = f"{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    # Project root points to the Projects folder inside current working directory
    PROJECT_ROOT = pathlib.Path.cwd() / "Projects" / folder_name
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)

    print(f"\nProject Created At: {PROJECT_ROOT}\n")
    return str(PROJECT_ROOT)


def get_project_root() -> pathlib.Path:
    """Returns the initialized PROJECT_ROOT or raises ValueError if not set."""
    global PROJECT_ROOT
    if PROJECT_ROOT is None:
        raise ValueError("Project root not initialized")
    return PROJECT_ROOT


def safe_path_for_project(path: str) -> pathlib.Path:
    """Ensures that the given path is resolved safely inside the project root."""
    project_root = get_project_root()
    p = (project_root / path).resolve()

    if (
        project_root.resolve() not in p.parents
        and project_root.resolve() != p
    ):
        raise ValueError("Attempt to write outside project root")

    return p


# --- LangChain Core File IO Tools ---

@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file at the specified path within the project root."""
    try:
        p = safe_path_for_project(path)

        if p.is_dir():
            return f"ERROR: '{path}' is a directory. Cannot write content directly to a directory path."

        p.parent.mkdir(parents=True, exist_ok=True)

        with open(p, "w", encoding="utf-8") as f:
            f.write(content)

        return f"WROTE: {p}"
    except Exception as e:
        return f"ERROR: Could not write file '{path}': {e}"


@tool
def read_file(path: str) -> str:
    """Reads content from a file at the specified path within the project root."""
    try:
        p = safe_path_for_project(path)

        if not p.exists():
            return ""

        if p.is_dir():
            return f"ERROR: '{path}' is a directory, not a file."

        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"ERROR: Could not read file '{path}': {e}"


@tool
def get_current_directory() -> str:
    """Returns the current working directory."""
    return str(get_project_root())


@tool
def list_files(directory: str = ".") -> str:
    """Lists all files in the specified directory within the project root."""
    project_root = get_project_root()
    p = safe_path_for_project(directory)

    if not p.is_dir():
        return f"ERROR: {p} is not a directory"

    files = [
        str(f.relative_to(project_root))
        for f in p.glob("**/*")
        if f.is_file()
    ]

    return "\n".join(files) if files else "No files found."


@tool
def run_cmd(
    cmd: str, cwd: str = None, timeout: int = 30
) -> Tuple[int, str, str]:
    """Runs a shell command in the specified directory and returns the result."""
    project_root = get_project_root()
    cwd_dir = safe_path_for_project(cwd) if cwd else project_root

    res = subprocess.run(
        cmd,
        shell=True,
        cwd=str(cwd_dir),
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    return res.returncode, res.stdout, res.stderr
