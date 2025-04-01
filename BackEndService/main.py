from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path
from pydantic import BaseModel, PositiveInt

app = FastAPI()
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)  # Create folder if not exists

class UserData(BaseModel):
    race_name: str
    bib_number: PositiveInt

@app.post("/submit-data")
def receive_data(user: UserData):
    return {"message": f"Received data for {user.race_name} -> {user.bib_number}"}


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_path = UPLOAD_FOLDER / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "message": "Upload successful!"}
