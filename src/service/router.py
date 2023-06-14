from fastapi import APIRouter, HTTPException, Depends
from typing import List

from src.api import codes
from src.auth.middleware import user_id_authorization
from src.api.errors import error_response
from src.service.model import Service
from src.service.schema import CreateServiceRequest
from src.service.service import get_service_by_id, get_services_by_organization_id

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
    pass
