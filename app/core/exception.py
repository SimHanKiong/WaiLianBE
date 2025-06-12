class IntegrityException(Exception):
    def __init__(self, model_name: str):
        self.model_name = model_name

    def __str__(self):
        return f"A related record of {self.model_name} is missing."


class UniqueViolationException(Exception):
    def __init__(self, model_name: str):
        self.model_name = model_name

    def __str__(self):
        return f"Duplicate {self.model_name} detected."


class MissingRecordException(Exception):
    def __init__(self, model_name: str):
        self.model_name = model_name

    def __str__(self):
        return f"{self.model_name} not found."
