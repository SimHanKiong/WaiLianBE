class IntegrityException(Exception):
    def __init__(self, model_name: str):
        self.model_name = model_name

    def __str__(self):
        return f"Invalid data for {self.model_name}."


class MissingRecordException(Exception):
    def __init__(self, model_name: str):
        self.model_name = model_name

    def __str__(self):
        return f"{self.model_name} not found."
