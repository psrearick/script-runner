from pathlib import Path
from script_runner.config import Registry
from script_runner.exceptions import AliasNotFoundError, ScriptNotFoundError

class DeleteScript():
    def __init__(self, registry: Registry):
        self.registry = registry

    def delete_alias(self, alias: str):
        for idx, script in enumerate(self.registry.scripts):
            if script["alias"] == alias:
                del self.registry.scripts[idx]
                return

        raise AliasNotFoundError

    def delete_script(self, path: Path):
        delete_count = 0
        try:
            delete_script_path = path.resolve()
        except:
            raise ScriptNotFoundError

        for idx in range(len(self.registry.scripts) - 1, -1, -1):
            script = self.registry.scripts[idx]
            script_path = Path(script["path"]).resolve()
            if delete_script_path.is_dir():
                if not script_path.is_relative_to(delete_script_path):
                    continue

                del self.registry.scripts[idx]
                delete_count += 1
                continue

            if script_path == delete_script_path:
                del self.registry.scripts[idx]
                delete_count += 1
                break

        if delete_count == 0:
            raise ScriptNotFoundError
