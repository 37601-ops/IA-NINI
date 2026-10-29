"""
schemas.py — Schemas Pydantic para validação de dados de entrada e saída (MongoDB).
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Union
from pydantic import BaseModel, Field, ConfigDict


# ─────────────────────────── PRODUTO ───────────────────────────

class ProductBase(BaseModel):
    name: str
    description: str
    category: str
    brand: str
    price: Decimal
    stock_quantity: int
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime

    @property
    def in_stock(self) -> bool:
        return self.stock_quantity > 0


class ProductCard(BaseModel):
    """Versão compacta do produto para exibir nos cards do chat."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str
    category: str
    brand: str
    price: Decimal
    stock_quantity: int
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    in_stock: bool = True

    @classmethod
    def from_doc(cls, p) -> "ProductCard":
        return cls(
            id=str(p.id),
            name=p.name,
            description=p.description,
            category=p.category,
            brand=p.brand,
            price=p.price,
            stock_quantity=p.stock_quantity,
            image_url=p.image_url,
            product_url=p.product_url,
            in_stock=p.stock_quantity > 0,
        )


class ProductSearchParams(BaseModel):
    q: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    brand: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=50)
    offset: int = Field(default=0, ge=0)


# ─────────────────────────── CHAT ───────────────────────────

class ChatMessageRequest(BaseModel):
    session_id: str = Field(..., min_length=36, max_length=36)
    message: str = Field(..., min_length=1, max_length=2000)


class ChatMessageResponse(BaseModel):
    session_id: str
    response: str
    products: List[ProductCard] = []
    budget_action: Optional[dict] = None


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    role: str
    content: str
    created_at: datetime


class ConversationHistoryResponse(BaseModel):
    session_id: str
    messages: List[MessageResponse]


# ─────────────────────────── ORÇAMENTO ───────────────────────────

class AddItemRequest(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1, le=999)


class UpdateItemRequest(BaseModel):
    quantity: int = Field(..., ge=1, le=999)


class BudgetItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_id: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    product: Optional[ProductCard] = None


class BudgetResponse(BaseModel):
    session_id: str
    items: List[BudgetItemResponse]
    subtotal: Decimal
    discount_total: Decimal
    shipping: Decimal
    grand_total: Decimal
    is_estimate: bool
    discount_info: Optional[str] = None
    shipping_info: Optional[str] = None


# ─────────────────────────── GENÉRICO ───────────────────────────

class ErrorResponse(BaseModel):
    detail: str


class SuccessResponse(BaseModel):
    message: str
