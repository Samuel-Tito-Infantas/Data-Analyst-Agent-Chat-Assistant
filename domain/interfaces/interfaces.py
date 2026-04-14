
from abc import ABC, abstractmethod
from typing import List

import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from entities import RetrievedContext
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