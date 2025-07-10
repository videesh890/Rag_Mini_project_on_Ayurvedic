# rag_chain.py

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def load_vectorstore():
    # Use the same embedding model used in vector_store.py
    embedding = OpenAIEmbeddings(model="text-embedding-3-small")
    vectordb = Chroma(
        persist_directory="chroma_ayurvedic_db",
        embedding_function=embedding
    )
    return vectordb

def create_rag_chain():
    vectordb = load_vectorstore()

    # Customize retriever
    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 6}
    )

    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7  # Slightly lower for more factual answers
    )

    # Create RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )

    return qa_chain

def ask_medicine_bot(query: str) -> str:
    chain = create_rag_chain()
    try:
        result = chain({"query": query})
        answer = result["result"].strip()

        if answer.lower() in ["i don't know", "i am not sure"]:
            return "🤖 Sorry, I couldn't find a match. Try being more specific or rephrasing your question."

        return answer

    except Exception as e:
        return f"⚠️ Error during RAG processing: {str(e)}"
