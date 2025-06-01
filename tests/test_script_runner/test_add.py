from pathlib import Path
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
    assert entry["interpreter"] == str(venv_path / "bin" / "python")
    assert entry["type"] == "python"

def test_can_add_script_with_alias(test_registry: Registry, tmp_path: Path):
    script_path = tmp_path / "script.py"
    script_path.touch()
    alias = "first_script"
    test_registry.add_script(script_path, alias=alias)
    assert len(test_registry.scripts) == 1

    entry = test_registry.scripts[0]
    assert entry["alias"] == alias
    assert entry["path"] == str(script_path)
    assert entry["interpreter"] != ""
    assert entry["type"] == "python"

def test_can_add_script_without_python(test_registry: Registry, tmp_path: Path):
    script_path = tmp_path / "script.py"
    script_path.touch()
    test_registry.add_script(script_path)
    assert len(test_registry.scripts) == 1

    entry = test_registry.scripts[0]
    assert entry["alias"] == script_path.stem
    assert entry["path"] == str(script_path)
    assert entry["interpreter"] != ""
    assert not Path(entry["interpreter"]).is_relative_to(tmp_path)
    assert entry["type"] == "python"

def test_can_add_script_and_detect_venv(test_registry: Registry, tmp_path: Path, venv_path: Path):
    script_path = tmp_path / "script.py"
    script_path.touch()
    test_registry.add_script(script_path)
    assert len(test_registry.scripts) == 1

    entry = test_registry.scripts[0]
    assert entry["alias"] == script_path.stem
    assert entry["path"] == str(script_path)
    assert entry["interpreter"] == str(venv_path / "bin" / "python")
    assert entry["type"] == "python"

def test_can_add_shell_script(test_registry: Registry, tmp_path: Path):
    script_path = tmp_path / "script.sh"
    script_path.write_text("#!/bin/bash\necho 'Hello World'")
    test_registry.add_script(script_path)
    assert len(test_registry.scripts) == 1

    entry = test_registry.scripts[0]
    assert entry["alias"] == script_path.stem
    assert entry["path"] == str(script_path)
    assert entry["interpreter"] != ""
    assert entry["type"] == "shell"

def test_can_detect_script_type_from_shebang(test_registry: Registry, tmp_path: Path):
    # Test Python script without .py extension
    python_script = tmp_path / "python_script"
    python_script.write_text("#!/usr/bin/env python3\nprint('hello')")
    test_registry.add_script(python_script, alias="py_test")

    # Test shell script without .sh extension
    shell_script = tmp_path / "shell_script"
    shell_script.write_text("#!/bin/bash\necho 'hello'")
    test_registry.add_script(shell_script, alias="sh_test")

    assert len(test_registry.scripts) == 2

    py_entry = next(s for s in test_registry.scripts if s["alias"] == "py_test")
    sh_entry = next(s for s in test_registry.scripts if s["alias"] == "sh_test")

    assert py_entry["type"] == "python"
    assert sh_entry["type"] == "shell"

def test_can_add_script_with_custom_interpreter(test_registry: Registry, tmp_path: Path):
    script_path = tmp_path / "script.py"
    script_path.touch()
    custom_interpreter = tmp_path / "custom_python"
    custom_interpreter.touch()
    custom_interpreter.chmod(0o755)

    test_registry.add_script(script_path, interpreter_path=custom_interpreter)
    assert len(test_registry.scripts) == 1

    entry = test_registry.scripts[0]
    assert entry["interpreter"] == str(custom_interpreter)
    assert entry["type"] == "python"
