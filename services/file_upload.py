import shutil
from fastapi import UploadFile
import os

UPLOAD_DIR = "uploads"


def save_uploaded_file(file: UploadFile) -> str | None:
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path
    except Exception as e:
        print(f"Error saving file: {e}")
        return None
