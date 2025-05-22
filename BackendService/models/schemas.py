from pydantic import BaseModel
from pydantic import (
    PastDate, PositiveInt, EmailStr
)
from uuid import UUID
from pathlib import Path

class UserRequest(BaseModel):
    id: UUID
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr

class RaceRequest(BaseModel):
    id: UUID
    name: str
    date: PastDate

class RaceResponse(BaseModel):
    id: UUID
    name: str
    date: PastDate

class RegistrationRequest(BaseModel):
    user_id: UUID
    race_id: UUID
    bib_number: PositiveInt

class RegistrationResponse(BaseModel):
    user_id: UUID
    race_id: UUID
    bib_number: PositiveInt

class ImageMetadataResponse(BaseModel):
    id: UUID
    path: Path

class ImageBibsRequest(BaseModel):
    image_id: UUID
    race_id: UUID

class ImageBibsResponse(BaseModel):
    image_id: UUID
    race_id: UUID
    bib_number: PositiveInt
