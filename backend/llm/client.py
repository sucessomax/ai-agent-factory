from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=MODEL_NAME,
    temperature=TEMPERATURE,
    streaming=True
)

def get_llm(temperature: float = TEMPERATURE):
    return ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=MODEL_NAME,
        temperature=temperature,
        streaming=True
    )