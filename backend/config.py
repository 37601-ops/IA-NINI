"""
config.py — Configurações centrais da aplicação NINI Store (MongoDB).
Lê as variáveis de ambiente do arquivo .env via pydantic-settings.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # --- LLM (Groq) ---
    groq_api_key: str
    groq_model: str = "qwen/qwen3.8-27b"
    max_products_per_response: int = 6
    max_history_messages: int = 10

    # --- MongoDB ---
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "nini_store"

    # --- Segurança ---
    secret_key: str = "troque-por-uma-chave-segura-em-producao"

    # --- CORS ---
    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Retorna a lista de origens CORS permitidas."""
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Instância global de configurações
settings = Settings()
