import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import click

def run_script(script_info: Dict[str, str], args: Tuple[Any]=tuple()):
    script = Path(script_info['path']).resolve()
    venv = Path(script_info.get("venv", sys.executable)).resolve()

    if sys.platform == "win32":
        python_path = venv / "Scripts" / "python.exe"
    else:
        python_path = venv / "bin" / "python"

    if not script.exists():
        raise FileNotFoundError(f"Script not found: {script}")
    if not python_path.exists():
        raise FileNotFoundError(f"Python executable not found in: {python_path}")

    cmd: List[Any] = [str(python_path), str(script), *args]

    try:
        result = subprocess.run(
            cmd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        click.echo(result.stdout.rstrip("\n"))
    except subprocess.CalledProcessError as e:
        click.echo(f"Script failed with exit code {e.returncode}")
        click.echo("stdout: " + e.stdout.rstrip("\n"))
        click.echo("stderr: " + e.stderr.rstrip("\n"))
        raise
