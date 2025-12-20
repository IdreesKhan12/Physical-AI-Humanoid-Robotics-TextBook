# Quickstart: RAG Book Project — Spec 4: Agentic RAG Backend with FastAPI

This guide provides instructions on how to set up, run, and interact with the RAG Agent FastAPI backend.

## 1. Environment Setup

1.  **Ensure Python 3.11 and UV**: Make sure you have Python 3.11 installed and `uv` (a fast Python package installer and manager) is available in your environment.
2.  **Install Dependencies**: Navigate to the `backend/` directory and install the required Python packages.
    ```bash
    cd backend/
    uv pip install -r requirements.txt
    ```

## 2. Configuration

1.  **Environment Variables**: Create a `.env` file in the `backend/` directory and populate it with your API keys and Qdrant connection details.
    ```dotenv
    OPENAI_API_KEY="your_openai_api_key_here"
    COHERE_API_KEY="your_cohere_api_key_here"
    QDRANT_URL="your_qdrant_cloud_url_here"
    QDRANT_API_KEY="your_qdrant_api_key_here"
    # QDRANT_COLLECTION_NAME="physical_ai_textbook" # Default, can override
    ```
    *(Ensure your Qdrant collection is populated with data from Spec 1.)*

## 3. Running the FastAPI Application

1.  **Start the Uvicorn Server**: From the project root, run the FastAPI application using `uvicorn`.
    ```bash
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    This will start the API server, typically accessible at `http://127.0.0.1:8000`.

## 4. Testing Endpoints

Once the FastAPI server is running, you can interact with its endpoints.

### 4.1. Health Check (`GET /health`)

Check the health and connectivity status of the service.

```bash
curl -X GET "http://127.0.0.1:8000/health" -H "accept: application/json"
```

Expected response (example):
```json
{
  "status": "ok",
  "qdrant_status": "connected",
  "cohere_status": "connected",
  "openai_status": "connected",
  "timestamp": "2025-12-18T12:00:00Z"
}
```

### 4.2. Ask a Question (`POST /ask`)

Ask a question to the RAG Agent and get a grounded answer.

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d "{
  \"question\": \"What are the core concepts of ROS 2?\",
  \"selected_text\": null
}"
```

Expected response (example):
```json
{
  "answer": "The core concepts of ROS 2 include Nodes, Topics, Services, and Actions. Nodes are executable processes, Topics are named buses for message exchange (publish/subscribe), Services provide a request/reply mechanism, and Actions are for long-running, goal-oriented communication with feedback.",
  "citations": [
    {
      "url": "https://example.com/docs/module-1/ros2-core-concepts",
      "heading": "The Core Concepts of ROS 2",
      "chunk_text_snippet": "At the heart of ROS 2 are several key concepts that define how these \"workers\" (software components) interact. Nodes: The Workers, Topics: The Conveyor Belts, Services: The Request-Response System, Actions: The Long-Term Goals."
    }
  ],
  "metadata": {
    "retrieval_score": 0.85,
    "model_used": "gpt-4",
    "response_time_ms": 1200
  }
}
```

### 4.3. Debug Retrieval (`POST /debug/retrieval`)

Inspect the raw retrieved chunks for a given query.

```bash
curl -X POST "http://127.0.0.1:8000/debug/retrieval" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d "{
  \"question\": \"What is URDF?\"
}"
```

Expected response (example - truncated):
```json
{
  "query_embedding": [...],
  "retrieved_chunks": [
    {
      "url": "https://example.com/docs/module-1/launch-urdf",
      "heading": "Introduction to URDF: Describing Your Robot",
      "chunk_text": "The Unified Robot Description Format (URDF) is an XML format for describing all aspects of a robot. It's used to represent the robot's kinematic and dynamic properties, visual appearance, and collision geometry.",
      "chunk_index": 0,
      "score": 0.92
    },
    {
      "url": "https://example.com/docs/module-1/launch-urdf",
      "heading": "Links and Joints: The Building Blocks of a Robot",
      "chunk_text": "At its core, a URDF file defines a robot as a collection of links connected by joints.",
      "chunk_index": 1,
      "score": 0.88
    }
  ]
}
```
