"""
database.py — Conexão com o MongoDB via Motor + Beanie (ODM assíncrono).
Substitui completamente o SQLAlchemy do projeto anterior.
"""
import motor.motor_asyncio
from beanie import init_beanie
from config import settings


def get_motor_client() -> motor.motor_asyncio.AsyncIOMotorClient:
    """Cria e retorna o cliente Motor (driver async do MongoDB)."""
    return motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)


async def init_db(client: motor.motor_asyncio.AsyncIOMotorClient) -> None:
    """
    Inicializa o Beanie com todos os modelos de documento.
    Deve ser chamado uma única vez na inicialização da aplicação.
    """
    # Importação aqui para evitar circular imports
    from models import Product, Conversation, BudgetSession

    await init_beanie(
        database=client[settings.mongodb_db_name],
        document_models=[Product, Conversation, BudgetSession],
    )
