from enum import Enum
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING
from uuid import uuid4
import click
from ..utils import get_venv

if TYPE_CHECKING:
    from ..config import Registry


class AddResponse(Enum):
    SKIP = 1
    CANCEL = 2
    ADDED = 3
    FAILED = 4

class AddScript():
    def __init__(self, registry: "Registry"):
        self.registry = registry

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
            self.registry.delete_alias(alias)

        return AddResponse.ADDED

    def _verify_multiple_matching_paths(self, script: Path, aliases: List[str], dir_id: Optional[str] = None) -> AddResponse:
        options = ["Cancel", "Remove Existing Aliases Before Adding", "Create Another Alias"]

        if dir_id:
            options.append("Skip")

        options_string = "\n".join([f"[{i + 1}] {option}" for i, option in enumerate(options)])
        alias_exists: int = click.prompt(
            f"""
            The script "{script}" already has aliases: {", ".join(aliases)}.\n
            What do you want to do?\n\n{ options_string }\n\nSelection""",
            type=click.IntRange(1, len(options))
        )

        selection = options[alias_exists]
        if selection == "Skip":
            return AddResponse.SKIP
        if selection == "Cancel":
            return AddResponse.CANCEL
        if selection == "Remove Existing Aliases Before Adding":
            self.registry.delete_script(script)

        return AddResponse.ADDED

    def _validate_alias_to_add(self, alias: str, force: bool = False, dir_id: Optional[str] = None) -> AddResponse:
        if alias in [s["alias"] for s in self.registry.scripts] and not force:
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
        existing_path_aliases = [s["alias"] for s in self.registry.scripts if s["path"] == str(script)]

        if not existing_path_aliases:
            return AddResponse.ADDED

        if len(existing_path_aliases) == 1 and not force:
            return self._verify_single_matching_path(script, existing_path_aliases[0], dir_id)

        return self._verify_multiple_matching_paths(script, existing_path_aliases, dir_id)

    def _add_single_script(self,
            script: Path, alias: Optional[str] = None, dir_id: Optional[str] = None,
            venv: Optional[Path] = None, venv_depth: int = 3, force: bool = False) -> AddResponse:
        if not alias:
            alias = script.stem

        validated_alias = self._validate_alias_to_add(alias, force, dir_id)
        if validated_alias != AddResponse.ADDED:
            return validated_alias

        validated_paths = self._validate_path_to_add(script, force, dir_id)
        if validated_paths != AddResponse.ADDED:
            return validated_paths

        if not venv:
            venv = get_venv(script, max_depth = venv_depth, depth = 1)

        self.registry.scripts.append({
            "path": str(script),
            "alias": alias,
            "directory_id": dir_id if dir_id else "",
            "venv": str(venv),
        })

        return AddResponse.ADDED

    def add_script(self,
                path: Path, alias: Optional[str]=None, venv: Optional[Path]=None,
                venv_depth: int = 3, force: bool = False):
        if path.is_dir():
            dir_id = str(uuid4())
            self.registry.directories.append({
                "id": dir_id,
                "path": str(path),
                "venv": str(venv) if venv else ""
            })
            for script in path.rglob("*.py"):
                self._add_single_script(script, dir_id=dir_id, venv=venv, venv_depth=venv_depth, force=force)
        else:
            self._add_single_script(path, alias=alias, venv=venv, venv_depth=venv_depth, force=force)

        self.registry.save()
