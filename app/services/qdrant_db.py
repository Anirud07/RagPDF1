from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from app.config import QDRANT_HOST, QDRANT_PORT, COLLECTION_NAME, QDRANT_API_KEY

if QDRANT_API_KEY:
    client = QdrantClient(url=QDRANT_HOST, api_key=QDRANT_API_KEY)
else:
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


# ✅ Create collection if not exists
def create_collection_if_not_exists(vector_size=1536):
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )


def upsert_points(points):
    create_collection_if_not_exists()  # 🔥 important

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


# ✅ FIXED SEARCH (NEW API)
def search(query_vector, limit=5):
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    )

    return results.points