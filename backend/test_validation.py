import os
import pytest
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import cohere
from collections import defaultdict
import time

# --- Global Test Constants ---
QDRANT_COLLECTION_NAME = "physical_ai_textbook"
COHERE_EMBEDDING_MODEL = "embed-english-v3.0"
QDRANT_VECTOR_SIZE = 1024

# --- Pytest Fixtures ---

@pytest.fixture(scope="module")
def qdrant_client() -> QdrantClient:
    """Initializes and returns a Qdrant client."""
    load_dotenv()
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    assert QDRANT_URL and QDRANT_API_KEY, "Qdrant environment variables must be set."
    # Explicitly disable local embedding models to prevent fastembed/onnxruntime loading
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=False, force_disable_fastembed=True)
    return client

@pytest.fixture(scope="module")
def cohere_client() -> cohere.Client:
    """Initializes and returns a Cohere client."""
    load_dotenv()
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    assert COHERE_API_KEY, "COHERE_API_KEY must be set."
    client = cohere.Client(COHERE_API_KEY)
    return client

# --- Diagnostic Tests ---

@pytest.mark.diagnostic
def test_collection_schema(qdrant_client: QdrantClient):
    """Verifies the Qdrant collection exists and has the correct schema."""
    try:
        collection_info = qdrant_client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
        assert collection_info is not None, f"Collection '{QDRANT_COLLECTION_NAME}' does not exist."
        
        # Access vector parameters correctly (it's within 'params' for the default vector type)
        vector_config = collection_info.config.params.vectors
        assert vector_config.size == QDRANT_VECTOR_SIZE, f"Expected vector size {QDRANT_VECTOR_SIZE}, but found {vector_config.size}."
        assert str(vector_config.distance).upper() == 'COSINE', f"Expected distance metric COSINE, but found {vector_config.distance}."

    except Exception as e:
        pytest.fail(f"Failed to get collection info from Qdrant: {e}")

@pytest.mark.diagnostic
def test_metadata_completeness(qdrant_client: QdrantClient):
    """Checks a sample of points for metadata completeness."""
    missing_metadata_points = []
    required_fields = ["URL", "heading", "chunk_text", "chunk_index"]
    sample_points, _ = qdrant_client.scroll(
        collection_name=QDRANT_COLLECTION_NAME, limit=100, with_payload=True
    )
    for point in sample_points:
        if not all(field in point.payload for field in required_fields):
            missing_metadata_points.append(point.id)
    assert not missing_metadata_points, f"Found points with missing metadata: {missing_metadata_points}"

@pytest.mark.diagnostic
def test_no_empty_vectors(qdrant_client: QdrantClient):
    """Checks a sample of vectors to ensure they are not empty."""
    empty_vector_points = []
    sample_points, _ = qdrant_client.scroll(
        collection_name=QDRANT_COLLECTION_NAME, limit=50, with_vectors=True
    )
    for point in sample_points:
        if not point.vector:
            empty_vector_points.append(point.id)
    assert not empty_vector_points, f"Found points with empty vectors: {empty_vector_points}"

@pytest.mark.diagnostic
def test_duplicate_chunks(qdrant_client: QdrantClient):
    """Checks for duplicate chunks of text in a sample of points."""
    text_to_ids = defaultdict(list)
    sample_points, _ = qdrant_client.scroll(
        collection_name=QDRANT_COLLECTION_NAME, limit=200, with_payload=True
    )
    for point in sample_points:
        text_to_ids[point.payload.get("chunk_text")].append(point.id)
    duplicates = {text: ids for text, ids in text_to_ids.items() if len(ids) > 1 and text}
    assert not duplicates, f"Found duplicate chunks: {duplicates}"

# --- Retrieval Tests ---

TEST_QUERIES = [
    {"query": "What is a URDF?", "keywords": ["Unified Robot Description Format", "link", "joint"], "top_k": 3},
    {"query": "How does bipedal locomotion work?", "keywords": ["Zero Moment Point", "ZMP", "balance"], "top_k": 3},
    {"query": "What is Isaac Sim?", "keywords": ["Omniverse", "RTX GPU", "Synthetic Data Generation"], "top_k": 3},
]

@pytest.mark.retrieval
@pytest.mark.parametrize("test_query", TEST_QUERIES)
def test_general_question_retrieval(qdrant_client: QdrantClient, cohere_client: cohere.Client, test_query):
    """Tests retrieval for a set of predefined queries."""
    query_embedding = cohere_client.embed(
        texts=[test_query["query"]], model=COHERE_EMBEDDING_MODEL, input_type="search_query"
    ).embeddings[0]
    
    start_time = time.time()
    search_results = qdrant_client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=query_embedding,
        limit=test_query["top_k"],
        with_payload=True,
    )
    end_time = time.time()
    print(f"Retrieval for '{test_query['query']}' took {end_time - start_time:.2f} ms.")
    
    assert search_results, f"Query '{test_query['query']}' returned no results."
    
    found_keywords = any(
        keyword.lower() in hit.payload.get("chunk_text", "").lower()
        for hit in search_results
        for keyword in test_query["keywords"]
    )
    assert found_keywords, f"Query did not retrieve documents with expected keywords: {test_query['keywords']}"

@pytest.mark.retrieval
def test_metadata_filtering(qdrant_client: QdrantClient, cohere_client: cohere.Client):
    """Tests the ability to filter search results by metadata."""
    from qdrant_client.models import Filter, FieldCondition, MatchValue

    query_text = "What is a node?"
    chapter_filter = "Ros2 Core Concepts | physical-ai-and-humanoid-robotics"
    
    query_embedding = cohere_client.embed(
        texts=[query_text], model=COHERE_EMBEDDING_MODEL, input_type="search_query"
    ).embeddings[0]

    search_results = qdrant_client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=query_embedding,
        query_filter=Filter(must=[FieldCondition(key="heading", match=MatchValue(value=chapter_filter))]),
        limit=5,
        with_payload=True,
    )
    
    assert search_results, f"Filtered query returned no results."
    for hit in search_results:
        assert hit.payload.get("heading") == chapter_filter
