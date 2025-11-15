import subprocess
import sys
import os
from pathlib import Path
from typing import Dict, Tuple, Optional

from script_runner.exceptions import ScriptNotFoundError

def get_activated_env(interpreter_path: Path, script_type: str) -> Optional[Dict[str, str]]:
    """Create environment variables for virtual environment activation"""
    if script_type != 'python':
        return None

    # Check if this is a virtual environment python (use original path, not resolved)
    # This is important because venv python executables are often symlinks to system python
    original_bin_dir = interpreter_path.parent
    if original_bin_dir.name in ('bin', 'Scripts'):  # Unix/Windows venv structure
        venv_path = original_bin_dir.parent
        pyvenv_cfg = venv_path / 'pyvenv.cfg'

        if pyvenv_cfg.exists():
            # Create activated environment
            env = os.environ.copy()
            env['VIRTUAL_ENV'] = str(venv_path)

            # Update PATH to include venv's bin directory
            path_separator = ';' if os.name == 'nt' else ':'
            if 'PATH' in env:
                env['PATH'] = str(original_bin_dir) + path_separator + env['PATH']
            else:
                env['PATH'] = str(original_bin_dir)

            # Remove PYTHONHOME if set (can conflict with venv)
            env.pop('PYTHONHOME', None)

            return env

    return None

def run_script(script_info: Dict[str, str], args: Tuple[str, ...], verbose: bool = False):
    script_path = Path(script_info['path']).resolve()
    interpreter_path_original = Path(script_info['interpreter'])
    interpreter_path = interpreter_path_original.resolve()
    script_type = script_info.get('type', 'python')

    if not script_path.exists():
        raise ScriptNotFoundError(value = script_path)
    if not interpreter_path.exists():
        raise FileNotFoundError(f"Interpreter not found: {interpreter_path}")

    # Get activated environment for virtual environments (use original path for detection)
    env = get_activated_env(interpreter_path_original, script_type)

    # if verbose and env:
    #     print(f"Activating virtual environment: {env.get('VIRTUAL_ENV')}")
    #     print(f"Using interpreter: {interpreter_path}")
    # elif verbose:
    #     print(f"No virtual environment detected for: {interpreter_path}")

    # Build command based on script type
    if script_type == 'python':
        # Use original interpreter path to preserve venv structure
        cmd = [str(interpreter_path_original), str(script_path), *args]
    elif script_type == 'shell':
        # For shell scripts, make them executable and run directly if possible
        # Otherwise use the interpreter
        if script_path.suffix in ['.sh', '.bash', '.zsh', '.fish'] or not script_path.suffix:
            try:
                # Try to make executable (Unix-like systems)
                script_path.chmod(script_path.stat().st_mode | 0o755)
            except (OSError, AttributeError):
                pass
        cmd = [str(interpreter_path_original), str(script_path), *args]
    else:
        # Fallback for unknown types
        cmd = [str(interpreter_path_original), str(script_path), *args]

    if verbose:
        # Stream output in real-time when verbose
        result = subprocess.run(
            cmd,
            text=True,
            env=env
        )
    else:
        # Capture and discard output when not verbose
        result = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            env=env
        )

    if result.returncode != 0:
        sys.exit(result.returncode)
