from typing import List

from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from src.application.ports.output import LLMServiceRepo
from src.domain.entities import RetrievedContext

class GoogleGeminiAdapter25FlashLite(LLMServiceRepo):
    def __init__(self):
        self.system_prompt = """Você é um DBA. Identifique quais tabelas são relevantes para a pergunta.
            Retorne APENAS uma lista separada por vírgulas com os nomes das tabelas. Sem explicações.
            Seja conservador: inclua a tabela apenas se for estritamente necessária baseada no plano.
            """
        self.model= "gemini-2.5-flash-lite" #"gemini-2.5-pro",
        self.temperature = 0.0
        self.max_tokens = 512

    def prepare_model_template(self):
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("user", "{question}")
        ])
        
        llm_raw_planner = ChatGoogleGenerativeAI(
            model= self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        self.chain = chat_prompt | llm_raw_planner

    def generate_grounded_response(self, question: str, context: List[RetrievedContext]) -> str:
        try:
            context_str = "\n".join([doc.text for doc in context])
            response =  self.chain.invoke({"question": question, "context": context_str})
            plan = response.content
            return plan
        except Exception as e:
            print(f"Erro in {self.__class__.__name__}: {e}")
            return f"Erro: {str(e)}"