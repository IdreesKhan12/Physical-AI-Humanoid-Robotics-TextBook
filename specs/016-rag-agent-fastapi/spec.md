# Feature Specification: RAG Book Project — Spec 4: Agentic RAG Backend with FastAPI

**Feature Branch**: `004-rag-agent-fastapi`  
**Created**: 2025-12-18  
**Status**: Draft  
**Input**: User description: "RAG Book Project — Spec 4: Agentic RAG Backend with FastAPI Objective: Design and implement a production-ready RAG Agent using the OpenAI Agents SDK. The Agent must retrieve relevant book content from Qdrant using Cohere embeddings and generate answers strictly grounded in retrieved context. Expose the Agent via a FastAPI backend to support future frontend integration. Context: Spec-1 completed vector ingestion and embedding storage. Spec-2 validated retrieval accuracy, metadata integrity, and pipeline stability. This Spec builds the reasoning and serving layer on top of the verified retrieval system. Spec-3 Bug fix the retrievel data. Target: Backend developers implementing the Agent layer responsible for: - retrieval - context construction - controlled response generation Success Criteria: - Create an OpenAI Agent using the Agents SDK as the core LLM interface. - Integrate Qdrant retrieval using the validated Spec-2 pipeline. - Generate query embeddings using Cohere (no alternative embedding models). - Agent responses must: - use only retrieved book content - cite or reference relevant sections when applicable - explicitly state when insufficient context is available - Implement a deterministic context-builder that: - selects top-k chunks - removes duplicates - enforces token limits - Support optional user-selected text as a retrieval constraint. - Expose FastAPI endpoints: - POST `/ask` → question + optional selected text → Agent answer - POST `/debug/retrieval` → retrieval results only - GET `/health` → system and Qdrant connectivity status - Add structured logging for: - embedding generation - retrieval scores - final Agent output - Include error handling for: - empty retrieval results - Qdrant connectivity failures - embedding service errors Technical Constraints: - Must use OpenAI Agents SDK (no raw ChatCompletion usage). - Must use FastAPI as the HTTP interface. - Must reuse Spec-2 retrieval logic without modification. - Must run under Python 3.11 using the existing UV environment. - No frontend integration in this Spec. Not Building: - No UI or client-side code. - No authentication or user accounts. - No streaming responses. - No fine-tuning or prompt-engineering experiments. - No vector ingestion or mutation. Timeline: Complete within 3–4 days. Output: - FastAPI backend under `backend/` - Agent definition module - Retrieval + context-builder modules - Minimal test script validating `/ask` endpoint correctness"

## User Scenarios & Testing

### User Story 1 - Ask Question (Priority: P1)

A user wants to ask a question related to the book content and receive an answer strictly grounded in the book, with citations if available.

**Why this priority**: This is the core functionality of a RAG chatbot, providing direct value to the end-user by enabling interactive queries against the book's knowledge base.

**Independent Test**: This can be fully tested by sending a question to the `/ask` endpoint and verifying the response's content, grounding, and optional citations. It delivers a functional answer-generation capability.

**Acceptance Scenarios**:

1.  **Given** the RAG Agent FastAPI backend is running and the Qdrant collection is populated, **When** a user sends a POST request to `/ask` with a question, **Then** the Agent responds with an answer derived solely from the book content.
2.  **Given** a question for which there is insufficient context in the book, **When** a user sends a POST request to `/ask` with that question, **Then** the Agent explicitly states that it cannot answer due to insufficient context.
3.  **Given** a question with relevant content, **When** the Agent responds, **Then** the response includes citations or references to the relevant sections of the book.

---

### User Story 2 - Debug Retrieval (Priority: P2)

A developer wants to inspect the raw retrieval results (top-k chunks) for a given query to debug or understand the context provided to the Agent.

**Why this priority**: Essential for development, debugging, and understanding Agent behavior. This directly supports the quality and maintainability of the core RAG functionality.

