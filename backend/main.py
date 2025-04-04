from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.matcher import RAW_DIR, match_probe_to_references
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Shoeprint Matching API"}

# CORS (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/shoeprints")
def list_probe_images():
    try:
        files = sorted([f for f in os.listdir(RAW_DIR) if f.endswith((".jpg", ".png"))])
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/match/{filename}")
def match_image(filename: str):
    try:
        matches = match_probe_to_references(filename)
        return {"probe": filename, "top_matches": matches}
    except Exception as e:
        print(f"[ERROR] Matching failed for {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
