from fastapi import FastAPI
from downloader import download_audio

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.post("/download")
def download(url: str):
    file_path = download_audio(url)
    return {"file_path": file_path}