from pydantic import BaseModel

class Appointment(BaseModel):
    id: str = ""
    organization_id: str
    # Apointee is the person who is being appointed from the organization to provide the service
    apointee_id: str
    service_id: str
    # User is the person who is requesting the service
    # user_id is the id of the user who orders the service
    user_id: str
    # Customer is the person who is receiving the service
    # Can be different from the user -> user order service for someone else
    customer_name: str
    customer_phone: str
    customer_email: str
    title: str
    start_at: int
    end_at: int
    status: str
    price: int
    paid: bool = False
    created_at: int = 0
    updated_at: int = 0