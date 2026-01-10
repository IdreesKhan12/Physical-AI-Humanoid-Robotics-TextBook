import os
import json
import logging
import time
from typing import Dict, List, Any

from dotenv import load_dotenv
from openai import AsyncOpenAI 
from agents import Agent, Runner, set_default_openai_client 
from agents import function_tool

# --------------------------------------------------
# ENV & LOGGING
# --------------------------------------------------
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------------------------------------
# OPENAI CLIENT INIT (ONCE)
# --------------------------------------------------
def init_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found")

    client = AsyncOpenAI(api_key=api_key)
    set_default_openai_client(client)

def retrieve_information_internal(query: str) -> Dict:
    from backend.retrieval import RAGRetriever
    retriever = RAGRetriever()

    try:
        raw = retriever.retrieve(query_text=query, top_k=3, threshold=0.3)
        parsed = json.loads(raw)

        chunks = []
        for r in parsed.get("results", []):
            chunks.append({
                "text": r["content"],
                "source": r["url"],
                "score": r["similarity_score"]
            })

        return {
            "retrieved_chunks": chunks,
            "total_results": len(chunks)
        }

    except Exception as e:
        return {
            "retrieved_chunks": [],
            "total_results": 0,
            "error": str(e)
        }

# --------------------------------------------------
# TOOL: RETRIEVAL
# --------------------------------------------------

@function_tool
def retrieve_information(query: str) -> Dict:
    return retrieve_information_internal(query)



# --------------------------------------------------
# RAG AGENT
# --------------------------------------------------
class RAGAgent:
    def __init__(self):
        init_openai_client()
        from backend.rag_agent import retrieve_information

        self.agent = Agent(
            name="RAG Assistant",
            instructions= """
You are the **Specialized AI Assistant** for the **Physical AI & Humanoid Robotics Capstone Course**.
Your primary function is to support students in understanding the curriculum, hardware prerequisites, system architectures, and foundational principles that connect a digital AI "brain" to a physical robotic body.


You are a course assistant.
- Greet users politely if they greet you.
- Answer ONLY using retrieved course content.
- If information is missing, say it is not covered.
- Do NOT mention sources unless explicitly asked.


        """,
            tools=[retrieve_information],
            model="gpt-4.1-mini"
        )

        logger.info("RAG Agent initialized")

    # --------------------------------------------------
    # PUBLIC METHOD (FastAPI uses this)
    # --------------------------------------------------
    async def query_agent(self, query_text: str) -> Dict[str, Any]:
        return await self._async_query_agent(query_text)

    # --------------------------------------------------
    # CORE ASYNC LOGIC
    # --------------------------------------------------
    
    async def _async_query_agent(self, query_text: str) -> Dict:
        start_time = time.time()

        try:
            logger.info(f"Processing query: {query_text}")

            # 🔥 STEP 1: FORCE retrieval yourself
            # from backend.rag_agent import retrieve_information
            retrieval = retrieve_information_internal(query_text)

            chunks = retrieval.get("retrieved_chunks", [])

            if not chunks:
                return {
                    "answer": (
                        "I cannot answer this question because it is not covered "
                        "in the Physical AI & Humanoid Robotics course material."
                    ),
                    "sources": [],
                    "matched_chunks": [],
                    "query_time_ms": (time.time() - start_time) * 1000,
                    "confidence": "low"
                }

            # 🔒 STEP 2: Build STRICT context
            context = "\n\n".join(
                f"[Chunk {i+1}]\n{c['text']}"
                for i, c in enumerate(chunks)
            )

            agent_input = f"""
    You MUST answer ONLY using the context below.
    If the answer is not explicitly present, say you cannot answer.

    CONTEXT:
    {context}

    QUESTION:
    {query_text}
    """

            # 🤖 STEP 3: Run agent (NO tool dependency now)
            result = await Runner.run(self.agent, agent_input)
            answer_text = result.final_output or ""

            return {
                "answer": answer_text,
                "sources": [c.get("source") for c in chunks if c.get("source")],
                "matched_chunks": chunks,
                "query_time_ms": (time.time() - start_time) * 1000,
                "confidence": "high"
            }

        except Exception as e:
            logger.exception("Agent execution failed")
            return {
                "answer": "",
                "error": str(e),
                "confidence": "low"
            }

# --------------------------------------------------
# CONFIDENCE (OPTIONAL – future use)
# --------------------------------------------------
def calculate_confidence(chunks: List[Dict]) -> str:
    if not chunks:
        return "low"

    avg = sum(c.get("similarity_score", 0) for c in chunks) / len(chunks)
    if avg >= 0.7:
        return "high"
    elif avg >= 0.4:
        return "medium"
    return "low"
