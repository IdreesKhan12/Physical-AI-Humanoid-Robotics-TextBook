import os
import httpx
from bs4 import BeautifulSoup
import cohere
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
import uuid
import time
import hashlib

load_dotenv()

# --- Configuration ---
SITEMAP_URL = "https://idreeskhan12.github.io/Physical-AI-Humanoid-Robotics-TextBook/sitemap.xml"
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = "physical_ai_textbook"
COHERE_EMBEDDING_MODEL = "embed-english-v3.0"

# --- Client Initialization ---
co = cohere.Client(COHERE_API_KEY)
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=60)

def get_all_urls(sitemap_url: str) -> list[str]:
    """Fetches and parses the sitemap.xml to extract all content URLs."""
    try:
        response = httpx.get(sitemap_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml-xml")
        urls = [loc.text for loc in soup.find_all("loc")]
        print(f"Found {len(urls)} URLs in sitemap.")
        return urls
    except Exception as e:
        print(f"Error parsing sitemap: {e}")
        return []

def extract_text_from_url(url: str) -> dict:
    """Fetches HTML, cleans it, and extracts the main text content and headings."""
    try:
        response = httpx.get(url, follow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        for unwanted_tag in soup(["nav", "header", "footer", "aside", "script", "style", "form"]):
            unwanted_tag.extract()

        page_title = soup.title.string if soup.title else "No Title Found"
        
        main_content = soup.find("main") or soup.find("article") or soup.body
        if not main_content:
            return {"text": "", "source": page_title}

        clean_text = main_content.get_text(separator=" ", strip=True)
        return {"text": clean_text, "source": page_title}
    except httpx.HTTPStatusError as e:
        print(f"HTTP error fetching {url}: {e}")
        return {"text": "", "source": "Unknown"}
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return {"text": "", "source": "Unknown"}

def chunk_text(text: str, chunk_size: int = 512, chunk_overlap: int = 50) -> list[str]:
    """Splits text into overlapping chunks."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + chunk_size]))
        i += chunk_size - chunk_overlap
    return chunks

def generate_deterministic_id(content_hash: str) -> str:
    """Generates a UUID for a text chunk based on its content's hash to ensure idempotency."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, content_hash))

def embed_chunks(chunks: list[str], cohere_client) -> list[list[float]]:
    """Generates embeddings for a list of text chunks using the Cohere client."""
    if not chunks:
        return []
    
    try:
        response = cohere_client.embed(
            texts=chunks,
            model=COHERE_EMBEDDING_MODEL,
            input_type="search_document"
        )
        return response.embeddings
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []

def create_and_store_vectors(chunks_data: list[dict], collection_name: str, qdrant_client):
    """Creates the Qdrant collection if it doesn't exist, then upserts the vectors."""
    try:
        qdrant_client.get_collection(collection_name=collection_name)
        print(f"Collection '{collection_name}' already exists.")
    except Exception:
        print(f"Collection '{collection_name}' not found, creating it.")
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
        )
    
    points = []
    for i, item in enumerate(chunks_data):
        points.append(
            models.PointStruct(
                id=generate_deterministic_id(item["chunk_text"]),
                vector=item["embedding"],
                payload={
                    "URL": item["URL"],
                    "heading": item["heading"],
                    "chunk_text": item["chunk_text"],
                    "chunk_index": i,
                },
            )
        )
    
    qdrant_client.upsert(
        collection_name=collection_name,
        wait=True,
        points=points,
    )
    print(f"Upserted {len(points)} vectors into collection '{collection_name}'.")

def main():
    """Main function to orchestrate the ingestion pipeline."""
    start_time = time.time()
    
    urls = get_all_urls(SITEMAP_URL)
    if not urls:
        print("No URLs found. Exiting.")
        return

    all_chunks_with_metadata = []
    
    for url in urls:
        print(f"Processing {url}...")
        content = extract_text_from_url(url)
        if content["text"]:
            chunks = chunk_text(content["text"])
            for i, chunk in enumerate(chunks):
                all_chunks_with_metadata.append({
                    "chunk_text": chunk,
                    "URL": url,
                    "heading": content["source"],
                    "chunk_index": i,
                })

    if not all_chunks_with_metadata:
        print("No chunks were created. Exiting.")
        return

    print(f"Generated {len(all_chunks_with_metadata)} total document chunks.")

    # Embed all chunks in batches
    batch_size = 96  # Cohere's API is efficient with batching
    for i in range(0, len(all_chunks_with_metadata), batch_size):
        batch = all_chunks_with_metadata[i:i + batch_size]
        batch_texts = [item["chunk_text"] for item in batch]
        
        embedding_start_time = time.time()
        embeddings = embed_chunks(batch_texts, co)
        embedding_end_time = time.time() 
        print(f"Embedded batch {i//batch_size + 1}/{(len(all_chunks_with_metadata) + batch_size - 1)//batch_size} in {embedding_end_time - embedding_start_time:.2f} seconds.")

        if embeddings:
            for j, item in enumerate(batch):
                item["embedding"] = embeddings[j]
        else:
            print(f"Skipping batch {i//batch_size + 1} due to embedding error.")
            for j, item in enumerate(batch):
                item["embedding"] = None

    # Filter out items that failed to get an embedding
    chunks_to_store = [item for item in all_chunks_with_metadata if item.get("embedding")]

    if chunks_to_store:
        upload_start_time = time.time()
        create_and_store_vectors(chunks_to_store, QDRANT_COLLECTION_NAME, qdrant_client)
        upload_end_time = time.time()
        print(f"Qdrant upload took {upload_end_time - upload_start_time:.2f} seconds.")

    end_time = time.time()
    print(f"\nIngestion pipeline completed in {end_time - start_time:.2f} seconds.")
    print(f"Total URLs processed: {len(urls)}")
    print(f"Total chunks created: {len(all_chunks_with_metadata)}")
    print(f"Total vectors uploaded: {len(chunks_to_store)}")

if __name__ == "__main__":
    main()

