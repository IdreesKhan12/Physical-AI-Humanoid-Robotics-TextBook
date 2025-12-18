# Task Plan: RAG Retrieval Testing & Pipeline Validation

This document outlines the tasks required to implement the RAG retrieval testing and pipeline validation.

## Phase 1: Setup

- [X] T001 Update `backend/requirements.txt` to include `pytest` and `pytest-dotenv`.
- [X] T002 Create `backend/pytest.ini` with custom markers (`diagnostic`, `retrieval`) and configure `pytest-dotenv`.
- [X] T003 Create an empty `backend/test_validation.py` file.

## Phase 2: Foundational Tasks (Client Setup and Collection Schema)

- [X] T004 [US1] In `backend/test_validation.py`, implement the `qdrant_client()` fixture to initialize and return a Qdrant client, loading credentials from `.env`.
- [X] T005 [US1] In `backend/test_validation.py`, implement the `cohere_client()` fixture to initialize and return a Cohere client, loading credentials from `.env`.
- [X] T006 [US1] In `backend/test_validation.py`, implement `test_collection_schema(qdrant_client)` to verify the Qdrant collection's existence, vector size, and distance metric.

## Phase 3: Diagnostic Tests (User Scenarios 2.2, 2.3, 2.4)

- [X] T007 [US2] In `backend/test_validation.py`, implement `test_metadata_completeness(qdrant_client)` to verify all required metadata fields are present and not empty.
- [X] T008 [US3] In `backend/test_validation.py`, implement `test_no_empty_vectors(qdrant_client)` to check for zero-norm vectors.
- [X] T009 [US4] In `backend/test_validation.py`, implement `test_duplicate_chunks(qdrant_client)` to identify points with identical `chunk_text`.

## Phase 4: Retrieval Tests (User Scenario 2.1)

- [X] T010 [US1] In `backend/test_validation.py`, define `TEST_QUERIES` as a list of dictionaries, each containing a query, expected keywords, and top_k.
- [X] T011 [US1] In `backend/test_validation.py`, implement `test_general_question_retrieval(qdrant_client, cohere_client, test_query)` to perform similarity searches and validate results.
- [X] T012 [US1] In `backend/test_validation.py`, implement `test_metadata_filtering(qdrant_client, cohere_client)` to test retrieval with metadata filters.

## Phase 5: Quickstart Documentation

- [X] T013 Create `specs/002-rag-retrieval-validation/quickstart.md` to document environment setup, running tests, and interpreting results.

## Dependencies

- All tasks in Phase 1 must be completed before starting Phase 2.
- All tasks in Phase 2 must be completed before starting Phase 3.
- All tasks in Phase 3 must be completed before starting Phase 4.
- Task T013 can be started after Phase 1, but its content relies on all implementation phases.

## Parallel Execution

- Tasks within Phase 3 (T007-T009) can be implemented in parallel.
- Tasks within Phase 4 (T011-T012) can be implemented in parallel (after T010).

## Implementation Strategy

The validation will be implemented as a `pytest` suite in `backend/test_validation.py`. Fixtures will be used for client initialization. Diagnostic tests will ensure data integrity, and retrieval tests will validate the semantic search capabilities.