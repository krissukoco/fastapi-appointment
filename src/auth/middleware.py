from fastapi import Request, HTTPException, Security
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware

from src.api.errors import error_response
from src.auth.service import decode_jwt
from src.auth.exceptions import ExpiredTokenException, InvalidTokenException

_auth_header = HTTPBearer(
    scheme_name="Authorization",
    auto_error=False
)

def user_id_authorization(cred: HTTPAuthorizationCredentials = Security(_auth_header)) -> str:
    """
    Get Authorization header, and parse the token.
    Check claims validity then return user id (sub claim)
    """
    if cred is None:
        raise HTTPException(status_code=401, detail=error_response(
            code=401,
            message="Unauthorized",
        ))
    if cred.scheme != "Bearer":
        raise HTTPException(status_code=401, detail=error_response(
            code=401,
            message="Unsupported authorization scheme",
        ))
    
    try:
        claims = decode_jwt(cred.credentials)
    except ExpiredTokenException:
        raise HTTPException(status_code=401, detail=error_response(
            code=401,
            message="Token expired",
        ))
    except InvalidTokenException:
        raise HTTPException(status_code=401, detail=error_response(
            code=401,
            message="Invalid token",
        ))
    except Exception as e:
        print("Error while decoding JWT:", e)
        raise HTTPException(status_code=401, detail=error_response(
            code=401,
            message="Invalid token",
        ))
    
    return claims.sub
