from pathlib import Path
from typing import Optional, Protocol
from script_runner.utils import get_venv
import pytest

@pytest.fixture
def venv_path(tmp_path: Path):
    venv_path = tmp_path / "venv"
    venv_path.mkdir()
    (venv_path / "pyvenv.cfg").touch()

    return venv_path

class ScriptGetter(Protocol):
    def __call__(self, path: Optional[str] = "") -> Path: ...

@pytest.fixture
def get_script(tmp_path: Path):
    def _get_script(path: Optional[str] = "") -> Path:
        script_dir = (tmp_path / path) if path else tmp_path
        script_dir.mkdir(parents=True, exist_ok=True)
        script_path = script_dir / "script.py"
        script_path.touch()

        return script_path

    return _get_script

def test_can_detect_venv_path(venv_path: Path, get_script: ScriptGetter):
    script_path = get_script()
    detected_venv = get_venv(script_path)
    assert detected_venv == venv_path

def test_can_detect_venv_path_for_script_in_nested_dir(venv_path: Path, get_script: ScriptGetter):
    script_path = get_script("scripts/scripts_of_type")
    detected_venv = get_venv(script_path)
    assert detected_venv == venv_path

def test_cannot_detect_venv_path_for_script_nested_deeper_than_max_depth(venv_path: Path, get_script: ScriptGetter):
    script_path = get_script("scripts/scripts_of_type/scripts/are/deeper")
    detected_venv = get_venv(script_path)
    assert detected_venv == None

def test_can_override_venv_detection_max_depth(venv_path: Path, get_script: ScriptGetter):
    script_path = get_script("scripts/scripts_of_type/scripts/are/deeper")
    detected_venv = get_venv(script_path, max_depth=0)
    assert detected_venv == venv_path
