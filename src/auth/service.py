import jwt
from uuid import uuid4
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
import bcrypt

from src.auth.exceptions import InvalidTokenException, ExpiredTokenException
from src.config import Config

DEFAULT_EXP_HOURS = 24 * 30
ISSUER = "fastapi-appointment"
AUDIENCE = "fastapi-appointment"

class JWTClaims(BaseModel):
    sub: str
    aud: str
    exp: int
    iat: int
    iss: str
    nbf: int
    jti: str

def new_jti() -> str:
    return "jwt_" + str(uuid4())

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=6)
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def compare_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def generate_jwt(user_id: str, exp_hours: Optional[int] = None) -> str:
    if exp_hours is None:
        exp_hours = DEFAULT_EXP_HOURS
    now_dt = datetime.utcnow()
    now = int(now_dt.timestamp()) # in second
    exp_dt = now_dt + timedelta(hours=exp_hours)
    exp = int(exp_dt.timestamp()) # in second
    
    # Build JWT standard claims
    payload = JWTClaims(
        sub=user_id,
        aud=AUDIENCE,
        exp=exp,
        iat=now,
        iss=ISSUER,
        nbf=now,
        jti=new_jti()
    )

    # Encode JWT
    enc = jwt.encode(payload.dict(), Config.JWT_SECRET, algorithm="HS256")
    return enc

def decode_jwt(token: str) -> Optional[JWTClaims]:
    dec = jwt.decode(token, Config.JWT_SECRET, audience=AUDIENCE, algorithms=["HS256"])
    # print("decoded: ", dec)
    claims = JWTClaims(**dec)
    # Validate token
    if claims.iss != ISSUER:
        raise InvalidTokenException()
    if claims.aud != AUDIENCE:
        raise InvalidTokenException()
    if claims.nbf > int(datetime.utcnow().timestamp()):
        raise InvalidTokenException()
    if claims.exp < int(datetime.utcnow().timestamp()):
        raise ExpiredTokenException()
    return claims

