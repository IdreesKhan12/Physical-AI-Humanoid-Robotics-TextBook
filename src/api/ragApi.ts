// src/api/ragApi.ts

interface QueryInput {
  question: string;
  selected_text?: string | null;
}

interface Citation {
  url: string;
  heading?: string | null;
  chunk_text_snippet: string;
}

interface AgentMetadata {
  retrieval_score: number;
  model_used: string;
  response_time_ms: number;
}

export interface AgentResponse {
  answer: string;
  citations: Citation[];
  metadata: AgentMetadata;
}

export interface RetrievedChunkPayload {
    url: string;
    heading?: string | null;
    chunk_text: string;
    chunk_index: number;
    score: number;
}

export interface RetrievalDebugResponse {
    query_embedding: number[];
    retrieved_chunks: RetrievedChunkPayload[];
}

export interface HealthStatus {
    status: string;
    qdrant_status: string;
    cohere_status: string;
    openai_status: string;
    timestamp: string;
}

// Function to get the backend URL from environment variables or Docusaurus config
const getBackendUrl = (): string => {
    // During local development, process.env.RAG_BACKEND_URL will be available if set.
    // For Docusaurus build, we might need to inject it differently or use a custom plugin.
    // For now, assume it's available or default to localhost.
    return process.env.RAG_BACKEND_URL || 'http://127.0.0.1:8002';
};

const BACKEND_URL = getBackendUrl();

export const askAgent = async (query: QueryInput): Promise<AgentResponse> => {
  const response = await fetch(`${BACKEND_URL}/ask`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(query),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `Backend error: ${response.status}`);
  }

  return response.json();
};

export const getHealthStatus = async (): Promise<HealthStatus> => {
    const response = await fetch(`${BACKEND_URL}/health`);

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Backend error: ${response.status}`);
    }

    return response.json();
};

export const debugRetrieval = async (question: string): Promise<RetrievalDebugResponse> => {
    const response = await fetch(`${BACKEND_URL}/debug/retrieval`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Backend error: ${response.status}`);
    }

    return response.json();
};
