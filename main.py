# filename: main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
import io
import json

app = FastAPI()

# Allow CORS for FlutterFlow
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)`

@app.post("/upload-theme/")
async def upload_theme_file(file: UploadFile = File(...)):
    filename = file.filename
    contents = await file.read()

    if filename.endswith(".csv"):
        decoded = contents.decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded))
        data = next(reader)  # use first row
    elif filename.endswith(".json"):
        decoded = contents.decode("utf-8")
        data = json.loads(decoded)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    # Ensure all required fields are present
    expected_fields = [
        "backgroundColor",
        "secondaryBackgroundColor",
        "navbarColor",
        "appLogoURL",
        "appbarColor",
        "fontPrimaryColor",
        "fontSecondaryColor"
    ]

    missing = [field for field in expected_fields if field not in data]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing fields: {missing}")

    return data
