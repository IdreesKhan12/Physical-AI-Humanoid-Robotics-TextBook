import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the existing RAG agent functionality
from rag_agent import RAGAgent

# Create FastAPI app
app = FastAPI(
    title="RAG Agent API",
    description="API for RAG Agent with document retrieval and question answering",
    version="1.0.0"
)

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QueryRequest(BaseModel):
    question: str

class MatchedChunk(BaseModel):
    content: str
    url: str
    position: int
    similarity_score: float

class QueryResponse(BaseModel):
    answer: str
    status: str = "success"

class HealthResponse(BaseModel):
    status: str
    message: str

# Global RAG agent instance
rag_agent = None

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG agent on startup"""
    global rag_agent
    logger.info("Initializing RAG Agent...")
    try:
        rag_agent = RAGAgent()
        logger.info("RAG Agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG Agent: {e}")
        raise

@app.post("/ask", response_model=QueryResponse)
async def ask_rag(request: QueryRequest):
    """
    Process a user query through the RAG agent and return the response
    """
    logger.info(f"Processing query: {request.question[:50]}...")

    try:
        # Validate input
        if not request.question or len(request.question.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        if len(request.question) > 2000:
            raise HTTPException(status_code=400, detail="Query too long, maximum 2000 characters")

        # Process query through RAG agent
        response = await rag_agent.query_agent(request.question)
        
        # 🔒 LOG DEBUG DATA (not returned)
        logger.info(f"Sources: {response.get('sources')}")
        logger.info(f"Similarity scores: {[c.get('similarity_score') for c in response.get('matched_chunks', [])]}")

        return QueryResponse(
            answer=response.get("answer", "No answer found"),
            status="success"
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return QueryResponse(
            answer="Something went wrong while processing your question.",
            status="error"
        )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    return HealthResponse(
        status="healthy",
        message="RAG Agent API is running"
    )

# For running with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


