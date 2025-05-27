# 🤖 Agente LIO - Backend (FastAPI + LangChain + FAISS)

Este é o backend de um agente conversacional IA que responde perguntas técnicas sobre a **documentação da LIO Local da Cielo**, usando **RAG (Retrieval-Augmented Generation)** com FastAPI, LangChain, OpenAI e FAISS.

## ⚙️ Funcionalidades

- 🔍 Carrega e embeda a documentação da LIO Local.
- 💬 Mantém histórico de conversa por sessão.
- 🧠 Usa LangChain com memória para manter contexto.
- 🚀 API REST para comunicação com front-end Flutter Web.

## 🗂️ Estrutura do Projeto

```
agente-lio-backend/
├── documento_lio.txt          # Texto extraído da documentação da LIO Local
├── faiss_index/               # Base vetorial criada com FAISS
├── history/                   # Históricos de conversas por sessão
├── loader.py                  # Faz scrape da documentação e salva .txt
├── rag.py                     # Constrói base vetorial a partir do .txt
├── main.py                    # FastAPI com endpoint de pergunta
├── .env                       # Contém sua chave da OpenAI
├── requirements.txt           # Dependências do projeto
└── README.md                  # Este arquivo
```

## 🚀 Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/agente-lio-backend.git
cd agente-lio-backend
```

### 2. Crie e ative o ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
python -m ensurepip
python -m pip install -r requirements.txt
```

> Caso ainda não tenha, crie um arquivo `.env` com sua chave da OpenAI:

```
OPENAI_API_KEY=sua-chave-aqui
```

### 4. Baixe a documentação da LIO

```bash
python loader.py
```

### 5. Gere a base vetorial FAISS

```bash
python rag.py
```

### 6. Rode o servidor FastAPI

```bash
uvicorn main:app --reload
```

A API estará disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🧪 Testando a API

Você pode testar manualmente via `curl`, Postman ou com o front-end Flutter que acompanha este projeto.

### Exemplo de requisição:

```http
POST /ask
Content-Type: application/json

{
  "question": "Como iniciar uma transação na LIO?",
  "session_id": "abc123"
}
```

## 📁 Requisitos

- Python 3.9+
- Chave da OpenAI válida

## 📦 Dependências principais

- FastAPI
- LangChain
- FAISS
- OpenAI API
- BeautifulSoup
- Uvicorn

## 📝 Licença

Este projeto é apenas para fins educacionais e uso pessoal. Todos os direitos da documentação da LIO pertencem à Cielo.

## 👨‍💻 Autor

Pedro Henrique Ignacio Sobrinho  
Desenvolvedor Mobile II @ Braspag/Cielo
