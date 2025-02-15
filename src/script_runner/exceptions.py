class AliasNotFoundError(Exception):
    def __init__(self, message="Alias not found in registry", value=None):
        self.message = message
        self.value = value
        super().__init__(self.message)

class ScriptNotFoundError(Exception):
    def __init__(self, message="Script or directory not found in registry", value=None):
        self.message = message
        self.value = value
        super().__init__(self.message)
