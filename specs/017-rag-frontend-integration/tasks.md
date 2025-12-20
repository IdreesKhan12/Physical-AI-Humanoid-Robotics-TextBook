# Task Plan: RAG Book Project — Spec 5: Frontend Integration with Agentic RAG Backend

This document outlines the tasks required to implement the RAG chatbot frontend integration, ordered by dependency and user story priority.

## Phase 1: Setup

- [X] T001 Create `src/components/Chatbot/` directory for the main chatbot UI component.
- [X] T002 Create `src/components/Chatbot/index.tsx` for the main chatbot React component.
- [X] T003 Create `src/api/` directory for the API client module.
- [X] T004 Create `src/api/ragApi.ts` for the TypeScript API client.
- [X] T005 Update `docusaurus.config.ts` to include configuration for the backend URL (e.g., as a custom field or theme config property).
- [X] T006 Modify `package.json` to include any necessary frontend dependencies (e.g., `axios` if used, `uuid` for message IDs).
- [X] T007 Create `src/css/custom.css` (if not exists) for initial chatbot styling.

## Phase 2: Foundational Tasks

- [X] T008 Implement API client functions in `src/api/ragApi.ts` for `POST /ask`, `GET /health`, and potentially `POST /debug/retrieval` (if needed for internal testing/development). These functions should handle request/response types based on Spec-4's data models.
- [X] T009 Implement a utility function in `src/api/ragApi.ts` to retrieve the configured backend URL from Docusaurus environment/config.

## Phase 3: User Story 1 - Ask Question via Chatbot (P1)

Goal: Implement the core chatbot UI and integrate with the `/ask` endpoint.
Independent Test: Use the chatbot UI to ask a question and verify the grounded answer.

- [X] T010 [US1] In `src/components/Chatbot/index.tsx`, implement the basic UI structure (input field, send button, message display area).
- [X] T011 [US1] In `src/components/Chatbot/index.tsx`, implement state management for user input, loading status, and messages.
- [X] T012 [US1] In `src/components/Chatbot/index.tsx`, implement the `sendMessage` function to:
    - Call the API client's `ask` function.
    - Display a loading indicator.
    - Update messages with user input and agent response.
    - Handle and display errors.
- [X] T013 [US1] Integrate `src/components/Chatbot/index.tsx` into a Docusaurus layout or page (e.g., `src/theme/Layout/index.js` or a new MDX page).

## Phase 4: User Story 2 - Ask Question with Selected Text (P1)

Goal: Enable sending user-selected text as context to the backend.
Independent Test: Select text, ask a question, and verify the answer is relevant to the selected text.

- [X] T014 [US2] In `src/components/Chatbot/index.tsx` (or a utility module), implement logic to capture user-selected text from the DOM.
- [X] T015 [US2] Modify the `sendMessage` function in `src/components/Chatbot/index.tsx` to include the captured `selected_text` in the `POST /ask` request payload.

## Phase 5: User Story 3 - Backend URL Configuration (P2)

Goal: Ensure backend URL is configurable via environment.
Independent Test: Change the configured URL and verify communication.

- [X] T016 [US3] In `src/components/Chatbot/index.tsx` (or `src/api/ragApi.ts`), use the configured backend URL from Docusaurus config.
- [X] T017 [US3] Document the process for setting the `RAG_BACKEND_URL` environment variable in `specs/013-rag-frontend-integration/quickstart.md`.

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T018 Implement basic request validation (e.g., question not empty) and response sanitization (e.g., preventing XSS) within `src/components/Chatbot/index.tsx`.
- [X] T019 Enhance error message display in `src/components/Chatbot/index.tsx` for clarity and user-friendliness.
- [X] T020 Ensure the chatbot UI component does not interfere with Docusaurus navigation or layout (requires careful CSS and React component placement).
- [X] T021 Finalize `specs/013-rag-frontend-integration/quickstart.md` with accurate commands and examples for frontend setup and interaction.

## Dependencies

- Phase 2 tasks depend on Phase 1 tasks.
- Phase 3 tasks depend on Phase 2 tasks.
- Phase 4 tasks depend on Phase 3 tasks (specifically T012 `sendMessage`).
- Phase 5 tasks depend on Phase 2 tasks (specifically T009 to retrieve URL).
- Phase 6 tasks can be integrated throughout development but are finalized after core functionality.

## Parallel Execution

- Tasks within Phase 1 (T001-T007) can be executed in parallel.
- T008 and T009 can be developed in parallel within Phase 2.
- Phase 3 (UI, state, API integration) can start once T008/T009 are complete.
- Phase 4 (selected text) can be implemented alongside Phase 3 or after.
- Phase 5 (URL config) can be implemented alongside other phases.

## Implementation Strategy

The implementation will follow an iterative approach, prioritizing User Story 1 (Ask Question via Chatbot) for early value delivery. Foundational API client logic will be built first, followed by the core chatbot UI. Subsequent user stories will enhance the chatbot's functionality, and polish tasks will ensure robustness and integration quality.
