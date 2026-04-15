from app.services.embedding import embed_documents, embed_query
from app.services.qdrant_db import upsert_points, search
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


# ✅ Simple chunking
def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def store_chunks(chunks):
    vectors = embed_documents(chunks)

    points = [
        {
            "id": i,
            "vector": vectors[i],
            "payload": {"text": chunks[i]}
        }
        for i in range(len(chunks))
    ]

    upsert_points(points)


# ✅ FIXED retrieval
def retrieve_context(query):
    query_vector = embed_query(query)
    results = search(query_vector)

    return [point.payload["text"] for point in results]


def generate_answer(query, context_chunks):
    context = "\n".join(context_chunks)

    prompt = f"""
Answer ONLY from the context below.

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content