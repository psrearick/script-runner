import json
from pathlib import Path
import sys
from typing import Any, Dict, Generator, List, Optional
from .utils import get_venv
from .exceptions import AliasNotFoundError, DuplicateAliasError, ScriptNotFoundError

class Registry:
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / ".config" / "script_runner"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.scripts_file = self.config_dir / "scripts.json"
        self._load()

    def _load(self):
        self.scripts = self._load_json(self.scripts_file)

    def _load_json(self, path: Path) -> List[Dict[str, str]]:
        if path.exists():
            return json.loads(path.read_text())
        return []

    def save(self):
        self.scripts_file.write_text(json.dumps(self.scripts, indent=2))

    def add_script(self,
                script_path: Path,
                alias: Optional[str]=None,
                python_path: Optional[Path]=None):
        script_path = script_path.resolve()
        if not script_path:
            raise ScriptNotFoundError(value=script_path)

        alias = alias or script_path.stem

        if alias in [s["alias"] for s in self.scripts]:
            raise DuplicateAliasError(value=alias)

        if not python_path:
            venv = get_venv(script_path)
            if venv:
                python_path = venv / ('Scripts' if sys.platform == 'win32' else 'bin') / 'python'
            else:
                python_path = Path(sys.executable)

        python_path = python_path.resolve()
        if not python_path.exists():
            raise FileNotFoundError(f"Python executable not found: {python_path}")

        self.scripts.append({
            "path": str(script_path),
            "alias": alias,
            "python": str(python_path)
        })

        self.save()

    def get_script(self, alias: str) -> Dict[str, str]:
        match = next(script for script in self.scripts if script["alias"] == alias)

        if not match:
            raise AliasNotFoundError(value=alias)

        return match

    def prune(self) -> Generator[Any, None, str|None]:
        for i in range(len(self.scripts) - 1, -1, -1):
            script = self.scripts[i]
            path = Path(script["path"])
            if not path.exists():
                alias = script["alias"]
                del self.scripts[i]
                yield alias
        self.save()

    def remove_alias(self, alias: str):
        script = self.get_script(alias)
        del script
        self.save()
