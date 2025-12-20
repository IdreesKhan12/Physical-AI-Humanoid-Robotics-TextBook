from typing import List, Dict, Optional
from qdrant_client import QdrantClient, models
import os
import cohere # Added import
import logging # Import logging
from backend.utils import get_env_variable
from qdrant_client.models import Filter
import time
from dotenv import load_dotenv

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

# Initialize Cohere Client
cohere_client = cohere.Client(get_env_variable("COHERE_API_KEY"))

def get_query_embedding(text: str) -> List[float]:
    """
    Generates a Cohere embedding for the given text.
    """
    try:
        response = cohere_client.embed(
            texts=[text],
            model="embed-english-v3.0", # Using a common Cohere embedding model
            input_type="search_query"
        )
        logger.info(f"Generated embedding for text snippet: '{text[:50]}...'")
        return response.embeddings[0]
    except Exception as e:
        logger.exception(f"Error generating embedding with Cohere for text: '{text[:50]}...'")
        raise

def deterministic_context_builder(retrieved_chunks: List[Dict], max_tokens: int) -> str:
    """
    Selects top-k unique chunks, removes duplicates, enforces token limits,
    and formats them into a context string.
    """
    context_parts = []
    seen_texts = set()
    current_tokens = 0

    for chunk in retrieved_chunks:
        chunk_text = chunk.get('chunk_text', '')
        
        # Simple deduplication
        if chunk_text in seen_texts:
            logger.debug(f"Skipping duplicate chunk: {chunk_text[:50]}...")
            continue
        seen_texts.add(chunk_text)

        # Estimate tokens (simple character count for now)
        # TODO: Replace with proper tokenizer (e.g., tiktoken) if token accuracy is critical
        estimated_tokens = len(chunk_text) / 4 # Rough estimate: 1 token ~ 4 characters

        if current_tokens + estimated_tokens > max_tokens:
            logger.warning(f"Max context tokens ({max_tokens}) reached. Truncating context.")
            break

        # Format chunk with metadata for context
        source_info = f"Source: {chunk.get('url', 'N/A')}"
        heading_info = f"Heading: {chunk.get('heading', 'N/A')}" if chunk.get('heading') else ""
        
        formatted_chunk = f"--- Document Start ---\n{heading_info}\n{source_info}\n{chunk_text}\n--- Document End ---\n"
        
        context_parts.append(formatted_chunk)
        current_tokens += estimated_tokens
    
    logger.info(f"Built context with {len(context_parts)} chunks, estimated {current_tokens:.0f} tokens.")
    return "\n".join(context_parts)

def search_qdrant(query_vector: List[float], collection_name: str, k: int = 5, filters: Dict = None) -> List[Dict]:
    """
    Searches the Qdrant collection for relevant chunks using the .search() method.
    """
    try:

        qdrant_filter = Filter(**filters) if filters else None
        logger.info(f"Searching Qdrant collection '{collection_name}' with limit {k} and filters: {filters}")
        search_result = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=k,
            # query_filter=models.Filter(**filters) if filters else None,
            query_filter=qdrant_filter,
            with_payload=True, # Ensure payload is returned
        )
        
        # The .search() method returns a list of ScoredPoint objects.
        # The payload is directly accessible.
        results = []
        for hit in search_result:
            if hit.payload is not None:
                payload = hit.payload
                payload['score'] = hit.score # Add score to payload
                results.append(payload)
            else:
                logger.warning(f"Found a hit with no payload: {hit}")

        logger.info(f"Found {len(results)} results from Qdrant.")
        return results
    except Exception as e:
        logger.exception(f"An unexpected error occurred while searching Qdrant collection '{collection_name}': {e}")
        raise e




# from qdrant_client import QdrantClient
# from qdrant_client.models import Filter, ScoredPoint
# from typing import List, Dict
# import logging

# logger = logging.getLogger(__name__)

# def search_qdrant(
#     query_vector: List[float], 
#     collection_name: str, 
#     k: int = 5, 
#     filters: Dict = None
# ) -> List[Dict]:
#     """
#     Searches the Qdrant collection using QdrantClient v1.16.2 API.
#     """
#     try:
#         logger.info(f"Searching Qdrant collection '{collection_name}' with limit {k} and filters: {filters}")

#         qdrant_filter = Filter(**filters) if filters else None

#         search_result: List[ScoredPoint] = qdrant_client.points.search(
#             collection_name=collection_name,
#             query_vector=query_vector,
#             limit=k,
#             query_filter=qdrant_filter,
#             with_payload=True
#         )

#         results = []
#         for hit in search_result:
#             if hit.payload:
#                 payload = hit.payload
#                 payload['score'] = hit.score
#                 results.append(payload)
#             else:
#                 logger.warning(f"Found a hit with no payload: {hit}")

#         logger.info(f"Found {len(results)} results from Qdrant.")
#         return results

#     except Exception as e:
#         logger.exception(f"An unexpected error occurred while searching Qdrant collection '{collection_name}': {e}")
#         raise e



