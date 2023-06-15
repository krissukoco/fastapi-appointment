from fastapi import APIRouter, HTTPException, Depends

from src.auth.middleware import user_id_authorization
from src.api.errors import error_response
from src.api import codes
from src.organization.schema import CreateOrganizationRequest
from src.organization.model import Organization
from src.user.service import get_user_by_id, update_user
from src.organization.service import \
    get_organization_by_id as get_by_id, \
    get_organization_by_user_id as get_by_user_id, \
    insert_organization as create

r = APIRouter()

@r.get("", response_model=Organization)
def get_users_organization(user_id: str = Depends(user_id_authorization)):
    # Get user's organization id
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail=error_response(
            code=codes.EXPIRED_TOKEN,
            message="Token expired",
        ))
    if user.organization_id == "":
        raise HTTPException(status_code=404, detail=error_response(
            code=codes.ORGANIZATION_NOT_FOUND,
            message="Organization not found",
        ))
    # Get organization
    org = get_by_id(user.organization_id)
    if org is None:
        raise HTTPException(status_code=404, detail=error_response(
            code=codes.ORGANIZATION_NOT_FOUND,
            message="Organization not found"
        ))
    return org

@r.get("/{id}", response_model=Organization)
def get_organization_by_id(id: str):
    org = get_by_id(id)
    if org is None:
        raise HTTPException(status_code=404, detail=error_response(
            code=codes.ORGANIZATION_NOT_FOUND,
            message="Organization not found",
        ))
    return org

@r.post("", response_model=Organization)
def create_organization(req: CreateOrganizationRequest, user_id: str = Depends(user_id_authorization)):
    # Get user's organization id
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail=error_response(
            code=codes.EXPIRED_TOKEN,
            message="Token expired",
        ))
    if user.organization_id != "":
        raise HTTPException(status_code=400, detail=error_response(
            code=codes.USER_ALREADY_HAS_ORGANIZATION,
            message="User already in organization",
        ))
    # Create organization
    org = Organization(
        name=req.name,
        user_id=user_id,
        description=req.description,
        address=req.address,
        city=req.city,
        country=req.country,
        category=req.category,
        phone=req.phone,
        email=req.email,
    )
    create(org)

    # Update user
    user.organization_id = org.id
    user.role = "admin"
    update_user(user)

    return org

