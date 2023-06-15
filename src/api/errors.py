from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    code: int
    message: str
    detail: Optional[dict] = None

class APIValidationError(Exception):
    def __init__(self, code: int, message: str, detail: Optional[dict] = None):
        self.code = code
        self.message = message
        self.detail = detail

def error_response(code: int, message: str, detail: Optional[dict] = None) -> dict:
    return ErrorResponse(
        code=code,
        message=message,
        detail=detail
    ).dict()