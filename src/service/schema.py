import pytz
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

from src.api.errors import APIValidationError
from src.api import codes

class Day(int, Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

class CreateServiceRequest(BaseModel):
    title: str = Field("", min_length=3, max_length=100)
    description: str
    category: str
    timezone: str
    start_time: int = Field(ge=0, le=23)
    end_time: int = Field(ge=0, le=23)
    # duration per session in minutes
    duration: int = Field(gt=0)
    # gap between sessions in minutes
    gap: int = Field(ge=0)
    # break time in local hour (e.g. 12 for lunch break), -1 means no break
    break_time: int = Field(ge=-1, le=23)
    # break duration in minutes
    break_duration: int = Field(ge=0)
    break_days: List[Day]
    # price per session
    price: int = Field(gt=0)
    # apointees are the people who are being appointed from the organization to provide the service
    appointees: List[str]
    slot_per_session: int = Field(gt=0)

    def check(self) -> None:
        """
        Raises APIValidationError if validation fails.
        """
        if self.start_time >= self.end_time:
            raise APIValidationError(codes.SERVICE_START_TIME_CANNOT_BE_GREATER_THAN_END_TIME, "Start_time cannot be greater than end_time")
        if self.gap >= self.duration:
            raise APIValidationError(codes.SERVICE_INVALID_GAP, "Gap cannot be greater than Duration")
        # Check timezone
        if self.timezone not in pytz.all_timezones:
            raise APIValidationError(codes.INVALID_TIMEZONE, "Invalid timezone")
        # Break days must be unique
        if len(self.break_days) != len(set(self.break_days)):
            raise APIValidationError(codes.SERVICE_NONUNIQUE_DAYS, "Break days must be unique")
        # Break time must be in range
        if self.break_time < 0:
            self.break_duration = 0
            if self.break_time < self.start_time or self.break_time > self.end_time:
                raise APIValidationError(codes.SERVICE_INVALID_BREAK_TIME, "Break time must be in range")
        # Apointees must be unique and non-empty
        if len(self.appointees) == 0:
            raise APIValidationError(codes.SERVICE_APPOINTEES_MUST_BE_FILLED, "appointees cannot be empty")
        if len(self.appointees) != len(set(self.appointees)):
            raise APIValidationError(codes.SERVICE_NONUNIQUE_APPOINTEES, "appointees must be unique")
        # Total duration cannot be greater than end time minus start time
        total_duration = self.duration + self.gap + max(self.break_duration, 0)
        if total_duration > self.end_time - self.start_time:
            raise APIValidationError(codes.SERVICE_INVALID_TOTAL_DURATION, "Total duration cannot be greater than end time minus start time")
        