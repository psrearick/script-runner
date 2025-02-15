import json
from pathlib import Path
from typing import Dict, List, Optional
from script_runner.commands.add import AddScript
from script_runner.commands.delete import DeleteScript

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

    def _load_json(self, path: Path) -> List[Dict[str, str]]:
        if path.exists():
            return json.loads(path.read_text())
        return []

    def _save(self):
        self.scripts_file.write_text(json.dumps(self.scripts, indent=2))
        self.directories_file.write_text(json.dumps(self.directories, indent=2))

    def _get_venv(self, script: Path, max_depth: int = 3, depth: int = 1) -> Optional[Path]:
        if depth > max_depth:
            return None

        if not script.parent:
            return None

        venv_path = script.parent.rglob("pyvenv.cfg")

        if not venv_path:
            return self._get_venv(script=script, max_depth=max_depth, depth=depth + 1)

        return list(venv_path)[0].parent

    def delete_alias(self, alias: str):
        remover = DeleteScript(self)
        remover.delete_alias(alias)

    def delete_script(self, path: Path):
        remover = DeleteScript(self)
        remover.delete_script(path)

    def add_script(self,
                path: Path, alias: Optional[str]=None, venv: Optional[Path]=None,
                venv_depth: int = 3, force: bool = False):
        adder = AddScript(self)
        adder.add_script(path=path, alias=alias,
                        venv=venv, venv_depth=venv_depth, force=force)

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
