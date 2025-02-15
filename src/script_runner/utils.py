from pathlib import Path
from typing import List, Optional

def get_venv(script: Path, max_depth: int = 3, depth: int = 1) -> Optional[Path]:
    """Get path to nearest virtual environment"""
    if depth > max_depth:
        return None

    if not script.parent:
        return None

    venv_path_matches = list(script.parent.rglob("pyvenv.cfg"))

    if not any(venv_path_matches):
        return get_venv(script=script.parent, max_depth=max_depth, depth=depth + 1)

    closest_venv: Path = venv_path_matches[0]
    closest_distance: int = -1

    for venv in venv_path_matches:
        distance = path_distance(venv, script)
        if distance < closest_distance or closest_distance == -1:
            closest_venv = venv
            closest_distance = distance

    return closest_venv.parent

def path_distance(path1: Path, path2: Path):
    """Calculate the distance between two file paths."""
    abs_path1 = path1.resolve()
    abs_path2 = path2.resolve()

    path1_parts = abs_path1.parts
    path2_parts = abs_path2.parts

    min_len = min(len(path1_parts), len(path2_parts))
    common_prefix_len = 0

    for i in range(min_len):
        if path1_parts[i] == path2_parts[i]:
            common_prefix_len += 1
        else:
            break

    distance = (len(path1_parts) - common_prefix_len) + (len(path2_parts) - common_prefix_len)

    return distance
from pathlib import Path
import ast
import subprocess

def can_run_with_args(file_path: Path):
    """Check if a script can handle command line arguments appropriately."""
    try:
        with open(file_path, 'r') as f:
            tree = ast.parse(f.read())

        has_arg_handling = False
        for node in ast.walk(tree):
            if (isinstance(node, ast.Import) and
                any(name.name == 'argparse' for name in node.names)):
                has_arg_handling = True
                break

            if (isinstance(node, ast.ImportFrom) and
                node.module == 'argparse'):
                has_arg_handling = True
                break

            if (isinstance(node, ast.Attribute) and
                isinstance(node.value, ast.Name) and
                node.value.id == 'sys' and
                node.attr == 'argv'):
                has_arg_handling = True
                break

        has_main = any(
            isinstance(node, ast.If) and
            isinstance(node.test, ast.Compare) and
            isinstance(node.test.left, ast.Name) and
            node.test.left.id == "__name__" and
            len(node.test.comparators) == 1 and
            isinstance(node.test.comparators[0], ast.Constant) and
            node.test.comparators[0].value == "__main__"
            for node in ast.walk(tree)
        )

        return has_main or has_arg_handling
    except:
        return False

def test_script_execution(file_path: Path, python_path: str="python"):
    """Test if script runs without error when given a --help flag."""
    try:
        result = subprocess.run(
            [python_path, str(file_path), "--help"],
            capture_output=True,
            timeout=5
        )

        return result.returncode in {0, 2}
    except:
        return False

def get_runnable_scripts(directory: Path, test_execution: bool=False):
    """Find Python scripts that appear to handle command line execution properly."""
    path = Path(directory)
    excluded_files = {"__init__.py", "__main__.py", "setup.py"}

    runnable_scripts: List[Path] = []
    for file_path in path.rglob("*.py"):
        if (file_path.name not in excluded_files and
            can_run_with_args(file_path) and
            (not test_execution or test_script_execution(file_path))):
            runnable_scripts.append(file_path)

    return runnable_scripts
