from pydantic import BaseModel

class Organization(BaseModel):
    id: str = ""
    # user_id who created the organization, automatically becomes the admin
    user_id: str
    name: str
    description: str
    image: str = ""
    address: str
    city: str
    country: str
    category: str
    phone: str = ""
    email: str = ""
    created_at: int = 0
    updated_at: int = 0
