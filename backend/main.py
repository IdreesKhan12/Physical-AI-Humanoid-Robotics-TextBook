from dotenv import load_dotenv
load_dotenv() # Load environment variables at the very beginning

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List, Optional, Dict
import datetime
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Placeholder for Qdrant client, Cohere client, Gemini client
# These will be properly initialized in later tasks
qdrant_client = None
cohere_client = None
gemini_client = None

# Initialize RAG Agent globally (can be done during lifespan in future if needed)
from backend.rag_agent import ChatMessage, ChatRequest, chat
# Pydantic models for request and response
class QueryInput(BaseModel):
    question: str
    selected_text: Optional[str] = None

class Citation(BaseModel):
    url: str
    heading: Optional[str] = None
    chunk_text_snippet: str

class AgentMetadata(BaseModel):
    retrieval_score: float
    model_used: str
    response_time_ms: int

class AgentResponse(BaseModel):
    answer: str
    citations: List[Citation]
    metadata: AgentMetadata

class RetrievedChunkPayload(BaseModel):
    url: str
    heading: Optional[str] = None
    chunk_text: str
    chunk_index: int
    score: float

class RetrievalDebugResponse(BaseModel):
    query_embedding: List[float]
    retrieved_chunks: List[RetrievedChunkPayload]

class HealthStatus(BaseModel):
    status: str
    qdrant_status: str
    cohere_status: str
    gemini_status: str
    timestamp: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for managing the lifespan of the FastAPI application.
    Initializes clients on startup and closes them on shutdown.
    """
    global qdrant_client, cohere_client, gemini_client

    # TODO: Initialize Qdrant client
    # qdrant_client = QdrantClient(...)

    # TODO: Initialize Cohere client
    # cohere_client = cohere.Client(...)

    # TODO: Initialize Gemini client
    # gemini_client = genai.GenerativeModel(...)

    logger.info("FastAPI app startup complete.")
    yield
    logger.info("FastAPI app shutdown complete.")

app = FastAPI(lifespan=lifespan)
# Add CORS middleware
origins = [
    "http://localhost:3000",    # Docusaurus frontend default port
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "file://",
    "https://idreeskhan12.github.io/Physical-AI-Humanoid-Robotics-TextBook/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthStatus, status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint to verify the API is running and dependencies are accessible.
    """
    logger.info("Received /health request.")
    qdrant_status = await check_qdrant_status()
    cohere_status = await check_cohere_status()
    gemini_status = await check_gemini_status()
    
    overall_status = "ok"
    if "disconnected" in qdrant_status or \
       "disconnected" in cohere_status or \
       "disconnected" in gemini_status:
        overall_status = "error"
        logger.warning(f"Health check found errors: Qdrant={qdrant_status}, Cohere={cohere_status}, Gemini={gemini_status}")
    else:
        logger.info("Health check passed all dependency checks.")

    return HealthStatus(
        status=overall_status,
        qdrant_status=qdrant_status,
        cohere_status=cohere_status,
        gemini_status=gemini_status,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

from backend.retrieval import retrieve_data, build_context


@app.post("/ask")
async def ask_question(query: QueryInput):
    logger.info(f"Received /ask request for question: {query.question}")

    # 1️⃣ Retrieve relevant chunks (DETERMINISTIC)
    retrieved_chunks = retrieve_data(query.question)

    # 2️⃣ Out-of-book handling
    if not retrieved_chunks:
        return {
            "answer": "This question is not covered in the course material.",
            "citations": [],
            "metadata": {
                "retrieval_score": 0.0,
                "model_used": "none",
                "response_time_ms": 0
            }
        }

    # 3️⃣ Build context
    context = build_context(retrieved_chunks)

    # 4️⃣ Create strict RAG prompt
    rag_prompt = f"""
You are a course assistant.

Answer the question using ONLY the information below.
If the answer is not present, say clearly:
"This topic is not covered in the course material."

COURSE MATERIAL:
{context}

QUESTION:
{query.question}
"""

    # 5️⃣ Send to agent
    request = ChatRequest(
        messages=[ChatMessage(role="user", text=rag_prompt)]
    )

    response = await chat(request)

    return {
        "answer": response["answer"],
        "citations": [],
        "metadata": {
            "retrieval_score": retrieved_chunks[0].get("score", 0.0),
            "model_used": "openrouter",
            "response_time_ms": 0
        }
    }

@app.post("/debug/retrieval", response_model=RetrievalDebugResponse, status_code=status.HTTP_200_OK)
async def debug_retrieval(query: QueryInput):
    """
    Endpoint to debug retrieval by returning the raw retrieved chunks.
    """
    logger.info(f"Received /debug/retrieval request for question: {query.question}")
    try:
        query_embedding = get_query_embedding(query.question)
        retrieved_chunks = search_qdrant(query_embedding, QDRANT_COLLECTION_NAME, k=10) # Retrieve top 10
        logger.info(f"Retrieved {len(retrieved_chunks)} chunks for '{query.question}'.")
        return RetrievalDebugResponse(
            query_embedding=query_embedding,
            retrieved_chunks=retrieved_chunks
        )
    except Exception as e:
        logger.exception(f"An unexpected error occurred in /debug/retrieval for question: {query.question}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during retrieval debugging: {e}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

