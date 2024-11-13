from fastapi import FastAPI, File, UploadFile, HTTPException
from services.file_upload import save_uploaded_file
import os
from settrings import UPLOAD_DIR

app = FastAPI()

os.makedirs("uploads", exist_ok=True)


@app.post("/file-upload")
async def upload_file(file: UploadFile = File(...), username: str = "none"):
    """Endpoint to upload `.docx` file."""

    file_path = save_uploaded_file(file, username)

    if not file_path:
        raise HTTPException(status_code=500, detail="Failed to upload file")

    return {"filename": file.filename, "file_path": file_path}


@app.get("/files/{username}")
async def get_files(username: str):
    user_dir = os.path.join(UPLOAD_DIR, username)

    if not os.path.exists(user_dir):
        raise HTTPException(status_code=404, detail="User directory not found")

    files = []
    for root, dirs, filenames in os.walk(user_dir):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append({"filename": filename, "file_path": file_path})

    return {"files": files}
