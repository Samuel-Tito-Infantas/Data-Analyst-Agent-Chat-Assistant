from domain.interfaces.interfaces import LLMServicePort
from domain.entities import RetrievedContext
from typing import List

class BedrockClaudeAdapter(LLMServicePort):
    def __init__(self):
        pass

    def generate_grounded_response(self, question: str, context: List[RetrievedContext]) -> str:
        context_str = "\n".join([doc.text for doc in context])
        prompt = f"Use APENAS o contexto abaixo para responder:\nContexto:\n{context_str}\n\nPergunta: {question}"
        
        # Simulação de chamada de API
        return "Com base no contexto, DDD separa a regra de negócio da infraestrutura."
    