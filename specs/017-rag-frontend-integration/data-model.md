# Data Model: RAG Book Project — Spec 5: Frontend Integration with Agentic RAG Backend

This document defines the key data structures for the frontend integration with the RAG Agent FastAPI backend.

## Frontend-specific state

### ChatbotState

Represents the internal state of the chatbot UI.

-   `messages` (List of Message objects): A history of chat messages (user input, agent response).
-   `isLoading` (Boolean): Indicates if a response from the backend is currently pending.
-   `error` (String, optional): Stores any error messages to be displayed to the user.
-   `backendUrl` (String): The configured URL for the RAG backend.

### Message

Represents a single message in the chat history.

-   `id` (String): Unique identifier for the message.
-   `sender` (String): "user" or "agent".
-   `text` (String): The content of the message.
-   `timestamp` (String): ISO format timestamp of when the message was created.
-   `citations` (List of Citation objects, optional): Citations if the sender is "agent".

## Backend Data Models (Reference from Spec-4)

The frontend will interact with the backend using the data models defined in `specs/004-rag-agent-fastapi/data-model.md`. These include:

-   **QueryInput**:
    -   `question` (string): The natural language query from the user.
    -   `selected_text` (string, optional): User-provided text to constrain retrieval.
-   **AgentResponse**:
    -   `answer` (string): The Agent's response to the question.
    -   `citations` (list of Citation objects, optional).
    -   `metadata` (object, optional): Additional metadata about the response.
-   **Citation**: (as defined in Spec-4 data model)
    -   `url` (string)
    -   `heading` (string, optional)
    -   `chunk_text_snippet` (string)
-   **RetrievalDebugResponse**: (not directly used by chatbot UI, but part of backend contract)
-   **HealthStatus**: (used for frontend to check backend health)
    -   `status` (string)
    -   `qdrant_status` (string)
    -   `cohere_status` (string)
    -   `openai_status` (string)
    -   `timestamp` (string)
