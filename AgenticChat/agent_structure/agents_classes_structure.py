from langchain_core.prompts import ChatPromptTemplate
from AgenticChat.models_providers.google_providers import configure_gemini_models

llm_raw_planner, llm_raw_linker = configure_gemini_models()

class PlannerAgent:
    def __init__(self, llm=llm_raw_planner):
        self.llm = llm

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um arquiteto de dados especialista em planejamento de consultas SQL.
            Sua tarefa: Decompor a pergunta do usuário em passos lógicos claros.
            
            Diretrizes:
            1. Identifique a intenção principal (agregação, comparação, join)
            2. Quebre em passos atômicos
            3. Defina métricas e fórmulas explicitamente
            4. NÃO escreva código SQL. Apenas o plano numerado.
            """),
            ("user", "{question}")
        ])

        self.chain = self.prompt | self.llm


    def plan(self, question:str)->dict:
        print("Planejador: Analisando a pergunta e criando um plano...")
        try:
            response =  self.chain.invoke({"question": question})
            plan = response.content
            return {"plan": plan, "status": "Sucess"}
        except Exception as e:
            print(f"Erro no planejamento: {e}")
            return {"erro": str(e), "status": "Error"}


class SchemaLinkerAgent:
    def __init__(self, llm=llm_raw_linker):
        self.llm = llm
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um DBA. Identifique quais tabelas são relevantes para a pergunta.
            Retorne APENAS uma lista separada por vírgulas com os nomes das tabelas. Sem explicações.
            Seja conservador: inclua a tabela apenas se for estritamente necessária baseada no plano.
            """),
            ("user", """
            Pergunta: {question}
            Plano Lógico: {plan}
            Tabelas Disponíveis no Banco: {all_tables}
            
            Tabelas necessárias:""")
        ])
        
        self.chain = self.prompt | self.llm


    def select_tables(self, question:str, plan:str, all_tables:list)->dict:
        print("SchemaLinker: Selecionando tabelas relevantes...")
        tables_str = self.chain.invoke({
                "question": question,
                "plan": plan,
                "all_tables": ", ".join(all_tables)
        })
        
        selected_tables = [t.strip() for t in tables_str.split(",") if t.strip() in all_tables]
        return selected_tables
    

