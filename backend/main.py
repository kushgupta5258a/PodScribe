import os

from fastapi import FastAPI
from fastapi.responses import FileResponse

from downloader import download_audio

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.post("/download")
def download(url: str):
    file_path = download_audio(url)
    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        filename=os.path.basename(file_path)
    )