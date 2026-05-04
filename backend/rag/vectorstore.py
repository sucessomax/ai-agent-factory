import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

PERSIST_DIR = "./data/vectorstore"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""]
)


def get_vectorstore():
    """Get or create vector store."""
    if os.path.exists(PERSIST_DIR):
        return Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embeddings
        )
    return None


def create_vectorstore(docs: List[str] = None):
    """Create new vector store with documents."""
    if docs is None:
        docs = [
            "O DevFactory é um framework de orquestração multi-agente.",
            "GSD significa Get Shit Done - metodologia de execução atômica.",
            "Context Rot é a degradação de contexto em conversas longas com LLMs.",
            "Workers efêmeros são subagentes com memória isolada.",
            "RAG combina recuperação de documentos com geração de texto.",
            "MCP é o Model Context Protocol para conectar LLMs a ferramentas.",
            "LangGraph permite criar arquiteturas multiagentes.",
            "A Pós-Graduação em Engenharia de IA Aplicada cobre: Agentes, MCP, RAG, MLOps."
        ]
    
    documents = [Document(page_content=doc) for doc in docs]
    texts = text_splitter.split_documents(documents)
    
    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )
    
    return vectorstore


def similarity_search(query: str, k: int = 3) -> List[str]:
    """Search in vector store."""
    vectorstore = get_vectorstore()
    
    if not vectorstore:
        vectorstore = create_vectorstore()
    
    docs = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]


def add_documents(docs: List[str]):
    """Add new documents to vector store."""
    vectorstore = get_vectorstore()
    
    if not vectorstore:
        return create_vectorstore(docs)
    
    documents = [Document(page_content=doc) for doc in docs]
    texts = text_splitter.split_documents(documents)
    
    vectorstore.add_documents(texts)
    vectorstore.persist()
    
    return vectorstore