from fastapi import APIRouter, HTTPException, Depends
from typing import List

from src.api import codes
from src.api.errors import APIValidationError
from src.auth.middleware import user_id_authorization
from src.api.errors import error_response
from src.organization.service import get_organization_by_id
from src.service.model import Service, UserService
from src.service.schema import CreateServiceRequest
from src.service.service import get_service_by_id, get_services_by_organization_id, \
    create_service, create_user_service
from src.user.service import get_user_by_id, get_user_by_id_and_organization

r = APIRouter()

@r.get("", response_model=List[Service])
def get_services(organization_id: str):
    services = get_services_by_organization_id(organization_id)
    return services

@r.get("/{id}", response_model=Service)
def get_service_by_id(id: str):
    service = get_service_by_id(id)
    if service is None:
        raise HTTPException(status_code=404, detail=error_response(
            code=codes.SERVICE_NOT_FOUND,
            message="Service not found",
        ))
    return service

@r.post("", response_model=Service)
def create_service(req: CreateServiceRequest, user_id: str = Depends(user_id_authorization)):
    # Get user
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail=error_response(
            code=codes.EXPIRED_TOKEN,
            message="Token expired",
        ))
    # User has to be an admin
    if user.role != "admin":
        raise HTTPException(status_code=403, detail=error_response(
            code=codes.FORBIDDEN,
            message="Forbidden",
        ))
    # Get user's organization
    if user.organization_id == "":
        raise HTTPException(status_code=400, detail=error_response(
            code=codes.USER_HAS_NO_ORGANIZATION,
            message="User has no organization",
        ))
    organization = get_organization_by_id(user.organization_id)
    if organization is None:
        raise HTTPException(status_code=404, detail=error_response(
            code=codes.ORGANIZATION_NOT_FOUND,
            message="Organization not found",
        ))
    # Validations
    try:
        req.check()
    except APIValidationError as e:
        raise HTTPException(status_code=400, detail=error_response(
            code=e.code,
            message=e.message,
            detail=e.detail,
        ))
    # Check if all appointees are in the organization
    for appointee_id in req.appointees:
        u = get_user_by_id_and_organization(appointee_id, user.organization_id)
        if u is None:
            raise HTTPException(status_code=400, detail=error_response(
                code=codes.SERVICE_APPOINTEE_NOT_FOUND,
                message="Appointee not found",
                detail=f"Appointee {appointee_id} is not in organization",
            ))
    # Create service
    service = Service(
        organization_id=user.organization_id,
        title=req.title,
        description=req.description,
        category=req.category,
        timezone=req.timezone,
        start_time=req.start_time,
        end_time=req.end_time,
        duration=req.duration,
        gap=req.gap,
        break_time=req.break_time,
        break_duration=req.break_duration,
        break_days=",".join(str(day.value) for day in req.break_days),
        price=req.price,
        slot_per_session=req.slot_per_session,
    )
    create_service(service)

    # Create user services
    for appointee_id in req.appointees:
        user_service = UserService(
            user_id=appointee_id,
            service_id=service.id,
        )
        create_user_service(user_service)
    return service