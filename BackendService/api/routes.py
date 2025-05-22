from fastapi import APIRouter, UploadFile, File, Form
from uuid import uuid4
import os
from BackendService.models.schemas import (
    ImageMetadataResponse,
)

router = APIRouter()
DATA_DIR = "/mnt/data/images"

# NOTE:
## FastAPI treats /route/ and /route as different!
## For consistency, use trailing slash when defining collections (e.g. /users/)
## Don't use training slash when defining individual entities (e.g. /users/{user_id})


@router.get("/users/")
async def list_users():
    pass

@router.get("/users/{user_id}")
async def get_user_by_id():
    pass

@router.post("/users/")
async def create_user():
    pass

@router.get("/races/")
async def list_races():
    pass

@router.get("/races/{race_id}")
async def get_race_by_id():
    pass

@router.get("/races/{race_id}/bibs/{bib_number}/images/")
async def list_race_images_with_bib():
    pass

@router.post("/races/")
async def create_race():
    pass

@router.get("/registrations/")
async def list_registrations():
    pass

@router.get("/registrations/{user_id}/{race_id}")
async def get_registration_by_ids():
    pass

@router.post("/registrations/")
async def register_user_to_race():
    pass


@router.get("/images/{image_id}")
async def get_image_metadata_by_id():
    pass

@router.get("/images/{image_id}/bibs/")
async def list_bibs_for_image_by_id():
    pass

@router.post("/images/")
async def upload_image():
    pass

@router.get("/image-bibs/")
async def list_image_bib_links():
    pass

@router.post("/image-bibs/")
async def link_image_to_race_and_bib():
    pass

