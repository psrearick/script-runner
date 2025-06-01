from pathlib import Path
from typing import Optional
import os
import sys
import sys

def get_venv(script: Path, max_depth: int = 5, depth: int = 1) -> Optional[Path]:
    """Get path to nearest virtual environment"""
    if depth > max_depth and max_depth > 0:
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

def get_script_type(script_path: Path) -> str:
    """Determine the type of script (python or shell)"""
    # Check file extension first
    if script_path.suffix.lower() == '.py':
        return 'python'
    elif script_path.suffix.lower() in ['.sh', '.bash', '.zsh', '.fish']:
        return 'shell'

    # Check shebang line for extensionless files
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line.startswith('#!'):
                if 'python' in first_line.lower():
                    return 'python'
                elif any(shell in first_line for shell in ['sh', 'bash', 'zsh', 'fish']):
                    return 'shell'
    except (UnicodeDecodeError, PermissionError, FileNotFoundError):
        pass

    # Default to shell for executable files without clear indication
    if os.access(script_path, os.X_OK):
        return 'shell'

    # Default fallback
    return 'python'

def get_interpreter_path(script_path: Path, script_type: str, custom_interpreter: Optional[Path] = None) -> Path:
    """Get the appropriate interpreter path for the script"""
    if custom_interpreter:
        return custom_interpreter.resolve()

    if script_type == 'python':
        # Use existing venv detection logic
        venv = get_venv(script_path)
        if venv:
            python_path = venv / ('Scripts' if os.name == 'nt' else 'bin') / 'python'
            if python_path.exists():
                return python_path
        # Fallback to system python
        return Path(sys.executable)

    elif script_type == 'shell':
        # For shell scripts, use the default shell or try to detect from shebang
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line.startswith('#!'):
                    # Extract interpreter from shebang
                    shebang_parts = first_line[2:].strip().split()
                    if shebang_parts:
                        interpreter = shebang_parts[0]
                        # Handle common cases like #!/usr/bin/env bash
                        if interpreter == '/usr/bin/env' and len(shebang_parts) > 1:
                            interpreter = shebang_parts[1]
                            # Try to find the interpreter in PATH
                            import shutil
                            full_path = shutil.which(interpreter)
                            if full_path:
                                return Path(full_path)
                        elif Path(interpreter).exists():
                            return Path(interpreter)
        except (UnicodeDecodeError, PermissionError, FileNotFoundError):
            pass

        # Default to system shell
        shell = os.environ.get('SHELL', '/bin/bash')
        return Path(shell)

    # Fallback
    return Path(sys.executable)
