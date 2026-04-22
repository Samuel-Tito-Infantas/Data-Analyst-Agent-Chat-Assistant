from abc import ABC, abstractmethod
from typing import List

from domain.entities import RetrievedContext, AgentResponse, KnowledgeDocument


class VectorDatabaseRepo(ABC):
    @abstractmethod
    def add_text_database(self, texts:List[KnowledgeDocument]):
        pass

    @abstractmethod
    def search_by_vector(self, query_vector: List[float], top_k: int = 3) -> List[RetrievedContext]:
        pass

class TextEmbedderRepo(ABC):
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass

class LLMServiceRepo(ABC):
    @abstractmethod
    def generate_grounded_response(self, question: str, context: AgentResponse) -> str:
        pass

