import yt_dlp
import os

OUTPUT_PATH = "audio"

def download_audio(url: str):
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{OUTPUT_PATH}/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # ORIGINAL FILE NAME
        original_file = ydl.prepare_filename(info)

        # FINAL MP3 FILE (IMPORTANT FIX)
        base, _ = os.path.splitext(original_file)
        final_file = base + ".mp3"

    return final_file