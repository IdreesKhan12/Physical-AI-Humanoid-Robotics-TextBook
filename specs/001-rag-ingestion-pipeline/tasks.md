# Task Plan: RAG Ingestion Pipeline

This document outlines the tasks required to implement the RAG Ingestion Pipeline.

## Phase 1: Project Setup

- [X] T001 Create the `backend/` directory.
- [X] T002 Create a `backend/requirements.txt` file with the dependencies: `httpx`, `beautifulsoup4`, `cohere`, `qdrant-client`, `python-dotenv`, `lxml`, `uuid`.
- [X] T003 Create a `backend/.env` file with placeholders for `COHERE_API_KEY`, `QDRANT_URL`, and `QDRANT_API_KEY`.
- [X] T004 Create an empty `backend/ingestion.py` file.

## Phase 2: Core Ingestion Logic (User Story 1: Ingestion)

- [X] T005 [US1] In `backend/ingestion.py`, implement the `get_all_urls` function to fetch and parse the `sitemap.xml`.
- [X] T006 [US1] In `backend/ingestion.py`, implement the `extract_text_from_url` function to fetch and clean HTML content.
- [X] T007 [US1] In `backend/ingestion.py`, implement the `chunk_text` function to split text into overlapping chunks.
- [X] T008 [US1] In `backend/ingestion.py`, implement the `generate_deterministic_id` function to create a unique ID for each chunk.
- [X] T009 [US1] In `backend/ingestion.py`, implement the `embed_chunks` function to generate embeddings with Cohere.
- [X] T010 [US1] In `backend/ingestion.py`, implement `create_and_store_vectors` to create the Qdrant collection and upsert vectors with metadata.

## Phase 3: Orchestration and Validation (User Story 1: Ingestion)

- [X] T011 [US1] In `backend/ingestion.py`, implement the `main` function to orchestrate the entire pipeline and log statistics.
- [X] T012 [US1] In `backend/ingestion.py`, add a validation check in the `main` function to confirm that vectors were successfully uploaded to Qdrant.

## Dependencies

- Phase 2 depends on Phase 1.
- Phase 3 depends on Phase 2.

## Implementation Strategy

The implementation will be done in a single file (`backend/ingestion.py`). Each function will be implemented and can be tested individually before being integrated into the final `main` function.