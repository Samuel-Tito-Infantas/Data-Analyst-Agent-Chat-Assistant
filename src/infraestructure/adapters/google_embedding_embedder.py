# infraestructure/adapters/google_embedding_embedder.py
from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.application.ports.output import TextEmbedderRepo # <-- Fix import

class GoogleGeminiEmbedder(TextEmbedderRepo): # <-- Inherit correct Port
    def __init__(self):
        self.model_name = "models/embedding-001"
        self.model = GoogleGenerativeAIEmbeddings(model=self.model_name)

    def embed_text(self, text: str) -> List[float]: 
        try:
            return self.model.embed_query(text)
        except Exception as e:
            print(f"Error in {self.__class__.__name__}: {e}")
            return []