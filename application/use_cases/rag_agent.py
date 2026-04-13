from domain.interfaces.interfaces import VectorDatabasePort, LLMServicePort, TextEmbedderPort
from domain.entities import AgentResponse

class AnswerWithRAGUseCase:
    def __init__(
        self, 
        embedder: TextEmbedderPort,   
        vector_db: VectorDatabasePort,
        llm_service: LLMServicePort
    ):
        self.embedder = embedder
        self.vector_db = vector_db
        self.llm_service = llm_service

    def execute(self, user_question: str) -> AgentResponse:
        
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