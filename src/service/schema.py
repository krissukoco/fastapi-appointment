from pydantic import BaseModel, Field
from typing import Optional, List

class CreateServiceRequest(BaseModel):
    title: str = Field("", min_length=3, max_length=100)
    description: str
    category: str
    timezone: str
    start_time: int = Field(ge=0, le=23)
    end_time: int = Field(ge=0, le=23)
    # duration per session in minutes
    duration: int = Field(ge=0)
    # gap between sessions in minutes
    gap: int = Field(ge=0)
    # break time in local hour (e.g. 12 for lunch break)
    break_time: int = Field(ge=0)
    # break duration in minutes
    break_duration: int = Field(ge=0)
    break_days: List[str]
    # price per session
    price: int = Field(ge=0)
    # apointees are the people who are being appointed from the organization to provide the service
    apointees: List[str]
    slot_per_session: int = Field(gt=0)