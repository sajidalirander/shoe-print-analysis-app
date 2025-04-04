# backend/api/endpoints.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os

from backend.api.logic import list_probe_files, match_probe_to_references

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "backend", "database", "raw_normalized")

router = APIRouter(prefix="/api")

@router.get("/shoeprints")
def get_probe_files():
    return {"files": list_probe_files()}

@router.get("/match/{filename}")
def get_matches(filename: str):
    matches = match_probe_to_references(filename)
    if not matches:
        return JSONResponse(content={"message": f"{filename} not found or invalid."}, status_code=404)
    return {"top_matches": matches}

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        filename = os.path.basename(file.filename)
        save_path = os.path.join(RAW_DIR, filename)
        with open(save_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return {"message": f"{filename} uploaded successfully."}
    except Exception as e:
        return JSONResponse(content={"message": f"Upload failed: {str(e)}"}, status_code=500)
