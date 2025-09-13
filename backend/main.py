from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_system import retrieve_answer
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware
import os
import google.generativeai as genai  # <-- NEW

# ---------- Config ----------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["PYTHONIOENCODING"] = "utf-8"
embedder = SentenceTransformer("all-MiniLM-L6-v2")


class AskRequest(BaseModel):
    question: str
    mode: str = "brief"  # "brief", "full", "detailed"


@app.post("/ask")
async def ask_question(request: AskRequest):
    query = request.question.strip()
    mode = request.mode.lower()

    if not query:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    if mode not in ["brief", "full", "detailed"]:
        raise HTTPException(status_code=400, detail="Invalid mode.")

    try:
        # 1️⃣ Retrieve context from PDFs
        raw_answer = retrieve_answer(query, embedder)
        if not raw_answer:
            return {"message": "❌ No relevant content found."}

        content = raw_answer[:2000]

        # 2️⃣ Build prompt
        if mode == "brief":
            prompt = f"""You are a helpful assistant for JEE students.
Use the text below if possible; if not, answer yourself.
Give a clear 5–6 line explanation and include formulas if relevant.

Content:
{content}

Question: {query}

Answer:"""
        else:
            prompt = f"""You are a helpful assistant for JEE students.
Use the text below if possible; if not, answer yourself.
Give a detailed explanation (15–17 lines), include formulas.

Content:
{content}

Question: {query}

Answer:"""

        # 3️⃣ Call Gemini Pro
        model = genai.GenerativeModel("gemini-pro")
        llm_response = model.generate_content(prompt)

        return {
            "raw_answer": content.strip(),
            "llm_answer": llm_response.text.strip(),
            "mode_used": mode,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {
        "message": "🚀 JEE Study Assistant running with Gemini Pro! POST /ask with 'question' & optional 'mode'."
    }
