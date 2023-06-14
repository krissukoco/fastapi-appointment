from fastapi import APIRouter, HTTPException

from src.api.errors import error_response
from src.user.service import get_user_by_id
from src.user.model import User

r = APIRouter()

@r.get("/{id}", response_model=User)
def get_user(id: str):
    user = get_user_by_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail=error_response(
            code=404,
            message="User not found",
        ))
    return user