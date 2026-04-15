from fastapi import APIRouter, UploadFile, File
from app.utils.pdf import extract_text
from app.services.rag import chunk_text, store_chunks

router = APIRouter()

@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()

    text = extract_text(content)
    chunks = chunk_text(text)

    store_chunks(chunks)

    return {"message": "PDF uploaded & processed"}