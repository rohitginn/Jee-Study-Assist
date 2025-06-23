import os
import sys
import io
import pickle
import numpy as np
import faiss
import subprocess
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer

# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Constants
INDEX_FILE = "faiss_index.index"
MAPPING_FILE = "text_mapping.pkl"
PDF_FOLDER = "./pdfs"

def extract_text_from_pdf(pdf_path):
    """Extracts visible text from all pages of a PDF using PyMuPDF."""
    extracted_text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            extracted_text += page.get_text("text")
    return extracted_text

def process_pdfs(pdf_folder, embedder):
    """Reads PDFs, splits into chunks, encodes, and builds FAISS index."""
    text_chunks = []
    embeddings_list = []

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            print(f"\n📄 Processing: {pdf_file}", flush=True)
            text = extract_text_from_pdf(pdf_path)
            text = text.replace("Reprint 2024-25", "")  # Cleaning noise
            print(f"📝 Extracted text preview:\n{text[:500]}...\n", flush=True)

            # Smaller chunk size for better retrieval
            chunks = [text[i:i+300] for i in range(0, len(text), 300)]
            print(f"🔢 Total chunks: {len(chunks)}\n", flush=True)

            text_chunks.extend(chunks)
            embeddings = embedder.encode(chunks)
            embeddings_list.extend(embeddings)

    if not embeddings_list:
        print("❌ No embeddings found.", flush=True)
        return

    np_embeddings = np.array(embeddings_list).astype('float32')
    embedding_dim = np_embeddings.shape[1]

    index = faiss.IndexFlatL2(embedding_dim)
    index.add(np_embeddings)

    faiss.write_index(index, INDEX_FILE)
    with open(MAPPING_FILE, "wb") as f:
        pickle.dump(text_chunks, f)

    print("✅ FAISS index and text mapping saved.", flush=True)

def retrieve_answer(query, embedder, k=3):
    """Retrieve top-k chunks relevant to query."""
    try:
        index = faiss.read_index(INDEX_FILE)
        with open(MAPPING_FILE, "rb") as f:
            text_mapping = pickle.load(f)
    except Exception as e:
        print("❌ Error loading index or mapping:", e, flush=True)
        return ""

    query_embedding = embedder.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, k)

    retrieved_chunks = [text_mapping[i] for i in indices[0] if i < len(text_mapping)]
    retrieved_text = " ".join(retrieved_chunks)

    return retrieved_text

def rephrase_with_mistral(text, query, mode="brief"):
    """Use Mistral LLM via Ollama CLI to rephrase answer with dynamic mode (brief/full)."""
    if mode == "brief":
        prompt = f"""Summarize briefly for a JEE student in 5-7 lines:

Content:
{text}
"""
    else:  # full or detailed
        prompt = f"""Explain in complete detailed form, well-structured and student-friendly :

Content:
{text}
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral:7b-instruct"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return result.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Mistral Error: {e.stderr}")
        return "⚠️ Error generating response."

if __name__ == "__main__":
    print("\n🚀 Script started...", flush=True)

    print("🧠 Loading SentenceTransformer...", flush=True)
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Embedder loaded.", flush=True)

    if not os.path.exists(INDEX_FILE) or not os.path.exists(MAPPING_FILE):
        print("⚙️ Processing PDFs for the first time...", flush=True)
        process_pdfs(PDF_FOLDER, embedder)
    else:
        print("✅ Using existing FAISS index and mapping.", flush=True)

    while True:
        query = input("\n🔍 Enter your question (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break

        raw_answer = retrieve_answer(query, embedder)
        print("\n📄 Retrieved content preview:\n", raw_answer[:300], flush=True)

        if input("\n👀 View more? (y/n): ").lower() == "y":
            print("\n📄 Full retrieved content:\n", raw_answer, flush=True)

        mode = input("\n⚡ Choose mode (brief/full): ").lower()
        print("\n⏳ Rephrasing via Mistral...", flush=True)
        final_answer = rephrase_with_mistral(raw_answer, query, mode)
        print(f"\n✅ Final Answer:\n{final_answer}", flush=True)


# import os
# import sys
# import io
# import pickle
# import time
# import numpy as np
# import faiss
# import subprocess
# import fitz  # PyMuPDF
# from sentence_transformers import SentenceTransformer

# # Ensure UTF-8 output
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# # Constants
# INDEX_FILE = "faiss_index.index"
# MAPPING_FILE = "text_mapping.pkl"
# PDF_FOLDER = "./pdfs"

# def extract_text_from_pdf(pdf_path):
#     """
#     Extracts visible text from all pages of a PDF using PyMuPDF.
#     """
#     extracted_text = ""
#     with fitz.open(pdf_path) as doc:
#         for page in doc:
#             extracted_text += page.get_text("text")
#     return extracted_text

