
from abc import ABC, abstractmethod
from typing import List
from entities import RetrievedContext, AgentResponse

class VectorDatabasePort(ABC):
    @abstractmethod
    def search_similar(self, query_text: str, top_k: int = 3) -> List[RetrievedContext]:
        pass

class LLMServicePort(ABC):
    @abstractmethod
    def generate_grounded_response(self, question: str, context: List[RetrievedContext]) -> str:
        pass


class TextEmbedderPort(ABC):
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass

class VectorDatabasePort(ABC):
    @abstractmethod
    def search_by_vector(self, query_vector: List[float], top_k: int = 3) -> List[RetrievedContext]:
        pass