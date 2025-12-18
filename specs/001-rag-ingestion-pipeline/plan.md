# Implementation Plan: RAG Book Ingestion Pipeline

**Version**: 1.0
**Status**: Draft
**Author**: Gemini

## 1. Technical Context

This plan outlines the technical implementation for the RAG Book Ingestion Pipeline. The goal is to create a single Python script (`ingestion.py`) that handles URL discovery, content scraping, text chunking, embedding generation, and vector storage.

-   **Project Initialization**: A new `backend/` directory will be created, and a Python environment will be managed using `uv`.
-   **Core Logic**: The entire pipeline will be implemented in a single file, `backend/ingestion.py`.
-   **Dependencies**:
    -   `httpx`: For making HTTP requests to fetch web content.
    -   `beautifulsoup4`: For parsing HTML and extracting text.
    -   `cohere`: The official Python client for the Cohere API.
    -   `qdrant-client`: The official Python client for Qdrant.
    -   `python-dotenv`: To manage environment variables for API keys.
    -   `lxml`: For XML parsing of the sitemap.
    -   `uuid`: For generating deterministic IDs.

## 2. Constitution Check

-   **Utility**: The script will be a practical tool for indexing the book content, directly supporting RAG functionality.
-   **Clarity & Accessibility**: The code will be modular and well-commented to ensure it's understandable.
-   **Spec-Driven Consistency**: The implementation will strictly follow the approved specification.
-   **Reproducibility**: The script will be deterministic and produce the same vector IDs for the same content.

## 3. Implementation Phases

### Phase 1: Core Ingestion Logic

#### **System Design (`backend/ingestion.py`)**

The script will be organized into the following functions:

-   `get_all_urls(sitemap_url: str) -> list[str]`: Fetches and parses the `sitemap.xml` to extract all content URLs. Will use `BeautifulSoup` with `lxml-xml` parser.
-   `extract_text_from_url(url: str) -> dict`: Fetches the HTML from a URL, uses `BeautifulSoup` to extract and clean the main text content, ignoring code blocks by default, and extracts the page title for metadata.
-   `chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]`: Splits the text into overlapping chunks based on the specified size. Will use a simple word-based splitter for now.
-   `generate_deterministic_id(content_hash: str) -> str`: Generates a UUID for a text chunk based on its content's hash to ensure idempotency.
-   `embed_chunks(chunks: list[str], cohere_client) -> list[list[float]]`: Generates embeddings for a list of text chunks using the Cohere client.
-   `create_and_store_vectors(chunks_data: list[dict], collection_name: str, qdrant_client)`:
    -   Checks if the Qdrant collection exists; if not, creates it with the correct vector size (1024) and distance metric (COSINE).
    -   Upserts the chunks (with their embeddings and metadata) to the Qdrant collection. Metadata will include: `URL`, `heading` (page title), `chunk_text`, `chunk_index`.
-   `main(sitemap_url: str)`: The main function that orchestrates the entire pipeline, calling the other functions in the correct order. It will also log ingestion statistics.

### Phase 2: Validation and Reporting

-   **Basic Validation Tests**:
    -   A simple check will be added to the `main` function to verify that the number of vectors in Qdrant is greater than zero after ingestion.
    -   The script will print a summary report to the console confirming the total URLs processed, chunks created, and vectors uploaded.

## 4. Next Steps

-   Proceed with `/sp.tasks` to break down the implementation into detailed tasks.
