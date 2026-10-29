"""
models.py — Modelos ODM para MongoDB via Beanie (substitui o SQLAlchemy).
Define as collections: products, conversations e budget_sessions.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
import uuid

from beanie import Document
from pydantic import BaseModel, Field


class Product(Document):
    """Documento da collection 'products' do MongoDB."""
    name: str
    description: str
    category: str
    brand: str
    price: Decimal
    stock_quantity: int = 0
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "products"
        indexes = [
            "category",
            "brand",
            "is_active",
            [("name", "text"), ("description", "text"), ("brand", "text"), ("category", "text")]
        ]


class ChatMessage(BaseModel):
    """Mensagem individual armazenada dentro do documento da conversa."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str  # "user" ou "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Conversation(Document):
    """Documento de sessão de conversa com a IA."""
    session_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    messages: List[ChatMessage] = Field(default_factory=list)

    class Settings:
        name = "conversations"
        indexes = ["session_id"]


class BudgetItem(BaseModel):
    """Item dentro de um orçamento."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    product_id: str
    quantity: int = 1
    unit_price: Decimal
    subtotal: Decimal
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BudgetSession(Document):
    """Documento de sessão de orçamento."""
    session_id: str
    subtotal: Decimal = Decimal("0.00")
    discount_total: Decimal = Decimal("0.00")
    shipping: Decimal = Decimal("0.00")
    grand_total: Decimal = Decimal("0.00")
    is_estimate: bool = True
    items: List[BudgetItem] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "budget_sessions"
        indexes = ["session_id"]
