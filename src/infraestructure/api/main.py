from fastapi import FastAPI, Depends
from src.application.use_cases.rag_agent import AnswerWithRAGUseCase
from src.infraestructure.adapters import get_chat_agent_use_case

app = FastAPI(title="Data Agent Chat Assistant API")

@app.post("/chat")
async def chat(message: str, use_case: AnswerWithRAGUseCase = Depends(get_chat_agent_use_case)):
    
    result = use_case.execute(message)
    return {"answer": result.answer, "sources": result.context_docs}