**Independent Test**: This can be fully tested by sending a question to the `/debug/retrieval` endpoint and inspecting the returned chunks. It delivers transparency and debuggability for the retrieval process.

**Acceptance Scenarios**:

1.  **Given** the RAG Agent FastAPI backend is running, **When** a developer sends a POST request to `/debug/retrieval` with a question, **Then** the API returns a list of top-k retrieved content chunks from Qdrant.

---

### User Story 3 - Health Check (Priority: P3)

A system administrator or monitoring tool needs to check the health and connectivity status of the RAG Agent backend and its dependencies (Qdrant).

**Why this priority**: Important for operational monitoring and ensuring the service's availability and reliability.

**Independent Test**: This can be fully tested by sending a GET request to the `/health` endpoint and verifying the status. It delivers basic service monitoring.

**Acceptance Scenarios**:

1.  **Given** the RAG Agent FastAPI backend is running, **When** a GET request is sent to `/health`, **Then** the API returns a status indicating the system's health and Qdrant connectivity.

## Requirements

### Functional Requirements

-   **FR-001**: System MUST create an OpenAI Agent using the Agents SDK as the core LLM interface.
-   **FR-002**: System MUST integrate Qdrant retrieval using the validated Spec-2 pipeline.
-   **FR-003**: System MUST generate query embeddings using Cohere (no alternative embedding models).
-   **FR-004**: Agent responses MUST use only retrieved book content.
-   **FR-005**: Agent responses MUST cite or reference relevant sections when applicable.
-   **FR-006**: Agent responses MUST explicitly state when insufficient context is available.
-   **FR-007**: System MUST implement a deterministic context-builder that: selects top-k chunks, removes duplicates, enforces token limits.
-   **FR-008**: System MUST support optional user-selected text as a retrieval constraint.
-   **FR-009**: System MUST expose a POST `/ask` endpoint accepting a question and optional selected text, returning the Agent's answer.
-   **FR-010**: System MUST expose a POST `/debug/retrieval` endpoint accepting a question, returning retrieval results only.
-   **FR-011**: System MUST expose a GET `/health` endpoint returning system and Qdrant connectivity status.
-   **FR-012**: System MUST add structured logging for embedding generation, retrieval scores, and final Agent output.
-   **FR-013**: System MUST include error handling for empty retrieval results, Qdrant connectivity failures, and embedding service errors.

### Key Entities

-   **Question**: Natural language query from the user.
-   **Selected Text**: Optional user-provided text to constrain retrieval.
-   **Answer**: Agent's response, grounded in retrieved context.
-   **Retrieved Chunk**: A segment of book content from Qdrant, including metadata.

## Success Criteria

### Measurable Outcomes

-   **SC-001**: 95% of relevant questions about book content receive a grounded answer within 5 seconds.
-   **SC-002**: Agent responses accurately cite or reference retrieved book sections in at least 90% of cases where context is sufficient.
-   **SC-003**: The `/health` endpoint reliably reports Qdrant connectivity status with 100% accuracy.
-   **SC-004**: Deployment to existing Python 3.11 environment in `backend/` is seamless and functional.

## Out of Scope

-   No UI or client-side code.
-   No authentication or user accounts.
-   No streaming responses.
-   No fine-tuning or prompt-engineering experiments.
-   No vector ingestion or mutation.

## Technical Constraints

-   Must use OpenAI Agents SDK (no raw ChatCompletion usage).
-   Must use FastAPI as the HTTP interface.
-   Must reuse Spec-2 retrieval logic without modification.
-   Must run under Python 3.11 using the existing UV environment.
-   No frontend integration in this Spec.

## Assumptions

-   A valid OpenAI API key is available for the Agent.
-   A populated Qdrant collection, as per Spec-1, is available and accessible.
-   A Cohere API key is available for embedding generation.
-   The existing Python 3.11 development environment and UV package manager are utilized.