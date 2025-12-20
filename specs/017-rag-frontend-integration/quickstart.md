# Quickstart: RAG Book Project — Spec 5: Frontend Integration with Agentic RAG Backend

This guide provides instructions on how to set up, run, and interact with the RAG chatbot integrated into the Docusaurus frontend.

## 1. Backend Setup

Before starting the Docusaurus frontend, ensure the FastAPI RAG backend from **Spec 4** is running.

1.  **Navigate to the project's root directory** (e.g., `physical-ai-and-humanoid-robotics/`).
2.  **Install Python dependencies**: (If not already done)
    ```bash
    uv pip install -r backend/requirements.txt
    ```
3.  **Configure Environment Variables**: Ensure your `.env` file in `backend/` has the necessary API keys (`GEMINI_API_KEY`, `COHERE_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`).
4.  **Start the FastAPI Backend**: From the project's **root directory**, run the following command:
    ```bash
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    Verify it's running, typically at `http://127.0.0.1:8000`.

## 2. Frontend Setup

1.  **Navigate to the project root**: (If you are not already there)
    ```bash
    cd /path/to/physical-ai-and-humanoid-robotics/
    ```
2.  **Install Node.js dependencies**: (If not already done)
    ```bash
    yarn
    ```
3.  **Configure Backend URL**: In a **new terminal window**, set the environment variable for the backend URL before starting Docusaurus.
    *   **For Windows PowerShell**:
        ```powershell
        $env:RAG_BACKEND_URL="http://localhost:8000"
        ```
    *   **For Linux/macOS Bash**:
        ```bash
        export RAG_BACKEND_URL="http://localhost:8000"
        ```
4.  **Start the Docusaurus Development Server** (in the same terminal where you set the environment variable):
    ```bash
    yarn start
    ```
    This will open the Docusaurus site in your browser, typically at `http://localhost:3000`.

## 3. Chatbot Interaction

1.  **Locate the Chatbot UI**: The chatbot component will be integrated into the Docusaurus site. Look for a floating button, a sidebar panel, or a dedicated page.
2.  **Ask a Question**:
    *   Type a question related to the book content into the chatbot's input field (e.g., "What are ROS 2 Nodes?").
    *   Submit the question.
    *   Observe the loading indicator and then the agent's grounded response.
3.  **Use Selected Text (Contextual Query)**:
    *   Navigate to a page in the Docusaurus book.
    *   Select a portion of text (e.g., a paragraph about URDF).
    *   Open the chatbot and type a question that refers to the selected text (e.g., "What is this used for?").
    *   Submit the question. The chatbot should automatically send the selected text to the backend.
    *   Verify the response is grounded in both your question and the selected text.
4.  **Observe Error Handling**:
    *   (Optional) Stop the FastAPI backend and try to ask a question. The chatbot UI should display an error message indicating connectivity issues.

By following these steps, you can interact with the RAG chatbot and experience the frontend-backend integration.
