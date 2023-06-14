from pydantic import BaseModel

class CreateAppointmentRequest(BaseModel):
    service_id: str
    # session_start is a timestamp that represents the start of the session
    session_start: int
    apointee_id: str
    customer_name: str
    customer_phone: str
    customer_email: str
    