from typing import List

from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from domain.interfaces.interfaces import LLMServicePort
from domain.entities import RetrievedContext

class GoogleGeminiAdapter3Flash(LLMServicePort):
    def __init__(self):
        self.system_prompt = """Você é um arquiteto de dados especialista em planejamento de consultas SQL.
            Sua tarefa: Decompor a pergunta do usuário em passos lógicos claros.
            
            Diretrizes:
            1. Identifique a intenção principal (agregação, comparação, join)
            2. Quebre em passos atômicos
            3. Defina métricas e fórmulas explicitamente
            4. NÃO escreva código SQL. Apenas o plano numerado.
            """
        self.model= "gemini-3-flash-preview", #"gemini-2.5-pro",
        self.temperature = 0.0
        self.max_tokens = 2048

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