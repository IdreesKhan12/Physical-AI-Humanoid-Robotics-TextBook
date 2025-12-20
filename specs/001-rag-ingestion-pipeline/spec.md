# Feature Specification: RAG Book Ingestion Pipeline

**Version**: 1.0
**Status**: Draft
**Author**: Gemini

## 1. Overview

### 1.1. Feature Name

RAG Book Ingestion Pipeline

### 1.2. Objective

Create the complete backend pipeline for ingesting the published Docusaurus book URLs, generating text embeddings using Cohere, and storing the vectors in a Qdrant Cloud collection.

### 1.3. Target Audience

This spec serves developers who will build and maintain the RAG pipeline for the unified book project.

## 2. User Scenarios & Acceptance Criteria

### 2.1. Scenario: Running the Ingestion Pipeline

-   **Given** a deployed Docusaurus website.
-   **When** a developer executes the ingestion script.
-   **Then** the script automatically discovers all content URLs.
-   **And** scrapes the main content from each URL, excluding UI boilerplate.
-   **And** chunks the text into smaller segments.
-   **And** generates a vector embedding for each chunk using Cohere.
-   **And** stores each vector and its metadata (URL, heading, chunk text, chunk index) in a Qdrant collection.
-   **And** the process is idempotent.

## 3. Functional Requirements

### 3.1. URL Discovery

-   The system must automatically discover all unique content URLs from the deployed Docusaurus website.

### 3.2. Content Scraping

-   The system must extract the main article text from each URL.
-   It must effectively exclude common UI elements like navigation bars, sidebars, headers, and footers.
-   It must ignore code blocks unless they are marked as relevant.

### 3.3. Text Chunking

-   The system must split the scraped text into smaller, overlapping chunks (400-800 tokens).

### 3.4. Embedding Generation

-   The system must generate a vector embedding for each text chunk using the Cohere Embed v3 model.

### 3.5. Vector Storage

-   The system must store each vector in the specified Qdrant Cloud collection.
-   Each vector must be stored with the following metadata payload:
    -   `URL`: The source URL of the content.
    -   `heading`: The most relevant heading (e.g., `H1`, `H2`) for the chunk.
    -   `chunk_text`: The actual text content of the chunk.
    -   `chunk_index`: The 0-based index of the chunk within the page.
-   The collection name must follow the global naming convention.

### 3.6. Idempotency

-   The system must generate a unique, deterministic ID for each text chunk.
-   Running the ingestion script multiple times must not create duplicate vectors for the same content.

### 3.7. Logging

-   The script must log ingestion statistics: total URLs, total chunks, embedding time, and Qdrant upload time.

## 4. Out of Scope

-   Chatbot functionality.
-   Retrieval code.
-   Agents, FastAPI, or OpenAI integration.
-   UI or frontend components.
-   Streaming ingestion or incremental updates.

## 5. Assumptions

-   A Qdrant Cloud Free Tier account is available.
-   A Cohere API key is available.
-   The Docusaurus website is deployed and accessible via a public URL.
