# 🛍️ NINI Store — IA de Atendimento para E-commerce (MongoDB)

Assistente virtual de vendas com IA generativa integrada ao catálogo de produtos.
A Nini conversa naturalmente com clientes, busca produtos reais no MongoDB e
oferece uma calculadora de orçamento interativa.

## Tecnologias utilizadas

| Camada | Tecnologia |
|---|---|
| LLM / IA | Groq API — LLaMA 3.1 70B |
| Backend | Python 3.10+ · FastAPI · Motor · Beanie (ODM) |
| Banco de dados | **MongoDB** (Local ou MongoDB Atlas gratuito) |
| Frontend | HTML · CSS · JavaScript (vanilla) |
| Validação | Pydantic v2 |

---

## Pré-requisitos

- Python **3.10 ou superior**
- **MongoDB** rodando localmente (`mongodb://localhost:27017`) **ou** uma conta no [MongoDB Atlas](https://www.mongodb.com/atlas/database) (gratuito)
- Conta gratuita no Groq: [console.groq.com](https://console.groq.com)

---

## Instalação passo a passo

### 1. Navegue até a pasta do backend

```bash
cd IA-NINI/backend
```

### 2. Crie e ative um ambiente virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo e preencha com os seus dados:

```bash
# Windows
copy ..\\.env.example .env

# Linux / macOS
cp ../.env.example .env
```

Edite o arquivo `.env`:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx   # sua chave Groq gratuita

# Conexão MongoDB local:
MONGODB_URL=mongodb://localhost:27017
# OU no MongoDB Atlas:
# MONGODB_URL=mongodb+srv://usuario:senha@cluster0.mongodb.net

MONGODB_DB_NAME=nini_store
SECRET_KEY=gere_uma_chave_secreta_aqui
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:5500
```

> **Como obter a chave Groq (gratuita):**
> 1. Acesse [console.groq.com](https://console.groq.com)
> 2. Crie uma conta gratuita
> 3. Clique em **API Keys → Create API Key**
> 4. Cole em `GROQ_API_KEY`

### 5. Popule o MongoDB com produtos de exemplo

```bash
python seed_data.py
```

Saída esperada:
```
✅ Conectado ao MongoDB e Beanie inicializado com sucesso!
✅ 20 produtos cadastrados com sucesso no MongoDB!

Categorias criadas:
  • Acessórios: 4 produto(s)
  • Informática: 6 produto(s)
  • Móveis para Escritório: 5 produto(s)
  • Smartphones: 5 produto(s)
```

### 6. Inicie o servidor backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Abra o frontend

Abra o arquivo `frontend/index.html` no navegador (ou com a extensão Live Server do VS Code).

---

## Endpoints da API

Documentação Swagger interativa: **[http://localhost:8000/docs](http://localhost:8000/docs)**

### Chat
| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/api/chat/message` | Envia mensagem, processa com IA e busca no MongoDB |
| GET | `/api/chat/history/{session_id}` | Histórico da conversa |
| DELETE | `/api/chat/session/{session_id}` | Apaga conversa |

### Produtos
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/api/products/search` | Busca com filtros (q, category, min_price, max_price, brand) |
| GET | `/api/products/{id}` | Produto por ID |
| GET | `/api/products/categories` | Lista categorias distintas |
| GET | `/api/products/brands` | Lista marcas distintas |

### Orçamento
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/api/budget/{session_id}` | Orçamento atual |
| POST | `/api/budget/{session_id}/add` | Adiciona produto real ao orçamento |
| PUT | `/api/budget/{session_id}/item/{item_id}` | Atualiza quantidade |
| DELETE | `/api/budget/{session_id}/item/{item_id}` | Remove item |
| DELETE | `/api/budget/{session_id}` | Limpa orçamento |
