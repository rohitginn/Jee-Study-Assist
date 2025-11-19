import os
import pickle
import numpy as np
import faiss
import fitz  # PyMuPDF
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv
import boto3
import google.generativeai as genai

# ----------------- Load Env & Configure -----------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ----------------- S3 CONFIG -----------------
S3_BUCKET = os.getenv("AWS_BUCKET_NAME")
PDF_KEYS = ["Chemistry_updated.pdf", "Physics_updated.pdf"]
LOCAL_PDF_FOLDER = "./pdfs"

# S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

# ----------------- LOCAL STORAGE -----------------
DATA_FOLDER = "./data"
INDEX_FILE = os.path.join(DATA_FOLDER, "faiss_index.index")
MAPPING_FILE = os.path.join(DATA_FOLDER, "text_mapping.pkl")

os.makedirs(DATA_FOLDER, exist_ok=True)


# ----------------- DOWNLOAD PDFs FROM S3 -----------------
def download_pdfs_from_s3():
    os.makedirs(LOCAL_PDF_FOLDER, exist_ok=True)

    for key in PDF_KEYS:
        local_path = os.path.join(LOCAL_PDF_FOLDER, key)

        if not os.path.exists(local_path):
            print(f"⬇️ Downloading {key} from S3...")
            s3.download_file(S3_BUCKET, key, local_path)
        else:
            print(f"✔ {key} already downloaded.")


# ----------------- PDF TEXT EXTRACTION -----------------
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text")
        return text
    except Exception as e:
        print(f"⚠️ Error extracting text from {pdf_path}: {e}")
        return ""


# ----------------- GEMINI EMBEDDINGS -----------------
def generate_embedding(text_chunk):
    """Generate embedding using Gemini embeddings API."""
    try:
        response = genai.embed_content(
            model="models/text-embedding-004",
            content=text_chunk
        )
        return np.array(response["embedding"], dtype="float32")
    except Exception as e:
        print(f"⚠️ Embedding Error: {e}")
        return None


# ----------------- PROCESS PDFS (BUILD INDEX) -----------------
def process_pdfs():
    print("📥 Checking & downloading PDFs from S3...")
    download_pdfs_from_s3()

    print("⚙️ Building FAISS index...")
    text_chunks = []

    # Extract and chunk text
    for pdf_file in PDF_KEYS:
        pdf_path = os.path.join(LOCAL_PDF_FOLDER, pdf_file)
        print(f"📄 Processing {pdf_file} ...")

        text = extract_text_from_pdf(pdf_path)
        cleaned = text.replace("Reprint 2024-25", "").replace("\n", " ")

        chunks = [cleaned[i:i + 300] for i in range(0, len(cleaned), 300)]
        text_chunks.extend(chunks)

    # Batch embeddings
    embeddings_list = []
    batch_size = 50

    for i in tqdm(range(0, len(text_chunks), batch_size), desc="Embedding batches"):
        batch = text_chunks[i:i + batch_size]

        try:
            response = genai.embed_content(
                model="models/text-embedding-004",
                content=batch
            )
            batch_embeddings = [
                np.array(e, dtype="float32") for e in response["embedding"]
            ]
            embeddings_list.extend(batch_embeddings)

        except Exception as e:
            print(f"⚠️ Batch Error: {e}")

    if not embeddings_list:
        print("❌ No embeddings generated.")
        return

    np_embeddings = np.array(embeddings_list, dtype="float32")
    dim = np_embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(np_embeddings)

    faiss.write_index(index, INDEX_FILE)
    with open(MAPPING_FILE, "wb") as f:
        pickle.dump(text_chunks, f)

    print("✅ FAISS Index + Mapping Saved.")


# ----------------- RETRIEVE ANSWER -----------------
def retrieve_answer(query, k=3, max_chars=1000):
    try:
        index = faiss.read_index(INDEX_FILE)
        text_mapping = pickle.load(open(MAPPING_FILE, "rb"))
    except Exception:
        return ""

    query_vec = generate_embedding(query)
    if query_vec is None:
        return ""

    distances, indices = index.search(np.array([query_vec]), k)

    chunks = [text_mapping[i] for i in indices[0] if i < len(text_mapping)]
    return (" ".join(chunks))[:max_chars]


# ----------------- GEMINI LLM REFINE -----------------
def rephrase_with_gemini(text, query, mode="brief"):

    if mode == "brief":
        prompt = f"""
Summarize the following answer in 5–6 lines. Include formulas where needed.

Extracted Answer:
{text}

User Question: {query}
"""
    else:
        prompt = f"""
Explain the following answer clearly in 15–17 lines with formulas.

Extracted Answer:
{text}

User Question: {query}
"""

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print("LLM ERROR:", e)
        return "⚠️ Error generating LLM response."
