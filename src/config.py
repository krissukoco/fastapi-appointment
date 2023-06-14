import os

class Config:
    JWT_SECRET: str = os.environ['JWT_SECRET']