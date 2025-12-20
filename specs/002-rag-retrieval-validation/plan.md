# Implementation Plan: RAG Retrieval Testing & Pipeline Validation

**Version**: 1.0
**Status**: Draft
**Author**: Gemini

## 1. Technical Context

This plan outlines the technical implementation for validating the RAG pipeline. The validation will be implemented as a Python test suite using `pytest`. This suite will cover various aspects: Qdrant collection health, vector quality, metadata integrity, and the accuracy of retrieval using Cohere embeddings.

-   **Project Initialization**: The test suite will reside in the `backend/` directory, ideally alongside `main.py` or in a dedicated `backend/tests/` subdirectory.
-   **Core Logic**: The validation will use `pytest` for test organization and execution.
-   **Dependencies**:
    -   `pytest`: For test framework.
    -   `pytest-dotenv`: To load environment variables for tests.
    -   `cohere`: The official Python client for the Cohere API.
    -   `qdrant-client`: The official Python client for Qdrant.
    -   `python-dotenv`: To manage environment variables.

## 2. Constitution Check

-   **Utility**: The test suite provides practical verification of the RAG pipeline, ensuring its functionality and data integrity.
-   **Clarity & Accessibility**: Tests will be clearly named and structured, making it easy for developers to understand the validation logic and results.
-   **Spec-Driven Consistency**: The tests will directly implement and verify the success criteria defined in the feature specification.
-   **Reproducibility**: The tests will be designed to be deterministic, yielding consistent results given a stable Qdrant collection.

## 3. Implementation Phases

### Phase 0: Research

No specific research is required, as the technologies (`pytest`, `cohere`, `qdrant-client`) are well-understood.

### Phase 1: Design and Contracts

#### **Data Model (`specs/002-rag-retrieval-validation/data-model.md`)**

The data model primarily revolves around the expected structure of test queries and their corresponding expected results, building upon the `BookChunk` concept from the ingestion pipeline.

-   **Entity**: `TestQuery`
    -   `query_text` (string): The natural language query to embed and test retrieval.
    -   `expected_keywords` (list of strings): Keywords expected to be found in retrieved chunks.
    -   `expected_heading` (string, optional): An optional heading to filter by.
    -   `top_k` (integer): The number of top results to retrieve.

-   **Entity**: `RetrievedChunk` (implicitly verified, matches `BookChunk` payload structure)
    -   `URL` (string)
    -   `heading` (string)
    -   `chunk_text` (string)
    -   `chunk_index` (integer)
    -   `score` (float): Qdrant's similarity score.

#### **API Contracts**

-   Not applicable, as this is a test suite, not an API.

#### **System Design (`backend/test_validation.py`)**

A `pytest` test file (`backend/test_validation.py`) will be created to house the validation logic.

-   **Pytest Fixtures**:
    -   `qdrant_client()`: Initializes and returns a Qdrant client, loading credentials from `.env`.
    -   `cohere_client()`: Initializes and returns a Cohere client, loading credentials from `.env`.

-   **Diagnostic Tests (`@pytest.mark.diagnostic`)**:
    -   `test_collection_schema(qdrant_client)`: Verifies the Qdrant collection exists and has the correct vector size and distance metric.
    -   `test_metadata_completeness(qdrant_client)`: Iterates through a sample of points to ensure all required metadata fields (`URL`, `heading`, `chunk_text`, `chunk_index`) are present and not empty.
    -   `test_no_empty_vectors(qdrant_client)`: Checks a sample of vectors to ensure they are not all zeros (indicating failed embeddings).
    -   `test_duplicate_chunks(qdrant_client)`: Identifies any points with identical `chunk_text` to verify ingestion idempotency.

-   **Retrieval Tests (`@pytest.mark.retrieval`)**:
    -   `test_general_question_retrieval(qdrant_client, cohere_client, test_query)`:
        -   Takes a parameterized `test_query` (from a predefined list).
        -   Generates an embedding for the query using Cohere.
        -   Performs a Qdrant similarity search.
        -   Asserts that a sufficient number of results are returned.
        -   Asserts that retrieved results contain expected keywords (from `test_query`).
    -   `test_metadata_filtering(qdrant_client, cohere_client)`:
        -   Tests retrieval with a query and a metadata filter (e.g., by `heading`).
        -   Asserts that all retrieved results match the specified filter.

-   **Configuration**:
    -   A `pytest.ini` file will be created in the `backend/` directory to define custom markers (`diagnostic`, `retrieval`) and configure `pytest-dotenv` to load `.env` files.
    -   `backend/requirements.txt` will be updated to include `pytest` and `pytest-dotenv`.

#### **Quickstart (`specs/002-rag-retrieval-validation/quickstart.md`)**

A `quickstart.md` file will be created in `specs/002-rag-retrieval-validation/` to document:

1.  **Environment Setup**:
    -   Instructions to update dependencies with `uv`.
    -   Instructions to configure the `.env` file with Cohere and Qdrant credentials.
2.  **Running Tests**:
    -   The command to execute the `pytest` suite.
    -   How to run specific test categories (e.g., `pytest -m retrieval`).
3.  **Interpreting Results**:
    -   Explanation of expected output and failure scenarios.

## 4. Next Steps

-   Proceed with `/sp.tasks` to break down the implementation into detailed tasks.
