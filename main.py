import os
import json
import pickle
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import messages_from_dict, messages_to_dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY não está definido no arquivo .env")

# FastAPI app
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminhos
INDEX_DIR = "faiss_index"
HISTORY_DIR = "history"

# Carrega o vetor FAISS salvo
def load_vectorstore():
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    if os.path.exists(INDEX_DIR):
        return FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
    else:
        raise RuntimeError("Base vetorial não encontrada. Execute rag.py para criar 'faiss_index'.")

vectorstore = load_vectorstore()

# Utilitários para histórico
def load_chat_history(session_id: str):
    path = os.path.join(HISTORY_DIR, f"{session_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            messages_dict = json.load(f)
            return messages_from_dict(messages_dict)
    return []

def save_chat_history(session_id: str, messages):
    os.makedirs(HISTORY_DIR, exist_ok=True)
    path = os.path.join(HISTORY_DIR, f"{session_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages_to_dict(messages), f, indent=2, ensure_ascii=False)

# Endpoint de pergunta
@app.post("/ask")
async def ask(request: Request):
    try:
        body = await request.json()
        question = body.get("question")
        session_id = body.get("session_id")

        if not question or not session_id:
            raise HTTPException(status_code=400, detail="Parâmetros 'question' e 'session_id' são obrigatórios.")

        # Histórico
        chat_history = load_chat_history(session_id)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        memory.chat_memory.messages = chat_history

        # LLM + RAG
        llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory,
            return_source_documents=False,
        )

        # Faz a pergunta
        result = qa_chain.invoke({"question": question})

        # Salva novo histórico
        save_chat_history(session_id, memory.chat_memory.messages)

        return {"response": result["answer"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")
