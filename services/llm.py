import requests
from services.embeddings import retrieve_relevant_chunks
from config import OPENROUTER_API_KEY


# ====================================================
# CORE LLM CALL
# ====================================================
def call_llm(messages):

    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY not configured."

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://podscribe.streamlit.app",  # optional but recommended
        "X-Title": "PodScribe AI"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0.3
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        else:
            return f"Unexpected response format:\n{data}"

    except requests.exceptions.RequestException as e:
        return f"LLM Request Error: {str(e)}"


# ====================================================
# RAG CHAT
# ====================================================
def chat_with_transcript(transcript, question):

    relevant_chunks = retrieve_relevant_chunks(question)

    if not relevant_chunks:
        return "No relevant context found."

    context = "\n\n".join(relevant_chunks)

    messages = [
        {
            "role": "system",
            "content": "You are a podcast assistant. Answer ONLY from the provided context. If the answer is not in context, say you don't know."
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion:\n{question}"
        }
    ]

    return call_llm(messages)


# ====================================================
# SUMMARY
# ====================================================
def generate_summary(transcript, style, word_limit):

    messages = [
        {
            "role": "system",
            "content": "You are an expert podcast summarizer."
        },
        {
            "role": "user",
            "content": f"""
Summarize the following podcast transcript.

Style: {style}
Maximum words: {word_limit}

Transcript:
{transcript}
"""
        }
    ]

    return call_llm(messages)


# ====================================================
# TRANSLATION
# ====================================================
def translate_text(text, target_language):

    messages = [
        {
            "role": "system",
            "content": "You are a professional translator. Only return translated text."
        },
        {
            "role": "user",
            "content": f"Translate this to {target_language}:\n\n{text}"
        }
    ]

    return call_llm(messages)
