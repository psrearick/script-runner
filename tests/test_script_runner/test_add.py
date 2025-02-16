from pathlib import Path
import sys
import pytest
from script_runner.config import Registry

@pytest.fixture
def venv_path(tmp_path: Path):
    venv_path = tmp_path / "venv"
    venv_path.mkdir()
    (venv_path / "bin").mkdir()
    (venv_path / "pyvenv.cfg").touch()
    (venv_path / "bin" / "python").touch()

    return venv_path

@pytest.fixture
def test_registry(tmp_path: Path):
    """Provide a clean registry instance for each test"""
    config_dir = tmp_path / "config"
    return Registry(config_dir=config_dir)

def test_can_add_script(test_registry: Registry, tmp_path: Path, venv_path: Path):
    script_path = tmp_path / "script.py"
    script_path.touch()
    test_registry.add_script(script_path)
    assert len(test_registry.scripts) == 1

    entry = test_registry.scripts[0]
    assert entry["alias"] == script_path.stem
    assert entry["path"] == str(script_path)
    assert entry["python"] == str(venv_path / "bin" / "python")

def test_can_add_script_with_alias(test_registry: Registry, tmp_path: Path):
    script_path = tmp_path / "script.py"
    script_path.touch()
    alias = "first_script"
    test_registry.add_script(script_path, alias=alias)
    assert len(test_registry.scripts) == 1

    entry = test_registry.scripts[0]
    assert entry["alias"] ==alias
    assert entry["path"] == str(script_path)
    assert entry["python"] is not ""

def test_can_add_script_without_python(test_registry: Registry, tmp_path: Path):
    script_path = tmp_path / "script.py"
    script_path.touch()
    test_registry.add_script(script_path)
    assert len(test_registry.scripts) == 1

    entry = test_registry.scripts[0]
    assert entry["alias"] == script_path.stem
    assert entry["path"] == str(script_path)
    assert entry["python"] is not ""
    assert not Path(entry["python"]).is_relative_to(tmp_path)

def test_can_add_script_and_detect_venv(test_registry: Registry, tmp_path: Path, venv_path: Path):
    script_path = tmp_path / "script.py"
    script_path.touch()
    test_registry.add_script(script_path)
    assert len(test_registry.scripts) == 1

    entry = test_registry.scripts[0]
    assert entry["alias"] == script_path.stem
    assert entry["path"] == str(script_path)
    assert entry["python"] == str(venv_path / "bin" / "python")
