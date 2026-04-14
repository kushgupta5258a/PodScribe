import streamlit as st
import requests

from services.audio import save_uploaded_file
from services.deepgram_service import transcribe_audio
from services.llm import translate_text, generate_summary, chat_with_transcript
from services.embeddings import create_vector_store


# =========================
# BACKEND CONFIG
# =========================
BACKEND_URL = "https://podscribe-saiv.onrender.com"


def download_from_backend(url):
    response = requests.post(
        f"{BACKEND_URL}/download",
        params={"url": url},
        timeout=120
    )

    if response.status_code != 200:
        raise Exception("Download failed")

    # SAVE FILE LOCALLY
    file_path = "temp_audio.mp3"
    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="PodScribe AI", layout="wide")
st.title("🎙️ PodScribe AI")


# =========================
# SESSION INIT
# =========================
if "transcript" not in st.session_state:
    st.session_state["transcript"] = None


# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["Transcribe", "Summary", "Chat"])


# =====================================================
# TRANSCRIBE TAB
# =====================================================
with tab1:

    st.subheader("Upload or Paste Podcast")

    url = st.text_input("Paste YouTube link")
    uploaded_file = st.file_uploader("Or upload audio file")

    input_language = st.selectbox(
        "Select input language",
        ["auto", "en", "hi"]
    )

    output_language = st.selectbox(
        "Select output language",
        ["Original", "English", "Hindi"]
    )

    if st.button("Transcribe"):

        file_path = None

        # -----------------------
        # HANDLE INPUT
        # -----------------------
        if uploaded_file:
            try:
                file_path = save_uploaded_file(uploaded_file)
            except Exception as e:
                st.error(f"File upload failed: {e}")
                st.stop()

        elif url:
            try:
                with st.spinner("Downloading from YouTube via backend..."):
                    file_path = download_from_backend(url)
            except Exception as e:
                st.error(f"YouTube backend failed:\n{e}")
                st.stop()

        else:
            st.warning("Please provide a URL or upload a file.")
            st.stop()

        # -----------------------
        # TRANSCRIPTION
        # -----------------------
        with st.spinner("Transcribing with Deepgram..."):
            transcript = transcribe_audio(
                file_path,
                language=input_language
            )

        if not transcript or "error" in transcript.lower():
            st.error(transcript)
            st.stop()

        # -----------------------
        # TRANSLATION
        # -----------------------
        if output_language != "Original":
            with st.spinner(f"Translating to {output_language}..."):
                translated = translate_text(transcript, output_language)

            if not translated or "error" in translated.lower():
                st.error(translated)
                st.stop()

            transcript = translated

        # -----------------------
        # SAVE + BUILD RAG
        # -----------------------
        st.session_state["transcript"] = transcript

        with st.spinner("Building semantic index..."):
            create_vector_store(transcript)

        st.subheader("Transcript")
        st.write(transcript)


# =====================================================
# SUMMARY TAB
# =====================================================
with tab2:

    st.subheader("Generate Summary")

    transcript = st.session_state.get("transcript")

    if not transcript:
        st.warning("Please transcribe a podcast first.")
    else:

        style = st.selectbox(
            "Select Summary Style",
            [
                "Bullet Points",
                "Executive Summary",
                "Key Takeaways",
                "Twitter Thread",
                "LinkedIn Post"
            ]
        )

        word_limit = st.number_input(
            "Word Limit",
            min_value=50,
            max_value=1000,
            value=200,
            step=50
        )

        if st.button("Generate Summary"):

            with st.spinner("Generating summary..."):
                summary = generate_summary(transcript, style, word_limit)

            if not summary or "error" in summary.lower():
                st.error(summary)
            else:
                st.markdown("### 📄 Summary")
                st.write(summary)


# =====================================================
# CHAT TAB (RAG Enabled)
# =====================================================
with tab3:

    st.subheader("Chat with Podcast")

    transcript = st.session_state.get("transcript")

    if not transcript:
        st.warning("Please transcribe a podcast first.")
    else:

        question = st.text_input("Ask something about the podcast")

        if st.button("Get Answer"):

            if not question:
                st.warning("Please enter a question.")
                st.stop()

            with st.spinner("Searching relevant context..."):
                answer = chat_with_transcript(transcript, question)

            if not answer or "error" in answer.lower():
                st.error(answer)
            else:
                st.markdown("### 🤖 AI Answer:")
                st.write(answer)
