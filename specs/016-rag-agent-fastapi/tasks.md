# Task Plan: RAG Book Project — Spec 4: Agentic RAG Backend with FastAPI

This document outlines the tasks required to implement the RAG Agent FastAPI backend, ordered by dependency and user story priority.

## Phase 1: Setup

- [X] T001 Create `backend/` directory if it doesn't exist.
- [X] T002 Create `backend/requirements.txt` and add `fastapi`, `uvicorn`, `openai`, `qdrant-client`, `cohere`, `python-dotenv`.
- [X] T003 Create `backend/.env` with placeholders for `OPENAI_API_KEY`, `COHERE_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, and `QDRANT_COLLECTION_NAME`.
- [X] T004 Create an empty `backend/main.py` file for the FastAPI application.
- [X] T005 Create an empty `backend/rag_agent.py` file for the RAG Agent definition.
- [X] T006 Create an empty `backend/retrieval.py` file for retrieval and context building logic.

## Phase 2: Foundational Tasks

- [X] T007 Implement a utility function in `backend/utils.py` (or similar) to load environment variables from `.env`.
- [X] T008 Initialize `QdrantClient` in `backend/retrieval.py` using `QDRANT_URL` and `QDRANT_API_KEY` from `.env`. Ensure `prefer_grpc=True` and `api_key` is passed directly.
- [X] T009 Initialize `CohereClient` in `backend/retrieval.py` using `COHERE_API_KEY` from `.env`.
- [X] T010 Implement `get_query_embedding(text: str) -> List[float]` function in `backend/retrieval.py` using the Cohere client.
- [X] T011 Implement `search_qdrant(query_vector: List[float], collection_name: str, k: int = 5, filters: dict = None) -> List[dict]` function in `backend/retrieval.py` using the Qdrant client.

## Phase 3: User Story 1 - Ask Question (P1)

Goal: Implement the core RAG Agent functionality and the `/ask` endpoint.
Independent Test: Send a question to `/ask` and verify the grounded answer with citations.

- [X] T012 Implement `deterministic_context_builder(retrieved_chunks: List[dict], max_tokens: int) -> str` in `backend/retrieval.py` to select top-k unique chunks and enforce token limits.
- [X] T013 Define an `OpenAI Agent` in `backend/rag_agent.py` that utilizes tools for `qdrant_retrieval` (using `get_query_embedding` and `search_qdrant`) and `context_building` (using `deterministic_context_builder`).
- [X] T014 Implement the `/ask` FastAPI endpoint in `backend/main.py`. This endpoint should:
    - Accept `QueryInput` (question, optional selected_text).
    - Use the Cohere client to get the query embedding.
    - Use `search_qdrant` to retrieve relevant chunks, potentially applying filters from `selected_text`.
    - Use `deterministic_context_builder` to construct the context for the agent.
    - Invoke the `OpenAI Agent` with the user's question and the constructed context.
    - Return `AgentResponse` (answer, citations, metadata).

## Phase 4: User Story 2 - Debug Retrieval (P2)

Goal: Implement the `/debug/retrieval` endpoint for inspecting raw retrieval results.
Independent Test: Send a question to `/debug/retrieval` and inspect the raw chunks.

- [X] T015 Implement the `/debug/retrieval` FastAPI endpoint in `backend/main.py`. This endpoint should:
    - Accept `QueryInput` (question).
    - Use the Cohere client to get the query embedding.
    - Use `search_qdrant` to retrieve relevant chunks.
    - Return `RetrievalDebugResponse` (query embedding, retrieved chunks).

## Phase 5: User Story 3 - Health Check (P3)

Goal: Implement the `/health` endpoint for system and dependency status.
Independent Test: Send a GET request to `/health` and verify the status.

- [X] T016 Implement a `check_qdrant_status()` function in `backend/utils.py` (or similar).
- [X] T017 Implement a `check_cohere_status()` function in `backend/utils.py` (or similar).
- [X] T018 Implement a `check_openai_status()` function in `backend/utils.py` (or similar).
- [X] T019 Implement the `/health` FastAPI endpoint in `backend/main.py`. This endpoint should:
    - Call the status check functions for Qdrant, Cohere, and OpenAI.
    - Return `HealthStatus` indicating overall and individual service statuses.

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T020 Implement structured logging for embedding generation, retrieval scores, and final Agent output (`backend/main.py`, `backend/rag_agent.py`, `backend/retrieval.py`).
- [X] T021 Implement comprehensive error handling for all endpoints, covering empty retrieval results, Qdrant connectivity failures, and embedding service errors (`backend/main.py`, `backend/rag_agent.py`, `backend/retrieval.py`).
- [X] T022 Update `backend/requirements.txt` with exact versions of all installed dependencies after initial development.
- [X] T023 Finalize `specs/004-rag-agent-fastapi/quickstart.md` with accurate commands and examples.
- [X] T024 Finalize `specs/004-rag-agent-fastapi/contracts/openapi.yaml` by auto-generating it from the FastAPI app (after implementation).

## Dependencies

- Phase 2 tasks depend on Phase 1 tasks.
- Phase 3 tasks depend on Phase 2 tasks.
- Phase 4 tasks depend on Phase 2 tasks.
- Phase 5 tasks depend on Phase 2 tasks.
- Phase 6 tasks can be integrated throughout development but are finalized after core functionality.

## Parallel Execution

- Tasks within Phase 1 (T001-T006) can be executed in parallel.
- Tasks within Phase 2 (T007-T011) can be executed in parallel (after T007).
- Phases 3, 4, and 5 can be developed largely in parallel once Phase 2 is complete, as they implement distinct endpoints.
- T012 (context builder) can be developed in parallel with T013 (Agent definition) once retrieval functions are stable.

## Implementation Strategy

The implementation will follow an iterative approach, prioritizing User Story 1 (Ask Question) for early value delivery. Each user story will be developed and tested independently. Foundational components will be built first, followed by the core RAG Agent logic and then the supplementary endpoints. Structured logging and error handling will be integrated throughout development and refined in the final phase.
