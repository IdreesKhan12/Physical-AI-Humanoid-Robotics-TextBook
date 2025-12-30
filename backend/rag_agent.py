from typing import List, Dict, Optional
import google.generativeai as genai
# from google import genai

import json
import logging
import time

from backend.retrieval import get_query_embedding
from backend.retrieval import search_qdrant
from backend.retrieval import deterministic_context_builder

QDRANT_COLLECTION_NAME = "physical_ai_textbook"

# from backend.retrieval import get_query_embedding, search_qdrant, deterministic_context_builder, QDRANT_COLLECTION_NAME
# from backend.utils import get_env_variable

logger = logging.getLogger(__name__)

# Configure Gemini client
# genai.configure(api_key=get_env_variable("GEMINI_API_KEY"))
# genai.configure(api_key=GEMINI_API_KEY)
# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class RAGAgent:
    def __init__(self, model: str = "gemini-2.0-flash", max_context_tokens: int = 8000):
        self.model = genai.GenerativeModel(model)
        self.max_context_tokens = max_context_tokens

    def _get_gemini_prompt(self, context: str, question: str) -> str:
        """
        Generates the prompt for the Gemini LLM, including the retrieved context.
        """
        return f"""You are a helpful assistant that answers questions about the book "Physical AI & Humanoid Robotics".
Your answers MUST be strictly grounded in the provided context. If the answer cannot be found in the context,
you MUST state "I cannot answer this question based on the provided context." Do NOT make up information.

When providing an answer, cite the source URL and heading from the context.
Format citations as "[Source: <URL>, Heading: <Heading>]" at the end of the sentence or paragraph it supports.
If no specific heading is available, just use the URL.

Context:
{context}

Question: {question}
"""

    def answer_question(self, question: str, selected_text: Optional[str] = None) -> Dict:
        """
        Answers a question using RAG by retrieving context and querying a Gemini LLM.
        """
        start_time = time.time()
        try:
            # 1. Generate query embedding
            logger.info("Generating query embedding...")
            query_text = f"{selected_text} {question}" if selected_text else question
            query_embedding = get_query_embedding(query_text)
            logger.info("Query embedding generated.")

            # 2. Search Qdrant for relevant chunks
            logger.info(f"Searching Qdrant collection '{QDRANT_COLLECTION_NAME}'...")
            retrieved_chunks = search_qdrant(query_embedding,collection_name=QDRANT_COLLECTION_NAME , k=10)

            if not retrieved_chunks:
                logger.warning(f"No chunks retrieved for question: '{question}'")
                return {
                    "answer": "I cannot answer this question based on the provided context.",
                    "citations": [],
                    "metadata": {"retrieval_score": 0.0, "model_used": "gemini-1.5-flash", "response_time_ms": int((time.time() - start_time) * 1000)}
                }
            
            avg_retrieval_score = sum([c['score'] for c in retrieved_chunks]) / len(retrieved_chunks)
            logger.info(f"Retrieved {len(retrieved_chunks)} chunks with average score: {avg_retrieval_score:.2f}")

            # 3. Build context for the LLM
            logger.info("Building context for LLM...")
            context = deterministic_context_builder(retrieved_chunks, self.max_context_tokens)
            logger.info("Context built.")

            # 4. Query LLM
            logger.info("Querying Gemini LLM...")
            prompt = self._get_gemini_prompt(context, question)
            
            response = self.model.generate_content(prompt)

            
            agent_answer = response.text
            logger.info("LLM responded.")

            # 5. Extract citations (simple approach)
            citations = []
            for chunk in retrieved_chunks:
                citations.append({
                    "url": chunk.get("url", "N/A"),
                    "heading": chunk.get("heading", "N/A"),
                    "chunk_text_snippet": chunk.get("chunk_text", "")[:100] + "..."
                })
            
            end_time = time.time()
            response_time_ms = int((end_time - start_time) * 1000)
            logger.info(f"RAG Agent finished processing in {response_time_ms}ms.")

            return {
                "answer": agent_answer,
                "citations": citations,
                "metadata": {
                    "retrieval_score": avg_retrieval_score,
                    "model_used": "gemini-1.5-flash",
                    "response_time_ms": response_time_ms
                }
            }

        except Exception as e:
            logger.exception(f"Error in RAG Agent for question: '{question}'")
            raise 
            


