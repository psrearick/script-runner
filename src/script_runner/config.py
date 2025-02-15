import json
from pathlib import Path
from typing import Optional
from uuid import uuid4
from enum import Enum
import click

class AddResponse(Enum):
    SKIP = 1
    CANCEL = 2
    ADDED = 3
    FAILED = 4

class ScriptNotFoundError(Exception):
    def __init__(self, message="Script or directory not found in registry", value=None):
        self.message = message
        self.value = value
        super().__init__(self.message)

class Registry:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "script_runner"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.scripts_file = self.config_dir / "scripts.json"
        self.directories_file = self.config_dir / "directories.json"
        self._load()

    def _load(self):
        self.scripts: list = self._load_json(self.scripts_file)
        self.directories: list = self._load_json(self.directories_file)

    def _load_json(self, path: Path):
        if path.exists():
            return json.loads(path.read_text())
        return {}

    def _save(self):
        self.scripts_file.write_text(json.dumps(self.scripts, indent=2))
        self.directories_file.write_text(json.dumps(self.directories, indent=2))

    def _get_venv(self, script: Path, max_depth: int = 3, depth = 1) -> Optional[Path]:
        if depth > max_depth:
            return None

        if not script.parent:
            return None

        venv_path = script.parent.rglob("pyvenv.cfg")

        if not venv_path:
            return self._get_venv(script=script, max_depth=max_depth, depth=depth + 1)

        return list(venv_path)[0].parent()

    def _verify_single_matching_path(self, script: Path, alias: str, dir_id: Optional[str] = None) -> AddResponse:
        options = ["Cancel", "Overwrite Existing Alias", "Create Another Alias"]

        if dir_id:
            options.append("Skip")

        options_string = "\n".join([f"[{i + 1}] {option}" for i, option in enumerate(options)])
        alias_exists: int = click.prompt(
            f"""
            The script "{script}" already has an alias: {alias}.
            What do you want to do?\n\n{ options_string }\n\nSelection""",
            type=click.IntRange(1, len(options))
        )

        selection = options[alias_exists]
        if selection == "Skip":
            return AddResponse.SKIP
        if selection == "Cancel":
            return AddResponse.CANCEL
        if selection == "Overwrite Existing Alias":
            self.delete_alias(alias)

        return AddResponse.ADDED

    def _verify_multiple_matching_paths(self, script: Path, aliases: list, dir_id: Optional[str] = None) -> AddResponse:
        options = ["Cancel", "Remove Existing Aliases", "Create Another Alias"]

        if dir_id:
            options.append("Skip")

        options_string = "\n".join([f"[{i + 1}] {option}" for i, option in enumerate(options)])
        alias_exists: int = click.prompt(
            f"""
            The script "{script}" already has aliases: {", ".join(aliases)}.
            What do you want to do?\n\n{ options_string }\n\nSelection""",
            type=click.IntRange(1, len(options))
        )

        selection = options[alias_exists]
        if selection == "Skip":
            return AddResponse.SKIP
        if selection == "Cancel":
            return AddResponse.CANCEL
        if selection == "Overwrite Existing Aliases":
            for alias in aliases:
                self.delete_alias(alias)

        return AddResponse.ADDED

    def _validate_alias_to_add(self, alias: str, force: bool = False, dir_id: Optional[str] = None) -> AddResponse:
        if alias in [s.alias for s in self.scripts] and not force:
            options = ["Cancel", "Overwrite"]
            if dir_id:
                options.append("Skip")
            options_string = "\n".join([f"[{i + 1}] {option}" for i, option in enumerate(options)])
            alias_exists: int = click.prompt(
                f"The alias \"{alias}\" already exists. What do you want to do?\n\n{ options_string }\n\nSelection",
                type=click.IntRange(1, len(options))
            )

            selection = options[alias_exists]
            if selection == "Skip":
                return AddResponse.SKIP
            if selection == "Cancel":
                return AddResponse.CANCEL

        return AddResponse.ADDED

    def _validate_path_to_add(self, script: Path, force: bool = False, dir_id: Optional[str] = None) -> AddResponse:
        existing_paths = [s for s in self.scripts if s.path == str(script)]

        if not existing_paths:
            return AddResponse.ADDED

        if len(existing_paths) == 1 and not force:
            return self._verify_single_matching_path(script, existing_paths[0]["alias"], dir_id)

        return self._verify_multiple_matching_paths()

    def _add_single_script(self,
            script: Path, alias: Optional[str] = None, dir_id: Optional[str] = None,
            venv: Optional[Path] = None, venv_depth: int = 3, force: bool = False) -> AddResponse:
        if not alias:
            alias = script.stem

        validated_alias = self._validate_alias_to_add(alias, force, dir_id)
        if validated_alias != AddResponse.ADDED:
            return validated_alias

        validated_paths = self._validate_path_to_add()
        if validated_paths != AddResponse.ADDED:
            return validated_paths

        if not venv:
            venv = self._get_venv(script, max_depth = venv_depth, depth = 1)

        self.scripts.append({
            "path": str(script),
            "alias": alias,
            "directory_id": dir_id,
            "venv": venv,
        })

        return AddResponse.ADDED

    def add_script(self,
                path: Path, alias: Optional[str]=None, venv: Optional[Path]=None,
                venv_depth: int = 3, force: bool = False):
        if path.is_dir():
            dir_id = str(uuid4())
            self.directories[dir_id] = {
                "path": str(path),
                "venv": str(venv) if venv else None
            }
            for script in path.rglob("*.py"):
                self._add_single_script(script, dir_id=dir_id, venv=venv, venv_depth=venv_depth, force=force)
        else:
            self._add_single_script(path, alias=alias, venv=venv, venv_depth=venv_depth, force=force)
        self._save()

    def delete_alias(self, alias: str):
        pass

    def delete_script(self, script: str):
        raise ScriptNotFoundError

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
