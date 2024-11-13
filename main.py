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
    """Get files list by username."""
    user_dir = os.path.join(UPLOAD_DIR, username)

    if not os.path.exists(user_dir):
        raise HTTPException(status_code=404, detail="User directory not found")

    files = []
    for root, dirs, filenames in os.walk(user_dir):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append({"filename": filename, "file_path": file_path})

    return {"files": files}


@app.get("/find-mistakes")
async def create_spec(file_path: str):
    """Create a JSON file with mistakes and return the new JSON file path."""
    if not file_path:
        raise HTTPException(status_code=404, detail="Pass the file path")
    return create_word_file_mistakes(file_path)


@app.get("/get-mistakes")
async def get_mistake_specification(file_path: str):
    """Return a JSON data using mistakes file path."""
    with open(file_path, "r") as file:
        data = json.load(file)

    return data


@app.get("/file-download")
async def get_file(file_path: str):

    if os.path.exists(file_path):
        directory, filename = os.path.split(file_path)

        return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
    else:
        return {"error": "File not found"}
    pass


@app.post("/file-fix")
async def fix_file(request: Request):
    """Pass the JSON mistakes as body to get updated `.docx` file path."""

    json_data = await request.json()

    file_path = json_data["file_path"]

    file_path = copy_file(file_path)["copy_path"]

    fix_format_mistakes(file_path, json_data)

    return {"file_path": file_path}
