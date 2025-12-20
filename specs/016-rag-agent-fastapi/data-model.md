# Data Model: RAG Book Project — Spec 4: Agentic RAG Backend with FastAPI

This document defines the key data structures for the RAG Agent FastAPI backend.

## QueryInput

Represents the input for asking a question to the RAG Agent.

-   `question` (string, required): The natural language query from the user.
-   `selected_text` (string, optional): User-provided text to constrain retrieval, used as an additional query parameter or filter for Qdrant.

## AgentResponse

Represents the structured response from the RAG Agent.

-   `answer` (string): The Agent's response to the question.
-   `citations` (list of objects, optional): A list of source citations. Each object will contain:
    -   `url` (string): The URL of the source document.
    -   `heading` (string, optional): The main heading of the content section.
    -   `chunk_text_snippet` (string): A short snippet of the retrieved text that directly supports the answer.
-   `metadata` (object, optional): Additional metadata about the response, such as `retrieval_score` (average score of retrieved chunks), `model_used` (e.g., "gpt-4"), `response_time_ms`.

## RetrievalDebugResponse

Provides detailed information about the retrieval process for debugging.

-   `query_embedding` (list of float): The embedding generated for the user's query.
-   `retrieved_chunks` (list of objects): A list of the top-k retrieved content chunks from Qdrant. Each object will typically include:
    -   `url` (string)
    -   `heading` (string)
    -   `chunk_text` (string)
    -   `chunk_index` (integer)
    -   `score` (float)

## HealthStatus

Represents the health and connectivity status of the backend and its dependencies.

-   `status` (string): Overall status ("ok" or "error").
-   `qdrant_status` (string): Connectivity status to Qdrant ("connected", "disconnected", "error").
-   `cohere_status` (string): Connectivity status to Cohere ("connected", "disconnected", "error").
-   `openai_status` (string): Connectivity status to OpenAI ("connected", "disconnected", "error").
-   `timestamp` (string): ISO format timestamp of the health check.
