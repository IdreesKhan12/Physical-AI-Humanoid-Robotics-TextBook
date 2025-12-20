# Feature Specification: RAG Book Project — Spec 2 Bug Fix & Compatibility Refactor

**Version**: 1.0
**Status**: Draft
**Author**: Gemini

## 1. Overview

### 1.1. Feature Name

RAG Book Project — Spec 2 Bug Fix & Compatibility Refactor

### 1.2. Objective

Fix all failing tests and runtime crashes in Spec 2 caused by Python version incompatibility, Qdrant client API changes, and unintended fastembed/onnxruntime loading. The goal is to make the retrieval pipeline stable, testable, and fully compliant with the current Qdrant Python SDK.

### 1.3. Target Audience

This spec is for developers who are fixing the broken RAG validation test suite.

## 2. User Scenarios & Acceptance Criteria

### 2.1. Scenario: Running the Validation Suite

-   **Given** a correctly configured local environment with Python 3.11.
-   **When** a developer runs `pytest` in the `backend` directory.
-   **Then** all diagnostic and retrieval tests pass without any `AttributeError` or `Windows fatal exception` crashes.
-   **And** the test report confirms successful validation of the Qdrant collection schema and data integrity.
-   **And** the retrieval tests confirm that the `search` method (or its modern equivalent) works correctly.

## 3. Functional Requirements

### 3.1. Qdrant Client Refactor

-   The `QdrantClient` initialization must be updated to explicitly disable any `fastembed` or on-device inference features to prevent native crashes.
-   All calls to the Qdrant client for vector search must be updated from the deprecated `.search()` or `.query()` methods to the modern, correct equivalent (e.g., `.query_points()`).
-   All calls to get collection information must be updated to use the correct attribute for accessing vector configuration (e.g., `collection_info.config.params.vectors`).

### 3.2. Test Suite Correction

-   The `test_validation.py` suite must be updated to be compatible with the refactored Qdrant client calls.
-   All assertions must be updated to match the data structures returned by the modern Qdrant SDK.

### 3.3. Environment Compatibility

-   The `requirements.txt` file must be updated to ensure it uses a stable version of `qdrant-client` that is compatible with Python 3.11 and does not have problematic native dependencies.

## 4. Out of Scope

-   Changing the core logic of the Spec-1 ingestion script.
-   Introducing any new database or embedding models.
-   Adding any FastAPI, Agent, or frontend code.

## 5. Assumptions

-   The development environment will be standardized on Python 3.11 to ensure compatibility.
-   The Qdrant collection has been successfully populated with data from the Spec 1 ingestion script.
