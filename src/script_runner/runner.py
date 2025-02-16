import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

import click

from script_runner.exceptions import ScriptNotFoundError

def run_script(script_info: Dict[str, str], args: Tuple[Any]=tuple()):
    script_path = Path(script_info['path']).resolve()
    python_path = Path(script_info['python']).resolve()

    if not script_path.exists():
        raise ScriptNotFoundError(value = script_path)
    if not python_path.exists():
        raise FileNotFoundError(f"Python not found: {python_path}")

    result = subprocess.run(
        [str(python_path), str(script_path), *args],
        text=True,
        capture_output=True
    )

    if result.stdout:
        click.echo(result.stdout.rstrip())
    if result.stderr:
        click.echo(result.stderr.rstrip(), err=True)

    if result.returncode != 0:
        sys.exit(result.returncode)
