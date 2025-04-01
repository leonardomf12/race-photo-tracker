import os
from pathlib import Path
import shutil
import json
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from pydantic import BaseModel, PositiveInt

import database_tools

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)  # Create folder if not exists

app = FastAPI()

# pydantic
class UserData(BaseModel):
    email: str
    bib_number: PositiveInt

@app.post("/submit-data")
def submit_data(user: UserData):

    if database_tools.get_user_by_email(user.email) is None:
        # TODO: register if not present
        return {"message": f"{user.email} is not registered"}

    images = database_tools.get_images_by_bib_number(user.bib_number)
    return {"message": f"Received data for {user.email} @ BIB {user.bib_number} -> {images}"}


@app.post("/upload")
async def upload(
        file: UploadFile = File(...),
        metadata: str = Form(...),
):
    metadata = json.loads(metadata)
    file_path = UPLOAD_FOLDER / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # TODO: save image data to correct place (see DataService)
    try:
        database_tools.register_new_image(
            path=str(file_path),
            email=metadata.get("email"),
            bib_number=metadata.get("bib_number"),
        )
        return {"filename": file.filename, "message": "Upload successful!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:  # FIXME: used for debugging, should not be here
        users = database_tools.get_all_users()
        print(user for user in users)
