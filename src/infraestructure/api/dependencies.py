from src.infraestructure.adapters.redis_vector_db import RedisVectorAdapter
from src.infraestructure.adapters.google_flash3_planner import GoogleGeminiAdapter3Flash
from src.application.use_cases.rag_agent import AnswerWithRAGUseCase

def get_chat_use_case() -> AnswerWithRAGUseCase:
    vector_db = RedisVectorAdapter(index_name="reddit_index")
    llm_service = GoogleGeminiAdapter3Flash()

    llm_service.prepare_model_template()

    return AnswerWithRAGUseCase(vector_db=vector_db, llm_service=llm_service, embedder=vector_db)