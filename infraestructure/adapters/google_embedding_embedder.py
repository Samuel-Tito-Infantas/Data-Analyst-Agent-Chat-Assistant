from typing import List

from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from domain.interfaces.interfaces import LLMServicePort
from domain.entities import RetrievedContext

class GoogleGeminiEmbedder(LLMServicePort):
    def __init__(self):
        self.model_name= "gemini-embedding-001"

    def prepare_model_template(self):
        self.model = GoogleGenerativeAIEmbeddings(self.model_name)

    def convert_to_embedding(self, text: str) -> List[float]:
        try:
            embedding = self.model.embed_query(text)
            return embedding
        except Exception as e:
            print(f"Erro in {self.__class__.__name__}: {e}")
            return []
