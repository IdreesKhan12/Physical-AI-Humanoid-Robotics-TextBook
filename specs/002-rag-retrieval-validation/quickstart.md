# Quickstart: RAG Retrieval Testing & Pipeline Validation

This guide provides instructions on how to set up the environment, run the validation tests for the RAG retrieval pipeline, and interpret the results.

## 1. Environment Setup

Before running the tests, ensure you have the following:

-   Python 3.9+ installed.
-   `uv` installed for dependency management.
-   Your Qdrant Cloud instance is running and accessible.
-   Your Cohere API key is valid.

1.  **Navigate to the `backend` directory:**
    ```bash
    cd backend
    ```

2.  **Update and install dependencies:**
    Ensure your `requirements.txt` is up-to-date (it should contain `pytest` and `pytest-dotenv`).
    ```bash
    uv pip install -r requirements.txt
    ```

3.  **Configure environment variables:**
    Create or update the `.env` file in the `backend/` directory with your API keys and Qdrant URL:
    ```
    COHERE_API_KEY="your_cohere_api_key_here"
    QDRANT_URL="https://your-qdrant-cloud-url-here.gcp.cloud.qdrant.io:6333"
    QDRANT_API_KEY="your_qdrant_api_key_here"
    ```
    Make sure the Qdrant collection (`physical_ai_textbook`) has been populated by the RAG Ingestion Pipeline (Spec 1).

## 2. Running Tests

Navigate to the `backend/` directory in your terminal and execute `pytest`.

```bash
# Run all tests
pytest

# Run only diagnostic tests
pytest -m diagnostic

# Run only retrieval tests
pytest -m retrieval
```

## 3. Interpreting Results

-   **Passed Tests (`.`):** A dot indicates a successful test.
-   **Failed Tests (`F`):** An 'F' indicates a failed test. The console output will provide details on the assertion failure.
-   **Skipped Tests (`s`):** An 's' indicates a skipped test (if any conditions for skipping are met).

For failed tests, review the traceback and error messages to debug. Common issues include:
-   Incorrect API keys or Qdrant URL.
-   Missing data in the Qdrant collection.
-   Unexpected data format or content.
-   Network connectivity issues.

The tests are designed to provide clear feedback on the health and performance of your RAG pipeline's retrieval component.
