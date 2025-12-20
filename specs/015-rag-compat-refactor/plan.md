# Implementation Plan: RAG Compatibility Refactor

**Version**: 1.0
**Status**: Draft
**Author**: Gemini

## 1. Technical Context

This plan outlines the technical refactoring required to fix the failing RAG validation test suite. The primary goal is to eliminate the native dependency crashes and align the test suite with a stable, modern version of the `qdrant-client` SDK.

-   **Core Problem**: The test suite is failing due to a combination of Python version incompatibility (3.13), breaking changes in the `qdrant-client` API, and the unintended loading of the `fastembed` library, which has unstable native dependencies (`onnxruntime`).
-   **Strategy**:
    1.  Refactor the Qdrant client initialization to explicitly disable `fastembed`.
    2.  Update all API calls to use the current, correct methods and attribute names.
    3.  Pin the `qdrant-client` version to a known stable release that works well with Python 3.11.

-   **Dependencies**:
    -   `pytest`
    -   `pytest-dotenv`
    -   `cohere`
    -   `qdrant-client` (pinned to a specific stable version)
    -   `python-dotenv`

## 2. Constitution Check

-   **Utility**: This refactor is critical to providing a working, testable retrieval pipeline, which is a core utility of the project.
-   **Clarity & Accessibility**: The refactored code will be clearer as it will use the modern, documented API for `qdrant-client`.
-   **Spec-Driven Consistency**: This plan directly addresses the failures to meet Spec 2's success criteria.
-   **Reproducibility**: By pinning the `qdrant-client` version and using a standard Python version (3.11), we ensure a reproducible and stable testing environment.

## 3. Implementation Phases

### Phase 1: Refactor `test_validation.py`

This phase focuses on updating the existing test suite to be compatible with the modern `qdrant-client` SDK and to be more robust.

#### **System Design (`backend/test_validation.py`)**

-   **`qdrant_client()` fixture**:
    -   **Update**: The `QdrantClient` will be initialized with `prefer_grpc=True` and by passing the API key in the `api_key` parameter. This combination is more robust and less likely to trigger on-device inference features.
-   **`test_collection_schema()`**:
    -   **Update**: The assertion for the collection's vector configuration will be changed from `collection_info.vectors_config` (old API) to `collection_info.config.params.vectors` (current API).
-   **`test_general_question_retrieval()` and `test_metadata_filtering()`**:
    -   **Update**: The deprecated `.search()` method will be replaced with the current `.query()` method (if `fastembed` is disabled) or, more specifically, the recommended `.search()` method from a stable client version. We will standardize on `.search()` for clarity.

### Phase 2: Environment and Dependency Management

-   **`requirements.txt`**:
    -   **Update**: The `qdrant-client` dependency will be pinned to a specific, stable version like `1.7.0` to avoid pulling in versions with breaking changes or unstable native dependencies.
    -   **Update**: The `langsmith` and `fastembed` dependencies will be explicitly removed, as they are not needed and are the source of the crashes.

## 4. Next Steps

-   Proceed with `/sp.tasks` to break down the refactoring into detailed, actionable tasks.
