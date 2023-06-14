from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import os
# import uvicorn

from src.api.errors import ErrorResponse
from src.auth.router import r as auth_router
from src.user.router import r as user_router
from src.organization.router import r as organization_router
from src.appointment.router import r as appointment_router
from src.service.router import r as service_router

def get_port() -> int:
    portEnv = os.environ.get("PORT", "8000")
    try:
        return int(portEnv)
    except ValueError:
        return 8000

app = FastAPI(
    title="Appointment API",
    description="API for managing appointments, built with FastAPI",
    contact={"name": "Kris Sukoco", "email": "kristianto.sukoco@gmail.com", "github": "github.com/krissukoco"}
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    detail = exc.detail
    if isinstance(detail, ErrorResponse):
        return JSONResponse({ "code": detail.code, "message": detail.message }, status_code=exc.status_code)
    try:
        return JSONResponse(detail, status_code=exc.status_code)
    except:
        return JSONResponse({ "message": "ERROR" }, status_code=exc.status_code)
    
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse({ "code": 422, "message": "Invalid request", "detail": exc.detail }, status_code=422)

v1 = APIRouter(
    prefix="/api/v1",
)

@v1.get("/ping", tags=['healthcheck'])
def ping():
    return {"message": "pong"}

v1.include_router(auth_router, prefix="/auth", tags=["Auth"])
v1.include_router(user_router, prefix="/user", tags=["User"])
v1.include_router(organization_router, prefix="/organizations", tags=["Organization"])
v1.include_router(service_router, prefix="/services", tags=["Service"])
v1.include_router(appointment_router, prefix="/appointments", tags=["Appointment"])

app.include_router(v1)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=get_port())