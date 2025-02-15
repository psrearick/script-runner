import os
import sys
from pathlib import Path

def run_script(script_info, args=()):
    script_path = Path(script_info["path"])
    venv = script_info.get("venv")

    if venv:
        python = Path(venv) / "bin" / "python"
    else:
        python = sys.executable

    os.execvp(str(python), [str(python), str(script_path), *args])
