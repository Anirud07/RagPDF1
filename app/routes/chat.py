from fastapi import APIRouter
from app.services.rag import retrieve_context, generate_answer

router = APIRouter()

@router.post("/")
async def chat(query: str):
    context = retrieve_context(query)
    answer = generate_answer(query, context)

    return {"answer": answer, "citations": context}