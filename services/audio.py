import os
import subprocess
import sys

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


def save_uploaded_file(uploaded_file):
    """
    Saves uploaded file to data directory.
    """
    file_path = os.path.join(DATA_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def download_youtube_audio(url):
    """
    Downloads best audio from YouTube using yt-dlp.
    Returns path to downloaded file.
    """

    output_path = os.path.join(DATA_DIR, "%(title)s.%(ext)s")

    # ✅ Use current Python executable (fixes Streamlit + Windows issue)
    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        "-f",
        "bestaudio",
        "--no-playlist",
        "-o",
        output_path,
        url
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(f"yt-dlp error:\n{result.stderr}")

    # Get latest downloaded file
    files = [
        os.path.join(DATA_DIR, f)
        for f in os.listdir(DATA_DIR)
        if not f.endswith(".wav")  # ignore any wav files
    ]

    if not files:
        raise Exception("No file downloaded by yt-dlp.")

    latest_file = max(files, key=os.path.getctime)

    return latest_file
