from langchain_community.vectorstores import Chroma
from AgenticChat.models_providers.google_providers import GoogleGenerativeAIEmbeddings

class VectorDatabaseProvider:
    def __init__(self, embeddings_model=GoogleGenerativeAIEmbeddings):
        self.vectorstore = Chroma(embedding_function=embeddings_model)