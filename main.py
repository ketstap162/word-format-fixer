from fastapi import FastAPI, File, UploadFile, HTTPException
from services.file_upload import save_uploaded_file
import os


app = FastAPI()

os.makedirs("uploads", exist_ok=True)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint to upload file."""

    file_path = save_uploaded_file(file)

    if not file_path:
        raise HTTPException(status_code=500, detail="Failed to upload file")

    return {"filename": file.filename, "file_path": file_path}
