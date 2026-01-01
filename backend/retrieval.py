from typing import List, Dict, Optional
from qdrant_client import QdrantClient, models
import os
import logging # Import logging
from backend.utils import get_env_variable
from qdrant_client.models import Filter
import time
from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI

logger = logging.getLogger(__name__)

load_dotenv()

# Load Qdrant configuration from environment variables
QDRANT_URL = get_env_variable("QDRANT_URL")
QDRANT_API_KEY = get_env_variable("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = get_env_variable("QDRANT_COLLECTION_NAME", "physical_ai_textbook")

# Initialize Qdrant Client
# Ensure prefer_grpc=True for better performance and API_KEY is passed correctly
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    prefer_grpc=False

)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def build_context(chunks: list[dict], max_tokens: int = 1200) -> str:
    context = []
    used_tokens = 0
    seen = set()

    for chunk in chunks:
        text = chunk.get("chunk_text", "")
        if not text or text in seen:
            continue
        seen.add(text)

        est_tokens = len(text) // 4
        if used_tokens + est_tokens > max_tokens:
            break

        context.append(text)
        used_tokens += est_tokens

    return "\n\n".join(context)

def get_embedding(text: str):
    try:
        resp = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return resp.data[0].embedding
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def retrieve_data(query: str) -> list[str]:
    """
    Retrieve relevant textbook chunks from Qdrant
    """
    embedding = get_embedding(query)

    
    if embedding is None:
        raise HTTPException(
            status_code=429,
            detail="Embedding rate limit exceeded. Please try later."
        )

    results = qdrant_client.query_points(
        collection_name=QDRANT_COLLECTION_NAME,
        query=embedding,
        limit=5,
        with_payload=True,
    )

    # return [point.payload["chunk_text"] for point in results]
    retrieved = []
    for point in results.points:
        payload = point.payload or {}
        payload["score"] = point.score
        retrieved.append(payload)

    return retrieved
