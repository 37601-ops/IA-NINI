"""
product_service.py — Serviço de busca e filtragem de produtos no MongoDB.
Utiliza Beanie Document para consultas assíncronas.
"""
from decimal import Decimal
from typing import List, Optional
import re
from bson import ObjectId

from models import Product
from schemas import ProductCard


async def search_products(
    q: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    brand: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    only_in_stock: bool = True,
) -> List[ProductCard]:
    """
    Busca produtos no MongoDB aplicando filtros.
    """
    query = {"is_active": True}

    if only_in_stock:
        query["stock_quantity"] = {"$gt": 0}

    if category and category.strip():
        query["category"] = {"$regex": f"^{re.escape(category.strip())}$", "$options": "i"}

    if brand and brand.strip():
        query["brand"] = {"$regex": f"^{re.escape(brand.strip())}$", "$options": "i"}

    price_query = {}
    if min_price is not None:
        price_query["$gte"] = min_price
    if max_price is not None:
        price_query["$lte"] = max_price
    if price_query:
        query["price"] = price_query

    if q and q.strip():
        termo_regex = {"$regex": re.escape(q.strip()), "$options": "i"}
        query["$or"] = [
            {"name": termo_regex},
            {"description": termo_regex},
            {"brand": termo_regex},
            {"category": termo_regex},
        ]

    products = (
        await Product.find(query)
        .sort(+Product.price)
        .skip(offset)
        .limit(limit)
        .to_list()
    )

    return [ProductCard.from_doc(p) for p in products]


async def get_product_by_id(product_id: str) -> Optional[Product]:
    """Retorna um produto pelo ID (ObjectId ou string) ou None se não encontrado."""
    try:
        if ObjectId.is_valid(product_id):
            return await Product.get(product_id)
        return await Product.find_one({"_id": product_id, "is_active": True})
    except Exception:
        return None


async def get_categories() -> List[str]:
    """Retorna a lista de categorias disponíveis no MongoDB."""
    collection = Product.get_motor_collection()
    cats = await collection.distinct("category", {"is_active": True})
    return sorted([str(c) for c in cats if c])


async def get_brands() -> List[str]:
    """Retorna a lista de marcas disponíveis no MongoDB."""
    collection = Product.get_motor_collection()
    brands = await collection.distinct("brand", {"is_active": True})
    return sorted([str(b) for b in brands if b])
