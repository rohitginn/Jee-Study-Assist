from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_system import retrieve_answer
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Force UTF-8 encoding for subprocess
os.environ["PYTHONIOENCODING"] = "utf-8"

# Load the SentenceTransformer model once
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Input model
class AskRequest(BaseModel):
    question: str
    mode: str = "brief"  # "brief", "full" or "detailed"

@app.post("/ask")
async def ask_question(request: AskRequest):
    query = request.question.strip()
    mode = request.mode.lower()

    if not query:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    if mode not in ["brief", "full", "detailed"]:
        raise HTTPException(status_code=400, detail="Invalid mode. Use 'brief' or 'full'.")

    try:
        # Step 1: Get content from PDF
        raw_answer = retrieve_answer(query, embedder)

        if not raw_answer:
            return {"message": "❌ No relevant content found."}

        # Step 2: Prompt based on mode
        content = raw_answer[:2000]  # limit to avoid overflow
        if mode == "brief":
            prompt = f"""Y You are a helpful assistant for JEE students. Based on the following extracted content from a textbook, generate an answer with the following instructions:
            - First priority give to text from textbook if not enough use your brain.
            - Fix grammar or clarity issues.Also give the formula if present in textbook or raw answer if not present use your mind.
            - Summarize in 5–6 lines in simple language.:
            
        Content:
        {content}

        Question: {query}

        Answer:"""
        else:  # full or detailed
            prompt = f"""You are a helpful assistant for JEE students. Based on the following extracted content from a textbook, generate an answer with the following instructions:

            - First priority give to text from textbook if not enough use your brain.
            - Fix grammar or clarity issues.Also give the formula if present in textbook or raw answer if not present use your mind.
            - Provide a detailed explanation in 15–17 lines, well-structured and easy to understand. .
            If content is insufficient, respond with: 'The answer is not available in the provided material.'

        Content:
        {content}

        Question: {query}

        Answer:"""

        # Step 3: Run LLM
        response = subprocess.run(
            ["ollama", "run", "mistral:7b-instruct"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if response.returncode != 0:
            error_msg = response.stderr.decode("utf-8", errors="replace")
            print("Ollama error:", error_msg)
            return {
                "raw_answer": content,
                "llm_answer": "⚠️ Could not enhance the answer. Try again later."
            }

        llm_output = response.stdout.decode("utf-8")

        return {
            "raw_answer": content.strip(),
            "llm_answer": llm_output.strip(),
            "mode_used": mode
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "🚀 JEE Study Assistant running! Use POST /ask with 'question' and optional 'mode' (brief/full)."}



# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from rag_system import retrieve_answer
# from sentence_transformers import SentenceTransformer
# from fastapi.middleware.cors import CORSMiddleware
# import subprocess
# import os

# app = FastAPI()

# # --- CORS Settings ---
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173", "http://127.0.0.1:8000"],  # Allow frontend + Swagger docs
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- UTF-8 globally ---
# os.environ["PYTHONIOENCODING"] = "utf-8"

# # --- Load Embedder once ---
# embedder = SentenceTransformer("all-MiniLM-L6-v2")

# # --- Request Model ---
# class AskRequest(BaseModel):
#     question: str
#     mode: str = "brief"  # Default is brief or full

# @app.post("/ask")
# async def ask_question(request: AskRequest):
#     query = request.question.strip()
#     mode = request.mode.lower()

#     if not query:
#         raise HTTPException(status_code=400, detail="❌ Question cannot be empty.")
#     if mode not in ["brief", "full"]:
#         raise HTTPException(status_code=400, detail="❌ Mode must be 'brief' or 'full'.")

#     try:
#         # --- Step 1: Get raw content from PDF ---
#         raw_answer = retrieve_answer(query, embedder)
#         if not raw_answer.strip():
#             return {
#                 "raw_answer": "",
#                 "llm_answer": "❌ No relevant content found in the documents."
#             }

#         # --- Step 2: Prompt for LLM ---
#         prompt = (
#             f"Summarize and explain briefly in 4-6 lines for a student:\n\n{raw_answer}"
#             if mode == "brief" else
#             f"Explain in full detail for a student:\n\n{raw_answer}"
#         )

#         # --- Step 3: Call Mistral via Ollama ---
#         response = subprocess.run(
#             ["ollama", "run", "mistral:7b-instruct"],
#             input=prompt.encode("utf-8"),
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             timeout=45  # seconds
#         )

#         if response.returncode != 0:
#             error_msg = response.stderr.decode("utf-8", errors="replace")
#             print("❌ Ollama Error:", error_msg)
#             return {
#                 "raw_answer": raw_answer,
#                 "llm_answer": "⚠️ Mistral failed to respond. Try again later."
#             }

#         llm_output = response.stdout.decode("utf-8")

#         return {
#             "raw_answer": raw_answer.strip(),
#             "llm_answer": llm_output.strip(),
#             "mode_used": mode
#         }

#     except subprocess.TimeoutExpired:
#         raise HTTPException(status_code=504, detail="⏳ Ollama took too long. Try again.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"⚠️ Internal Error: {str(e)}")

# @app.get("/")
# def root():
#     return {
#         "message": "🚀 JEE Study Assistant is running!",
#         "info": "Use POST /ask with 'question' and optional 'mode' (brief/full)."
#     }





# # from fastapi import FastAPI, HTTPException
# # from pydantic import BaseModel
# # from rag_system import retrieve_answer
# # from sentence_transformers import SentenceTransformer
# # from fastapi.middleware.cors import CORSMiddleware
# # import subprocess
# # import os

# # app = FastAPI()

# # # CORS Settings
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["http://localhost:5173"],  # your Vite React frontend
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # UTF-8 globally
# # os.environ["PYTHONIOENCODING"] = "utf-8"

# # # Load embedder
# # embedder = SentenceTransformer("all-MiniLM-L6-v2")

# # # Request model
# # class AskRequest(BaseModel):
# #     question: str
# #     mode: str = "brief"  # Default is brief, or full

# # @app.post("/ask")
# # async def ask_question(request: AskRequest):
# #     query = request.question.strip()
# #     mode = request.mode.lower()

# #     if not query:
# #         raise HTTPException(status_code=400, detail="Question cannot be empty.")

# #     if mode not in ["brief", "full"]:
# #         raise HTTPException(status_code=400, detail="Invalid mode. Use 'brief' or 'full'.")

# #     try:
# #         # Step 1: Retrieve content
# #         raw_answer = retrieve_answer(query, embedder)
# #         if not raw_answer:
# #             return {"message": "❌ No relevant content found."}

# #         # Step 2: Create prompt
# #         if mode == "brief":
# #             prompt = (
# #                 f"Summarize and explain briefly (simple 5-7 lines) for a student:\n\n{raw_answer}"
# #             )
# #         else:
# #             prompt = (
# #                 f"Explain fully and clearly for a student:\n\n{raw_answer}"
# #             )

# #         # Step 3: Call Mistral
# #         response = subprocess.run(
# #             ["ollama", "run", "mistral:7b-instruct"],
# #             input=prompt.encode("utf-8"),
# #             stdout=subprocess.PIPE,
# #             stderr=subprocess.PIPE
# #         )

# #         if response.returncode != 0:
# #             error_msg = response.stderr.decode("utf-8", errors="replace")
# #             print("Error running Ollama:", error_msg)
# #             return {
# #                 "raw_answer": raw_answer,
# #                 "llm_answer": "⚠️ Error enhancing answer with LLM."
# #             }

# #         llm_output = response.stdout.decode("utf-8")

# #         return {
# #             "raw_answer": raw_answer.strip(),
# #             "llm_answer": llm_output.strip(),
# #             "mode_used": mode
# #         }

# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# # @app.get("/")
# # def root():
# #     return {"message": "🚀 JEE Study Assistant running! Use POST /ask with 'question' and optional 'mode' (brief/full)."}
