import json
from pathlib import Path
from typing import Dict, List, Optional
from .exceptions import ScriptNotFoundError
from .commands.add import AddScript
from .commands.delete import DeleteScript

class Registry:
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / ".config" / "script_runner"
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

    def save(self):
        self.scripts_file.write_text(json.dumps(self.scripts, indent=2))
        self.directories_file.write_text(json.dumps(self.directories, indent=2))

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

    def get_script(self, identifier: str) -> Dict[str, str]:
        alias_match: List[Dict[str, str]] = []

        for script in self.scripts:
            if script["path"] == identifier:
                return script

            if identifier == script["alias"]:
                alias_match.append(script)

        if len(alias_match) == 1:
            return alias_match[0]

        raise ScriptNotFoundError

    def prune(self):
        pass

    def update_directories(self):
        pass

    def update_directory(self, name: str):
        pass

    def update_script(self, name: str, path: Path, alias: Optional[str]=None, venv: Optional[Path]=None):
        # script = self.get_script(name)

        # script.update({
        #     "path": str(path),
        #     "alias": alias if alias else path.stem,
        #     "venv": str(venv) if venv else str(get_venv(path))
        # })
        pass
