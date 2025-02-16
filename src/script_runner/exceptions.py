from pathlib import Path
from typing import Optional

class AliasNotFoundError(Exception):
    def __init__(self, message: str="Alias not found in registry", value: Optional[str]=None):
        if value:
            message = f"{message}: {value}"

        self.message = message
        self.value = value
        super().__init__(self.message)

class DuplicateAliasError(Exception):
    def __init__(self, message: str="Alias already in registry", value: Optional[str]=None):
        if value:
            message = f"{message}: {value}"

        self.message = message
        self.value = value
        super().__init__(self.message)

class ScriptNotFoundError(FileNotFoundError):
    def __init__(self, message: str="Script not found", value: Optional[str|Path]=None):
        if value:
            message = f"{message}: {value}"

        self.message = message
        self.value = value
        super().__init__(self.message)
