---
id: 1
title: Specify RAG Compatibility Refactor
stage: spec
date: 2025-12-18
surface: agent
model: gemini-pro
feature: 003-rag-compat-refactor
branch: 003-rag-compat-refactor
user: user
command: /sp.specify
labels: [spec, bugfix, refactor]
links:
  spec: specs/003-rag-compat-refactor/spec.md
  ticket: null
  adr: null
  pr: null
files:
- specs/003-rag-compat-refactor/spec.md
- specs/003-rag-compat-refactor/checklists/requirements.md
tests:
- none
---

## Prompt

/sp.specify RAG Book Project — Spec 2 Bug Fix & Compatibility Refactor Objective: Fix all failing tests and runtime crashes in Spec 2 caused by Python version incompatibility, Qdrant client API changes, and unintended fastembed/onnxruntime loading. The goal is to make the retrieval pipeline stable, testable, and fully compliant with the current Qdrant Python SDK. Context: Current test execution fails with: - Windows access violation caused by onnxruntime via fastembed - Invalid Qdrant client API usage (search(), vectors_config) - Python 3.13 incompatibility with native dependencies Success Criteria: - All Spec-2 retrieval tests pass successfully on Windows. - No native crashes (onnxruntime / fastembed must not load). - Qdrant collection schema is validated using the correct SDK attributes. - Vector retrieval works using the modern Qdrant API. - Tests run deterministically and are safe to re-execute. Required Fixes: - Refactor Qdrant client initialization to explicitly disable fastembed. - Update all retrieval calls to use `query_points()` instead of deprecated methods. - Update collection schema access to match `collection_info.config.params.vectors`. - Ensure Cohere embeddings are used exclusively for queries. - Make the test suite compatible with Python 3.11 (not 3.13). Constraints: - Do NOT change Spec-1 ingestion logic or regenerate embeddings. - Do NOT introduce new vector databases or embedding models. - Do NOT add FastAPI, Agents SDK, or frontend code. - Maintain existing project structure under the `backend/` directory. Output: - Corrected Spec-2 test files - Updated Qdrant client initialization - Passing test results with no runtime crashes

## Response snapshot

Created the feature specification and requirements checklist for the RAG Compatibility Refactor.

## Outcome

- ✅ Impact: Created spec and checklist.
- 🧪 Tests: None.
- 📁 Files: 2 created.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: None.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
