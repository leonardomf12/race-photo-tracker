# Pydantic models for validation (request/response bodies)

from pydantic import BaseModel, ConfigDict
from pydantic import (
    PositiveInt, EmailStr
)
from uuid import UUID
from pathlib import Path
from datetime import date

# class UserRequest(BaseModel):
#     id: int
#     name: str
#     email: EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr

# class RaceRequest(BaseModel):
#     id: int
#     name: str
#     date: date

class RaceCreate(BaseModel):
    name: str
    date: date

class RaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    date: date

class RegistrationCreate(BaseModel):
    user_id: int
    race_id: int
    bib_number: PositiveInt

class RegistrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    race_id: int
    bib_number: PositiveInt

class ImageMetadataResponse(BaseModel):
    id: int
    path: Path

class ImageBibsRequest(BaseModel):
    image_id: int
    race_id: int

class ImageBibsResponse(BaseModel):
    image_id: int
    race_id: int
    bib_number: PositiveInt
