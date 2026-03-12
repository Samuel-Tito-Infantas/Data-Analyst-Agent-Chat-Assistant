from langchain_core.documents import Document
from AgenticChat.vector_database_providers.chroma_database import VectorDatabaseProvider

class FewShotRetrieverAWS:
    def __init__(self, VectorDatabaseProvider):
        self.vectorstore = VectorDatabaseProvider()
        
    def add_example(self, question: str, sql: str):
        doc = Document(
            page_content=question,
            metadata={"sql": sql}
        )
        self.vectorstore.add_documents([doc])
        
    def get_similar_examples(self, question: str, k=2) -> str:
        # Busca exemplos semelhantes
        docs = self.vectorstore.similarity_search(question, k=k)
        
        exemplos_formatados = ""
        for i, doc in enumerate(docs):
            exemplos_formatados += f"Exemplo {i+1}:\nPergunta: {doc.page_content}\nSQL: {doc.metadata['sql']}\n\n"
        return exemplos_formatados