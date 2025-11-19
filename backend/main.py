from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag_system import retrieve_answer, rephrase_with_gemini, PDF_FOLDER, watch_and_update_index
import threading

app = FastAPI(title="JEE Study Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jee-study-assist.vercel.app"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str
    mode: str = "brief"  # brief, full, detailed

@app.on_event("startup")
async def start_pdf_watcher():
    """Start background thread for PDF monitoring and FAISS rebuild."""
    thread = threading.Thread(target=watch_and_update_index, args=(PDF_FOLDER,), daemon=True)
    thread.start()

@app.post("/ask")
async def ask_question(req: AskRequest):
    question = req.question.strip()
    mode = req.mode.lower()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    if mode not in ["brief", "full", "detailed"]:
        raise HTTPException(status_code=400, detail="Invalid mode.")

    raw_answer = retrieve_answer(question)
    if not raw_answer:
        return {"message": "❌ No relevant content found."}

    llm_answer = rephrase_with_gemini(raw_answer, question, mode)

    return {
        "raw_answer": raw_answer,
        "llm_answer": llm_answer,
        "mode_used": mode
    }

@app.get("/")
def root():
    return {"message": "🚀 JEE Study Assistant is running. Use POST /ask"}