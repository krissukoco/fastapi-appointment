from pydantic import BaseModel, Field

class User(BaseModel):
    """
    Representation of user table in the database
    """
    id: str = ""
    organization_id: str = ""
    email: str
    password: str = Field("", exclude=True)
    phone: str
    first_name: str
    last_name: str
    image: str = ""
    role: str
    address: str = ""
    created_at: int = 0
    updated_at: int = 0