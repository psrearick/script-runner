from pathlib import Path
from typing import Optional

def get_venv(script: Path, max_depth: int = 3, depth: int = 1) -> Optional[Path]:
    if depth > max_depth:
        return None

    if not script.parent:
        return None

    venv_path_matches = list(script.parent.rglob("pyvenv.cfg"))

    if not any(venv_path_matches):
        return get_venv(script=script.parent, max_depth=max_depth, depth=depth + 1)

    return list(venv_path_matches)[0].parent

def path_distance(path1: Path, path2: Path):
    """
    Calculate the distance between two file paths.
    """
    abs_path1 = path1.resolve()
    abs_path2 = path2.resolve()

    path1_parts = abs_path1.parts
    path2_parts = abs_path2.parts

    min_len = min(len(path1_parts), len(path2_parts))
    common_prefix_len = 0

    for i in range(min_len):
        if path1_parts[i] == path2_parts[i]:
            common_prefix_len += 1
        else:
            break

    distance = (len(path1_parts) - common_prefix_len) + (len(path2_parts) - common_prefix_len)

    return distance
