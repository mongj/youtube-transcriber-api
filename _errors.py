from werkzeug.exceptions import HTTPException

class InvalidAPIUsage(HTTPException):
    def __init__(self, description, code=400):
        super().__init__()
        self.description = description
        self.code = code

class TranscriptionError(HTTPException):
    def __init__(self, description, code=500):
        super().__init__()
        self.description = description
        self.code = code