import streamlit as st
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Cache model for deployment
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

vector_store = None
stored_chunks = []


def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def create_vector_store(transcript):
    global vector_store, stored_chunks

    stored_chunks = chunk_text(transcript)
    embeddings = model.encode(stored_chunks)

    dimension = embeddings.shape[1]

    vector_store = faiss.IndexFlatL2(dimension)
    vector_store.add(np.array(embeddings))


def retrieve_relevant_chunks(query, top_k=3):
    global vector_store, stored_chunks

    if vector_store is None:
        return []

    query_embedding = model.encode([query])
    distances, indices = vector_store.search(
        np.array(query_embedding),
        top_k
    )

    results = []
    for idx in indices[0]:
        results.append(stored_chunks[idx])

    return results
