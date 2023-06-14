from fastapi import APIRouter, HTTPException

from src.api.errors import error_response
from src.appointment.service import \
    get_appointment_by_id as get_by_id, \
    get_appointments_by_organization as get_by_organization

r = APIRouter()

@r.get("/{id}")
def get_appointment_by_id(id: str):
    a = get_by_id(id)
    if a is None:
        raise HTTPException(status_code=404, detail=error_response(
            code=404,
            message="Appointment not found",
        ))
    return {"id": id}