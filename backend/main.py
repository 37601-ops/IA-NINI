"""
main.py — Ponto de entrada da aplicação NINI Store API (MongoDB).
FastAPI com CORS, Beanie ODM e inicialização do MongoDB.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from database import get_motor_client, init_db
from routers import chat, products, budget


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação e conexão com o MongoDB."""
    print("🚀 Conectando ao MongoDB...")
    client = get_motor_client()
    await init_db(client)
    print("✅ Conectado ao MongoDB e Beanie inicializado com sucesso!")
    yield
    print("👋 Fechando conexão com o MongoDB...")
    client.close()


app = FastAPI(
    title="NINI Store API",
    description="API da loja virtual com IA de atendimento integrada (MongoDB).",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(chat.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(budget.router, prefix="/api")


# ─── Handlers globais de erro ─────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Captura erros não tratados e retorna resposta amigável."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocorreu um erro interno. Por favor, tente novamente."},
    )


# ─── Health check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verifica se a API está funcionando."""
    return {"status": "ok", "message": "NINI Store API está no ar! 🛍️ (MongoDB)"}


@app.get("/", tags=["Sistema"])
async def root():
    return {
        "message": "Bem-vindo à NINI Store API!",
        "database": "MongoDB",
        "docs": "/docs",
        "health": "/health",
    }
