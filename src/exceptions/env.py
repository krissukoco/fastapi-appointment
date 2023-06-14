class EnvNotSetException(Exception):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return f"Environment variable {self.key} is not set"