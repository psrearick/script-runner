from pathlib import Path
import pytest
from script_runner.config import Registry

@pytest.fixture
def venv_path(tmp_path: Path):
    venv_path = tmp_path / "venv"
    venv_path.mkdir()
    (venv_path / "pyvenv.cfg").touch()

    return venv_path

@pytest.fixture
def test_registry(tmp_path: Path):
    """Provide a clean registry instance for each test"""
    config_dir = tmp_path / "config"
    return Registry(config_dir=config_dir)

def test_can_add_script(test_registry: Registry, tmp_path: Path):
    script_path = tmp_path / "script.py"
    script_path.touch()
    test_registry.add_script(script_path)
    assert len(test_registry.scripts) == 1

    entry = test_registry.scripts[0]
    assert entry["alias"] == "script"
    assert entry["directory_id"] == ""
    assert entry["path"] == str(script_path)
    assert entry["venv"] == ""

def test_can_add_script_with_alias(test_registry: Registry, tmp_path: Path):
    script_path = tmp_path / "script.py"
    script_path.touch()
    test_registry.add_script(script_path, alias="first_script")
    assert len(test_registry.scripts) == 1

    entry = test_registry.scripts[0]
    assert entry["alias"] == "first_script"
    assert entry["directory_id"] == ""
    assert entry["path"] == str(script_path)
    assert entry["venv"] == ""

def test_can_add_script_and_detect_venv(test_registry: Registry, tmp_path: Path, venv_path: Path):
    script_path = tmp_path / "script.py"
    script_path.touch()
    test_registry.add_script(script_path, alias="first_script")
    assert len(test_registry.scripts) == 1

    entry = test_registry.scripts[0]
    assert entry["alias"] == "first_script"
    assert entry["directory_id"] == ""
    assert entry["path"] == str(script_path)
    assert entry["venv"] == str(venv_path)
