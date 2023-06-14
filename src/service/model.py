from pydantic import BaseModel, Field
from enum import Enum

class Day(int, Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

class Service(BaseModel):
    id: str
    organization_id: str
    title: str
    description: str
    category: str
    image: str
    # start time of the first session in a day in local time (e.g. 9)
    timezone: str
    start_time: int = Field(ge=0, le=23)
    # end time of the last session in a day in local time (e.g. 17)
    end_time: int = Field(ge=0, le=23)
    # duration per session in minutes
    duration: int = Field(ge=0)
    # gap between sessions in minutes
    gap: int = Field(ge=0)
    # break time in local hour (e.g. 12 for lunch break)
    break_time: int = Field(ge=0)
    # break duration in minutes
    break_duration: int = Field(ge=0)
    break_days: str = ""
    # price per session
    price: int = Field(ge=0)
    slot_per_session: int = Field(gt=0)
    created_at: int
    updated_at: int

class UserService(BaseModel):
    """
    User to Service relation \n
    That is, each record represents a user's 
    """
    id: str
    user_id: str
    service_id: str
    created_at: int
    updated_at: int