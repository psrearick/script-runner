import json
from pathlib import Path
import sys
from typing import Any, Dict, Generator, List, Optional
from .utils import get_venv, get_script_type, get_interpreter_path
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
            scripts = json.loads(path.read_text())
            # Migrate old format to new format for backward compatibility
            for script in scripts:
                if "python" in script and "interpreter" not in script:
                    # Old format - migrate to new format
                    script["interpreter"] = script.pop("python")
                    script["type"] = "python"
                elif "interpreter" not in script:
                    # Handle edge case of malformed data
                    script["interpreter"] = sys.executable
                    script["type"] = "python"
                elif "type" not in script:
                    # Missing type field - detect it
                    script_path = Path(script["path"])
                    script["type"] = get_script_type(script_path) if script_path.exists() else "python"
            return scripts
        return []

    def save(self):
        self.scripts_file.write_text(json.dumps(self.scripts, indent=2))

    def add_script(self,
                script_path: Path,
                alias: Optional[str]=None,
                interpreter_path: Optional[Path]=None):
        script_path = script_path.resolve()
        if not script_path.exists():
            raise ScriptNotFoundError(value=script_path)

        alias = alias or script_path.stem

        if alias in [s["alias"] for s in self.scripts]:
            raise DuplicateAliasError(value=alias)

        # Detect script type
        script_type = get_script_type(script_path)

        # Get appropriate interpreter
        interpreter = get_interpreter_path(script_path, script_type, interpreter_path)

        if not interpreter.exists():
            raise FileNotFoundError(f"Interpreter not found: {interpreter}")

        self.scripts.append({
            "path": str(script_path),
            "alias": alias,
            "interpreter": str(interpreter),
            "type": script_type
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
        for i, script in enumerate(self.scripts):
            if script["alias"] == alias:
                del self.scripts[i]
                self.save()
                return
        raise AliasNotFoundError(value=alias)
