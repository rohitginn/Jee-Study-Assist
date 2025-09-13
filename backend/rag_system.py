import os
import pickle
import numpy as np
import faiss
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv
import subprocess
import time
from pathlib import Path

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

PDF_FOLDER = "./pdfs"
INDEX_FILE = "faiss_index.index"
MAPPING_FILE = "text_mapping.pkl"

embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- PDF & FAISS ----------------

def extract_text_from_pdf(pdf_path):
    """Extract visible text from a PDF."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text")
    return text

def process_pdfs(pdf_folder, embedder):
    """Build FAISS index from PDFs."""
    print("⚙️ Building FAISS index from PDFs...")
    text_chunks = []
    embeddings_list = []

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            print(f"📄 Processing: {pdf_file}")
            text = extract_text_from_pdf(pdf_path)
            text = text.replace("Reprint 2024-25", "").replace("\n", " ")
            chunks = [text[i:i+300] for i in range(0, len(text), 300)]
            text_chunks.extend(chunks)
            embeddings = embedder.encode(chunks)
            embeddings_list.extend(embeddings)

    if not embeddings_list:
        print("❌ No embeddings found.")
        return

    np_embeddings = np.array(embeddings_list).astype('float32')
    embedding_dim = np_embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(np_embeddings)

    faiss.write_index(index, INDEX_FILE)
    with open(MAPPING_FILE, "wb") as f:
        pickle.dump(text_chunks, f)
    print("✅ FAISS index and mapping saved.")

def retrieve_answer(query, embedder, k=3, max_chars=1000):
    """Retrieve top-k chunks relevant to query and shorten them."""
    try:
        index = faiss.read_index(INDEX_FILE)
        with open(MAPPING_FILE, "rb") as f:
            text_mapping = pickle.load(f)
    except Exception as e:
        print("❌ Error loading index or mapping:", e)
        return ""

    query_embedding = embedder.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, k)
    retrieved_chunks = [text_mapping[i] for i in indices[0] if i < len(text_mapping)]
    retrieved_text = " ".join(retrieved_chunks)
    return retrieved_text[:max_chars]

# ---------------- Gemini LLM ----------------

def rephrase_with_gemini(text, query, mode="brief"):
    """Use Gemini LLM to refine answer."""
    if mode == "brief":
        prompt = f"""You are a helpful assistant for JEE students.
Summarize the following content in 5–6 lines with formulas if relevant:

Content:
{text}

Question: {query}

Answer:"""
    else:
        prompt = f"""You are a helpful assistant for JEE students.
Provide a detailed explanation in 15–17 lines including formulas:

Content:
{text}

Question: {query}

Answer:"""

    model = genai.GenerativeModel("models/gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("⚠️ Gemini LLM Error:", e)
        return "⚠️ Error generating response."

# ---------------- Background watcher ----------------

def watch_and_update_index(pdf_folder, embedder, interval=120):
    """Background task: watches PDF folder and rebuilds FAISS index."""
    seen_files = set(Path(pdf_folder).glob("*.pdf"))
    while True:
        time.sleep(interval)
        current_files = set(Path(pdf_folder).glob("*.pdf"))
        if current_files != seen_files:
            print("⚙️ New PDFs detected. Rebuilding FAISS index...")
            process_pdfs(pdf_folder, embedder)
            seen_files = current_files
