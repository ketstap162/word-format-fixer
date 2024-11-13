import shutil
from fastapi import UploadFile
import os
from settrings import UPLOAD_DIR


def ensure_directory_exists(directory_path: str):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def ensure_file_path(file_path: str) -> str:
    if os.path.exists(file_path):
        directory, filename = os.path.split(file_path)
        base_name, ext = os.path.splitext(filename)

        counter = 1

        while os.path.exists(file_path):
            new_filename = f"{base_name}-{counter}{ext}"
            file_path = os.path.join(directory, new_filename)
            counter += 1

        return file_path
    return file_path


def save_uploaded_file(file: UploadFile, username: str = "none") -> str | None:
    try:
        user_dir = os.path.join(UPLOAD_DIR, username)

        ensure_directory_exists(user_dir)

        file_path = ensure_file_path(os.path.join(user_dir, file.filename))

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path
    except Exception as e:
        print(f"Error saving file: {e}")
        return None
