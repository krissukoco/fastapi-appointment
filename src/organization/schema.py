from pydantic import BaseModel, Field

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

class CreateOrganizationRequest(BaseModel):
    name: str
    description: str = Field("", max_length=300)
    address: str = Field(max_length=100, min_length=3)
    city: str = Field(max_length=50, min_length=2)
    country: str = Field(max_length=20, min_length=2)
    category: str
    phone: str = ""
    email: str = ""