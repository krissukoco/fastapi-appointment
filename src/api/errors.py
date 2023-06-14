from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    code: int
    message: str
    detail: Optional[dict] = None

def error_response(code: int, message: str, detail: Optional[dict] = None) -> dict:
    return ErrorResponse(
        code=code,
        message=message,
        detail=detail
    ).dict()