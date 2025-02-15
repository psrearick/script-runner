import subprocess
import sys
from pathlib import Path

def run_script(script_info: dict, args=()):
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

    cmd = [str(python_path), str(script), *args]

    try:
        result = subprocess.run(
            cmd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Script failed with exit code {e.returncode}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        raise
