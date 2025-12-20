# Implementation Plan: RAG Book Project — Spec 5: Frontend Integration with Agentic RAG Backend

**Version**: 1.0
**Status**: Draft
**Author**: Gemini

## 1. Technical Context

This plan outlines the technical implementation for "RAG Book Project — Spec 5: Frontend Integration with Agentic RAG Backend". The objective is to integrate the FastAPI-based Agentic RAG backend (Spec-4) with the Docusaurus book frontend to enable an interactive chatbot experience. This will establish reliable local communication between frontend and backend, allowing users to query the book content through the published site interface.

-   **Core Problem**: The RAG backend exists but lacks a user-facing interface within the Docusaurus book.
-   **Strategy**:
    1.  Create a new React component within Docusaurus for the chatbot UI.
    2.  Implement an API client module in TypeScript for communicating with the FastAPI backend.
    3.  Integrate the chatbot component into the Docusaurus layout (e.g., sidebar, global component, or a dedicated page).
    4.  Implement state management within the React component to handle user input, loading states, error messages, and displaying responses.
    5.  Add functionality to capture user-selected text and send it with the query.
    6.  Provide a mechanism for configuring the backend URL (e.g., via Docusaurus config or environment variables).
-   **Dependencies**: React (native to Docusaurus), `axios` or `fetch` API for HTTP requests, potentially Docusaurus theming/swizzling for component placement.
-   **Key Files**: `src/components/Chatbot/index.tsx` (main chatbot UI), `src/api/ragApi.ts` (API client), `docusaurus.config.ts` (for integration), potentially `src/theme/Layout/index.js` (for global placement).

## 2. Constitution Check

-   **Utility**: Integrating the chatbot directly into the Docusaurus book significantly enhances its utility by providing an interactive Q&A experience based on the book's content.
-   **Clarity & Accessibility**: The chatbot UI will be designed for clear user interaction and response display. The API client will provide a clear interface for frontend-backend communication.
-   **Spec-Driven Consistency**: The implementation will strictly adhere to the requirements of Spec 5, ensuring the chatbot uses the defined backend API contract from Spec 4.
-   **Reproducibility**: The Docusaurus React component will be easily integrated and configured, ensuring reproducibility for local development setups.

## 3. Implementation Phases

### Phase 0: Research & Setup

#### **Research Needs**

-   **Docusaurus Component Integration**: Investigate best practices for adding custom React components to Docusaurus, including component location (`src/components` vs. swizzling), styling, and integration points within the layout.
-   **Contextual Text Selection**: Research methods for programmatically capturing user-selected text in a Docusaurus/React environment and associating it with the chatbot's input.
-   **Environment Variable Handling in Docusaurus**: Understand how to securely and effectively pass environment-specific variables (like the backend URL) from the Docusaurus build process to a React component.

#### **Key Decisions (with Rationale & Alternatives)**

-   **Chatbot Placement**: The chatbot will initially be implemented as a global component, potentially displayed as a floating button or a collapsible sidebar panel. This allows for accessibility from any page without modifying core Docusaurus layouts directly, making it easier to integrate and less intrusive. (Alternative: Dedicated chatbot page, less integrated; Swizzling Docusaurus Layout, more intrusive initially).
-   **API Client**: A dedicated TypeScript API client (`src/api/ragApi.ts`) will be used to encapsulate all communication with the RAG backend. This promotes separation of concerns and reusability. (Alternative: inline `fetch` calls, less maintainable).
-   **Backend URL Configuration**: The backend URL will be configured via `docusaurus.config.ts` and passed down to the React component, allowing for easy environment-based switching (e.g., `process.env.BACKEND_URL` for local vs production).

### Phase 1: Design & Contracts

#### **Data Model (`specs/013-rag-frontend-integration/data-model.md`)**

The frontend will interact with the backend using the data models defined in `specs/004-rag-agent-fastapi/data-model.md`: `QueryInput`, `AgentResponse`, `RetrievalDebugResponse`, and `HealthStatus`.
-   **Frontend-specific state**:
    -   `ChatbotState`: Represents the internal state of the chatbot UI.
        -   `messages`: List of chat messages (user input, agent response).
        -   `isLoading`: Boolean indicating if a response is pending.
        -   `error`: String for displaying error messages.
        -   `backendUrl`: Configured URL for the RAG backend.

#### **API Contracts (`specs/013-rag-frontend-integration/contracts/openapi.yaml`)**

The frontend will adhere to the existing backend API contracts defined in `specs/004-rag-agent-fastapi/contracts/openapi.yaml`. No new API contracts are needed for this Spec. This file will remain a reference to the backend's API.

#### **Quickstart (`specs/013-rag-frontend-integration/quickstart.md`)**

A `quickstart.md` file will be created to document:
1.  **Backend Setup**: Instructions to ensure the FastAPI backend is running locally.
2.  **Frontend Setup**: How to start the Docusaurus development server.
3.  **Chatbot Interaction**: Guide on how to use the chatbot UI (typing questions, selecting text) and verify responses.
4.  **Backend URL Configuration**: Instructions for setting the backend URL.

## 4. Next Steps

-   Proceed with `/sp.tasks` to break down the implementation into detailed tasks.