# def process_pdfs(pdf_folder, embedder):
#     """
#     Reads PDFs, splits into chunks, encodes, and builds FAISS index.
#     """
#     text_chunks = []
#     embeddings_list = []

#     for pdf_file in os.listdir(pdf_folder):
#         if pdf_file.lower().endswith(".pdf"):
#             pdf_path = os.path.join(pdf_folder, pdf_file)
#             print(f"\n📄 Processing: {pdf_file}", flush=True)
#             text = extract_text_from_pdf(pdf_path)
#             text = text.replace("Reprint 2024-25", "")  # Cleaning noise
#             print(f"📝 Extracted text preview:\n{text[:500]}...\n", flush=True)

#             # Smaller chunk size for faster retrieval
#             chunks = [text[i:i+300] for i in range(0, len(text), 300)]
#             print(f"🔢 Total chunks: {len(chunks)}\n", flush=True)

#             text_chunks.extend(chunks)
#             embeddings = embedder.encode(chunks)
#             embeddings_list.extend(embeddings)

#     if not embeddings_list:
#         print("❌ No embeddings found.", flush=True)
#         return

#     np_embeddings = np.array(embeddings_list).astype('float32')
#     embedding_dim = np_embeddings.shape[1]

#     index = faiss.IndexFlatL2(embedding_dim)
#     index.add(np_embeddings)

#     faiss.write_index(index, INDEX_FILE)
#     with open(MAPPING_FILE, "wb") as f:
#         pickle.dump(text_chunks, f)

#     print("✅ FAISS index and text mapping saved.", flush=True)

# def retrieve_answer(query, embedder, k=3):
#     """
#     Retrieve top-k chunks relevant to query.
#     """
#     try:
#         index = faiss.read_index(INDEX_FILE)
#         with open(MAPPING_FILE, "rb") as f:
#             text_mapping = pickle.load(f)
#     except Exception as e:
#         print("❌ Error loading index or mapping:", e, flush=True)
#         return ""

#     query_embedding = embedder.encode([query]).astype('float32')
#     distances, indices = index.search(query_embedding, k)

#     retrieved_chunks = [text_mapping[i] for i in indices[0] if i < len(text_mapping)]
#     retrieved_text = " ".join(retrieved_chunks)

#     # Limit the size of retrieved text for faster LLM prompting
#     if len(retrieved_text) > 1000:
#         retrieved_text = retrieved_text[:1000] + "..."

#     return retrieved_text

# def rephrase_with_mistral(text, query):
#     """
#     Use Mistral LLM via Ollama CLI to rephrase answer.
#     """
#     prompt = f"""Generate an answer based on the following content. Adapt the length based on the user's request.
# If user asks for short, make it short. If they ask for detailed, make it detailed.
# Keep the tone friendly and remove any markdown formatting.

# User's question: {query}

# Content: {text}
# """

#     try:
#         result = subprocess.run(
#             ["ollama", "run", "mistral:7b-instruct"],
#             input=prompt.encode("utf-8"),
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             check=True
#         )
#         return result.stdout.decode("utf-8").strip()
#     except subprocess.CalledProcessError as e:
#         print(f"⚠️ Mistral Error: {e.stderr}")
#         return "⚠️ Error in generating response."

# if __name__ == "__main__":
#     print("\n🚀 Script started...", flush=True)

#     print("🧠 Loading SentenceTransformer...", flush=True)
#     embedder = SentenceTransformer("all-MiniLM-L6-v2")
#     print("✅ Embedder loaded.", flush=True)

#     if not os.path.exists(INDEX_FILE) or not os.path.exists(MAPPING_FILE):
#         print("⚙️ Processing PDFs for the first time...", flush=True)
#         process_pdfs(PDF_FOLDER, embedder)
#     else:
#         print("✅ Using existing FAISS index and mapping.", flush=True)

#     while True:
#         query = input("\n🔍 Enter your question (or type 'exit' to quit): ")
#         if query.lower() == 'exit':
#             break

#         raw_answer = retrieve_answer(query, embedder)
#         print("\n📄 Retrieved content preview:\n", raw_answer[:300], flush=True)

#         if input("\n👀 View more? (y/n): ").lower() == "y":
#             print("\n📄 Full retrieved content:\n", raw_answer, flush=True)

#         print("\n⏳ Rephrasing via Mistral...", flush=True)
#         final_answer = rephrase_with_mistral(raw_answer, query)
#         print(f"\n✅ Final Answer:\n{final_answer}", flush=True)
