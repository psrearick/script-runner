import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

import click

from script_runner.exceptions import ScriptNotFoundError

def run_script(script_info: Dict[str, str], args: Tuple[Any]=tuple()):
    script_path = Path(script_info['path']).resolve()
    interpreter_path = Path(script_info['interpreter']).resolve()
    script_type = script_info.get('type', 'python')

    if not script_path.exists():
        raise ScriptNotFoundError(value = script_path)
    if not interpreter_path.exists():
        raise FileNotFoundError(f"Interpreter not found: {interpreter_path}")

    # Build command based on script type
    if script_type == 'python':
        cmd = [str(interpreter_path), str(script_path), *args]
    elif script_type == 'shell':
        # For shell scripts, make them executable and run directly if possible
        # Otherwise use the interpreter
        if script_path.suffix in ['.sh', '.bash', '.zsh', '.fish'] or not script_path.suffix:
            try:
                # Try to make executable (Unix-like systems)
                script_path.chmod(script_path.stat().st_mode | 0o755)
            except (OSError, AttributeError):
                pass
        cmd = [str(interpreter_path), str(script_path), *args]
    else:
        # Fallback for unknown types
        cmd = [str(interpreter_path), str(script_path), *args]

    result = subprocess.run(
        cmd,
        text=True,
        capture_output=True
    )

    if result.stdout:
        click.echo(result.stdout.rstrip())
    if result.stderr:
        click.echo(result.stderr.rstrip(), err=True)

    if result.returncode != 0:
        sys.exit(result.returncode)
