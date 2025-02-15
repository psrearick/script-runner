import json
from pathlib import Path
from typing import Optional
from uuid import UUID, uuid4

class Registry:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "script_runner"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.scripts_file = self.config_dir / "scripts.json"
        self.directories_file = self.config_dir / "directories.json"
        self._load()

    def _load(self):
        self.scripts = self._load_json(self.scripts_file)
        self.directories = self._load_json(self.directories_file)

    def _load_json(self, path: Path):
        if path.exists():
            return json.loads(path.read_text())
        return {}

    def _save(self):
        self.scripts_file.write_text(json.dumps(self.scripts, indent=2))
        self.directories_file.write_text(json.dumps(self.directories, indent=2))

    def _add_single_script(self, script: Path, alias: Optional[str] = None, dir_id: Optional[UUID] = None, venv: Optional[Path] = None, venv_depth: int = 3):
        pass

    def add_script(self, path: Path, alias: Optional[str]=None, venv: Optional[Path]=None, venv_depth: int = 3):
        if path.is_dir():
            dir_id = str(uuid4())
            self.directories[dir_id] = {
                "path": str(path),
                "venv": str(venv) if venv else None
            }
            for script in path.rglob("*.py"):
                self._add_single_script(script, dir_id=dir_id, venv=venv, venv_depth=venv_depth)
        else:
            self._add_single_script(path, alias=alias, venv=venv, venv_depth=venv_depth)
        self._save()

    def delete_script(self, script: str):
        pass

    def get_script(self, script: str):
        pass

    def prune(self):
        pass

    def update_directories(self):
        pass

    def update_directory(self, name: str):
        pass

    def update_script(self, name: str, path: Optional[Path], alias: Optional[str]=None, venv: Optional[Path]=None):
        pass
