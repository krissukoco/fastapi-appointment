from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field

from src.api.errors import error_response
from src.user.service import get_user_by_email, get_user_by_id, insert_user
from src.user.model import User
from src.auth.service import compare_password, hash_password
from src.auth.service import generate_jwt, decode_jwt
from src.auth.middleware import user_id_authorization

r = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    phone: str
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    address: str = Field(min_length=3, max_length=100)

@r.post("/register", response_model=User)
def register(req: RegisterRequest):
    # Check if email is already registered
    user = get_user_by_email(str(req.email))
    if user is not None:
        raise HTTPException(status_code=400, detail=error_response(
            code=400,
            message="Email already registered",
        ))
    
    # Validate input
    if req.password != req.confirm_password:
        raise HTTPException(status_code=400, detail=error_response(
            code=400,
            message="Password and confirm password must match",
        ))
    
    # Insert user into database
    hashed_pwd = hash_password(str(req.password))
    user = User(
        email=str(req.email),
        password=hashed_pwd,
        phone=str(req.phone),
        first_name=str(req.first_name),
        last_name=str(req.last_name),
        address=str(req.address),
        role="unknown",
    )
    insert_user(user)

    return user

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    user: User
    token: str

@r.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    print(req)
    # Get user
    user = get_user_by_email(str(req.email))
    print(user)
    if user is None:
        raise HTTPException(status_code=400, detail=error_response(
            code=400,
            message="Email or password is incorrect",
        ))
    # Compare password
    print(user.password)
    if not compare_password(str(req.password), user.password):
        raise HTTPException(status_code=400, detail=error_response(
            code=400,
            message="Email or password is incorrect",
        ))
    # Generate JWT
    jwt = generate_jwt(user.id)

    return LoginResponse(
        user=user,
        token=jwt
    )

@r.get("/account", response_model=User)
def get_account(user_id: str = Depends(user_id_authorization)):
    print("user id: ", user_id)
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=409, detail=error_response(
            code=409,
            message="User not found",
        ))
    return user