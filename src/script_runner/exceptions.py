from typing import Any

class AliasNotFoundError(Exception):
    def __init__(self, message: str="Alias not found in registry", value: Any=None):
        self.message = message
        self.value = value
        super().__init__(self.message)

class ScriptNotFoundError(Exception):
    def __init__(self, message: str="Script or directory not found in registry", value: Any=None):
        self.message = message
        self.value = value
        super().__init__(self.message)
