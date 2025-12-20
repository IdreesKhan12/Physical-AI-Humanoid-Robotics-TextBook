# Task Plan: RAG Compatibility Refactor

This document outlines the tasks required to fix the RAG validation test suite.

## Phase 1: Environment and Dependency Management

- [X] T001 Update `backend/requirements.txt` to pin `qdrant-client` to version `1.7.0` and remove `langsmith` and `fastembed`.

## Phase 2: Refactor Test Suite (User Story 1: Fix Tests)

- [X] T002 [US1] In `backend/test_validation.py`, update the `qdrant_client` fixture to initialize with `prefer_grpc=True`.
- [X] T003 [US1] In `backend/test_validation.py`, refactor `test_collection_schema` to use `collection_info.config.params.vectors` to access the vector configuration.
- [X] T004 [US1] In `backend/test_validation.py`, refactor `test_general_question_retrieval` to use `qdrant_client.search()` instead of any deprecated methods.
- [X] T005 [US1] In `backend/test_validation.py`, refactor `test_metadata_filtering` to use `qdrant_client.search()` instead of any deprecated methods.

## Dependencies

- All tasks in Phase 1 must be completed before starting Phase 2.

## Implementation Strategy

The implementation will focus on refactoring the existing `test_validation.py` file to align with the stable `qdrant-client` version 1.7.0 and a Python 3.11 environment. This will involve updating the client initialization, API calls, and data structure accessors.