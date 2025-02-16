from pathlib import Path
from script_runner.utils import get_venv

def test_venv_detection(tmp_path: Path):
    venv_path = tmp_path / "venv"
    venv_path.mkdir()
    (venv_path / "pyvenv.cfg").touch()

    script_path = tmp_path / "script.py"
    script_path.touch()

    detected_venv = get_venv(script_path)
    assert detected_venv == venv_path

def test_venv_detection_in_nested_dir(tmp_path: Path):
    venv_path = tmp_path / "venv"
    venv_path.mkdir()
    (venv_path / "pyvenv.cfg").touch()

    script_dir = tmp_path / "scripts" / "scripts_of_type"
    script_dir.mkdir(parents=True)
    script_path = script_dir / "script.py"
    script_path.touch()

    detected_venv = get_venv(script_path)
    assert detected_venv == venv_path

def test_venv_detection_max_depth(tmp_path: Path):
    venv_path = tmp_path / "venv"
    venv_path.mkdir()
    (venv_path / "pyvenv.cfg").touch()

    script_dir = tmp_path / "scripts" / "scripts_of_type" / "scripts" / "are" / "deeper"
    script_dir.mkdir(parents=True)
    script_path = script_dir / "script.py"
    script_path.touch()

    detected_venv = get_venv(script_path)
    assert detected_venv == None

def test_venv_detection_max_depth_override(tmp_path: Path):
    venv_path = tmp_path / "venv"
    venv_path.mkdir()
    (venv_path / "pyvenv.cfg").touch()

    script_dir = tmp_path / "scripts" / "scripts_of_type" / "scripts" / "are" / "deeper"
    script_dir.mkdir(parents=True)
    script_path = script_dir / "script.py"
    script_path.touch()

    detected_venv = get_venv(script_path, max_depth=0)
    assert detected_venv == venv_path
