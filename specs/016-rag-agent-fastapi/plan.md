# Implementation Plan: RAG Book Project — Spec 4: Agentic RAG Backend with FastAPI

**Version**: 1.0
**Status**: Draft
**Author**: Gemini

## 1. Technical Context

This plan outlines the technical implementation for "RAG Book Project — Spec 4: Agentic RAG Backend with FastAPI". The objective is to design and implement a production-ready RAG Agent using the OpenAI Agents SDK, capable of retrieving relevant book content from Qdrant using Cohere embeddings and generating answers strictly grounded in retrieved context. The Agent will be exposed via a FastAPI backend to support future frontend integration.

-   **Core Problem**: The project requires a RAG chatbot capable of answering questions based on the book's content, exposed via a FastAPI backend. This involves integrating an OpenAI Agent, Qdrant retrieval, and Cohere embeddings, ensuring responses are strictly grounded in retrieved context.
-   **Strategy**:
    1.  Initialize a FastAPI application within the `backend/` directory.
    2.  Develop an OpenAI Agent using the OpenAI Agents SDK for conversational capabilities.
    3.  Integrate Qdrant retrieval, reusing the validated Spec-2 pipeline, to fetch relevant book content.
    4.  Implement a deterministic context-builder that processes retrieved chunks (top-k selection, deduplication, token limits) to provide grounded context to the Agent.
    5.  Expose `/ask`, `/debug/retrieval`, and `/health` endpoints via FastAPI.
    6.  Implement structured logging and comprehensive error handling.
-   **Dependencies**: `fastapi`, `uvicorn`, `openai-agents-sdk` (or `openai` directly if `openai-agents-sdk` is not a direct dependency but a conceptual one), `qdrant-client`, `cohere`, `python-dotenv`, `pytest` (for minimal endpoint testing).
-   **Key Files**: `backend/main.py` (FastAPI app), `backend/rag_agent.py` (Agent definition and orchestration), `backend/retrieval.py` (retrieval and context building logic).

## 2. Constitution Check

-   **Utility**: The RAG chatbot provides a practical tool for interacting with the book's content, directly enhancing its utility by offering an intelligent, queryable interface.
-   **Clarity & Accessibility**: The FastAPI application will feature auto-generated OpenAPI documentation, making the API clear and accessible. The Agent's responses will be designed for clarity, aiming for grounded and understandable answers.
-   **Spec-Driven Consistency**: The implementation will strictly adhere to the requirements outlined in Spec 4. It will reuse the proven Qdrant retrieval logic from Spec 2, ensuring consistency with established components.
-   **Reproducibility**: The solution will be developed within the existing Python 3.11 environment, managed by UV, ensuring that the setup and execution are reproducible for other developers.

## 3. Implementation Phases

### Phase 0: Research & Setup

#### **Research Needs**

-   **OpenAI Agents SDK Integration Patterns**: Investigate best practices for integrating the OpenAI Agents SDK within a FastAPI application. This includes understanding how to define tools, manage agent state, and handle asynchronous operations.
-   **Deterministic Context Building**: Research robust techniques for deterministic context building, particularly concerning token limits and optimal methods for deduplication and chunk selection (e.g., considering hierarchical chunking or re-ranking strategies if needed, within the "deterministic" constraint).
-   **FastAPI Error Handling for External Services**: Explore FastAPI's recommended approaches for handling errors from external API calls (Qdrant, Cohere, OpenAI), ensuring graceful degradation and informative error messages.

#### **Key Decisions (with Rationale & Alternatives)**

-   **RAG Agent Structure**: The RAG Agent logic will be encapsulated in a dedicated Python module (`backend/rag_agent.py`). This centralizes the Agent's definition, tool orchestration, and LLM interaction, promoting modularity and maintainability.
-   **Context Builder Implementation**: A separate utility module (`backend/context_builder.py`) will be created to manage deterministic chunk selection, deduplication, and token limiting. This separation of concerns ensures the context-building logic is reusable and testable independently.
-   **FastAPI Endpoints Location**: The `/ask`, `/debug/retrieval`, and `/health` FastAPI endpoints will be defined directly within `backend/main.py`. This keeps the main application file focused on API routing and request/response handling.

### Phase 1: Design & Contracts

#### **Data Model (`specs/004-rag-agent-fastapi/data-model.md`)**

-   **QueryInput**: Represents the input for asking a question to the RAG Agent.
    -   `question` (string, required): The natural language query from the user.
    -   `selected_text` (string, optional): User-provided text to constrain retrieval, used as an additional query parameter or filter for Qdrant.
-   **AgentResponse**: Represents the structured response from the RAG Agent.
    -   `answer` (string): The Agent's response to the question.
    -   `citations` (list of objects, optional): A list of source citations. Each object will contain:
        -   `url` (string): The URL of the source document.
        -   `heading` (string, optional): The main heading of the content section.
        -   `chunk_text_snippet` (string): A short snippet of the retrieved text that directly supports the answer.
    -   `metadata` (object, optional): Additional metadata about the response, such as `retrieval_score` (average score of retrieved chunks), `model_used` (e.g., "gpt-4"), `response_time_ms`.
-   **RetrievalDebugResponse**: Provides detailed information about the retrieval process for debugging.
    -   `query_embedding` (list of float): The embedding generated for the user's query.
    -   `retrieved_chunks` (list of objects): A list of the top-k retrieved content chunks from Qdrant. Each object will typically include:
        -   `url` (string)
        -   `heading` (string)
        -   `chunk_text` (string)
        -   `chunk_index` (integer)
        -   `score` (float)
-   **HealthStatus**: Represents the health and connectivity status of the backend and its dependencies.
    -   `status` (string): Overall status ("ok" or "error").
    -   `qdrant_status` (string): Connectivity status to Qdrant ("connected", "disconnected", "error").
    -   `cohere_status` (string): Connectivity status to Cohere ("connected", "disconnected", "error").
    -   `openai_status` (string): Connectivity status to OpenAI ("connected", "disconnected", "error").
    -   `timestamp` (string): ISO format timestamp of the health check.

#### **API Contracts (`specs/004-rag-agent-fastapi/contracts/openapi.yaml`)**

An OpenAPI 3.0 specification will be generated for the FastAPI endpoints:
-   `POST /ask`: Accepts `QueryInput` and returns `AgentResponse`.
-   `POST /debug/retrieval`: Accepts `QueryInput` and returns `RetrievalDebugResponse`.
-   `GET /health`: Returns `HealthStatus`.

#### **Quickstart (`specs/004-rag-agent-fastapi/quickstart.md`)**

A `quickstart.md` file will be created to document:
1.  **Environment Setup**: Instructions for setting up the Python 3.11 UV environment and installing dependencies.
2.  **Configuration**: How to configure `.env` variables for OpenAI, Cohere, and Qdrant.
3.  **Running the FastAPI App**: Commands to start the Uvicorn server.
4.  **Testing Endpoints**: Example `curl` commands or Python snippets to interact with `/ask`, `/debug/retrieval`, and `/health`.

## 4. Next Steps

-   Proceed with `/sp.tasks` to break down the implementation into detailed tasks.