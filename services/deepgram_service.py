import requests
from config import DEEPGRAM_API_KEY


def transcribe_audio(file_path: str, language=None):

    try:
        url = "https://api.deepgram.com/v1/listen"

        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
        }

        params = {
            "model": "nova-2",
            "smart_format": "true",
            "punctuate": "true",
            "diarize": "true",        # 🔥 speaker detection
            "utterances": "true"      # 🔥 sentence segmentation
        }

        if language and language != "auto":
            params["language"] = language

        with open(file_path, "rb") as audio:
            response = requests.post(
                url,
                headers=headers,
                params=params,
                data=audio
            )

        response.raise_for_status()
        result = response.json()

        # 🔥 Build speaker-formatted transcript
        utterances = result["results"]["utterances"]

        formatted_transcript = ""

        for utt in utterances:
            speaker = utt["speaker"]
            text = utt["transcript"]
            formatted_transcript += f"Speaker {speaker}: {text}\n\n"

        return formatted_transcript

    except Exception as e:
        return f"Transcription error: {str(e)}"

def text_to_speech(text, output_path="data/agent_voice.wav"):

    url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"

    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": text
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return None

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path
