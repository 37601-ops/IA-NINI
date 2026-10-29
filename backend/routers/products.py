"""
products.py — Endpoints do catálogo de produtos (MongoDB).
"""
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from schemas import ProductCard
from services.product_service import (
    search_products, get_product_by_id, get_categories, get_brands
)

router = APIRouter(prefix="/products", tags=["Produtos"])


@router.get("/search", response_model=List[ProductCard])
async def search(
    q: Optional[str] = Query(None, description="Texto de busca"),
    category: Optional[str] = Query(None),
    min_price: Optional[Decimal] = Query(None, ge=0),
    max_price: Optional[Decimal] = Query(None, ge=0),
    brand: Optional[str] = Query(None),
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
):
    """Busca produtos no catálogo do MongoDB."""
    return await search_products(
        q=q,
        category=category,
        min_price=min_price,
        max_price=max_price,
        brand=brand,
        limit=limit,
        offset=offset,
    )


@router.get("/categories", response_model=List[str])
async def list_categories():
    """Retorna todas as categorias disponíveis."""
    return await get_categories()


@router.get("/brands", response_model=List[str])
async def list_brands():
    """Retorna todas as marcas disponíveis."""
    return await get_brands()


@router.get("/{product_id}", response_model=ProductCard)
async def get_product(product_id: str):
    """Retorna um produto específico pelo ID do MongoDB."""
    product = await get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return ProductCard.from_doc(product)
