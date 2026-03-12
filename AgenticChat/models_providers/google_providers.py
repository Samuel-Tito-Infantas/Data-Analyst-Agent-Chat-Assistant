
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv

load_dotenv()


def configure_gemini_models():
    llm_raw_planner = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        temperature=0.0,
        max_tokens=2048
    )

    llm_raw_linker = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.0,
        max_tokens=512 # O output dele é só uma lista de tabelas, não precisa de muitos tokens
    )

    return llm_raw_planner, llm_raw_linker



def configure_gemini_encoder():
    # 3. O "Tradutor Matemático" (Para Embeddings / Semantic Cache)
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"
    )
    return embeddings_model