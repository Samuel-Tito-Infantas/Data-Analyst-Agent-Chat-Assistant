from src.application.ports.output import VectorDatabaseRepo, LLMServiceRepo, TextEmbedderRepo
from src.domain.entities import AgentResponse
from src.application.ports.input import ChatUseCase

class AnswerWithRAGUseCase(ChatUseCase):
    def __init__(
        self, 
        embedder: TextEmbedderRepo,   
        vector_db: VectorDatabaseRepo,
        llm_service: LLMServiceRepo
    ):
        self.embedder = embedder
        self.vector_db = vector_db
        self.llm_service = llm_service

    def start_conversation(self, user_question: str) -> AgentResponse:
        
        question_vector = self.embedder.embed_text(user_question)
        
        context_docs = self.vector_db.search_by_vector(query_vector=question_vector, top_k=3)
        
        if not context_docs:
            return AgentResponse(
                question=user_question,
                answer="Sorry, I don't have enough information to answer that.",
                sources_used=[]
            )

        generated_answer = self.llm_service.generate_grounded_response(
            question=user_question, 
            context=context_docs
        )

        return AgentResponse(question=user_question, answer=generated_answer, sources_used=context_docs)