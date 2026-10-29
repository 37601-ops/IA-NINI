"""
budget_service.py — Serviço de cálculo de orçamento para MongoDB.
Todos os valores monetários são processados no backend com Decimal
para garantir precisão financeira.
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional
from datetime import datetime

from models import BudgetSession, BudgetItem, Product
from schemas import BudgetResponse, BudgetItemResponse, ProductCard
from services.product_service import get_product_by_id

# ─── Regras comerciais ───────────────────────────────────────────────────────
DESCONTO_PERCENTUAL = Decimal("0.10")        # 10% de desconto
MINIMO_PARA_DESCONTO = Decimal("500.00")     # Mínimo para ganhar desconto
FRETE_GRATIS_ACIMA = Decimal("299.00")       # Frete grátis acima desse valor
FRETE_FIXO = Decimal("25.00")               # Frete fixo quando não é grátis


def _arredondar(valor: Decimal) -> Decimal:
    """Arredonda um valor monetário para 2 casas decimais."""
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


async def _get_or_create_budget(session_id: str) -> BudgetSession:
    """Recupera ou cria uma sessão de orçamento no MongoDB."""
    budget = await BudgetSession.find_one(BudgetSession.session_id == session_id)
    if not budget:
        budget = BudgetSession(session_id=session_id)
        await budget.insert()
    return budget


def _recalculate(budget: BudgetSession) -> None:
    """
    Recalcula subtotais, desconto, frete e total final do orçamento.
    """
    subtotal = _arredondar(sum(item.subtotal for item in budget.items))

    # Desconto: 10% quando subtotal >= R$ 500
    if subtotal >= MINIMO_PARA_DESCONTO:
        desconto = _arredondar(subtotal * DESCONTO_PERCENTUAL)
        budget.discount_total = desconto
    else:
        budget.discount_total = Decimal("0.00")

    # Frete: grátis acima de R$ 299 (após desconto)
    valor_com_desconto = _arredondar(subtotal - budget.discount_total)
    if valor_com_desconto >= FRETE_GRATIS_ACIMA:
        budget.shipping = Decimal("0.00")
    else:
        budget.shipping = FRETE_FIXO

    budget.subtotal = subtotal
    budget.grand_total = _arredondar(valor_com_desconto + budget.shipping)
    budget.is_estimate = True
    budget.updated_at = datetime.utcnow()


async def add_item(
    session_id: str, product_id: str, quantity: int
) -> BudgetResponse:
    """
    Adiciona um produto ao orçamento no MongoDB.
    Valida estoque e usa o preço real do catálogo.
    """
    product = await get_product_by_id(product_id)
    if not product or not product.is_active:
        raise ValueError("Produto não encontrado ou indisponível.")

    if product.stock_quantity < quantity:
        raise ValueError(
            f"Estoque insuficiente. Disponível: {product.stock_quantity} unidade(s)."
        )

    budget = await _get_or_create_budget(session_id)

    # Verifica se já está no orçamento
    existing_item = next((item for item in budget.items if item.product_id == str(product.id)), None)

    if existing_item:
        new_qty = existing_item.quantity + quantity
        if product.stock_quantity < new_qty:
            raise ValueError(
                f"Estoque insuficiente para {new_qty} unidade(s). "
                f"Disponível: {product.stock_quantity}."
            )
        existing_item.quantity = new_qty
        existing_item.unit_price = product.price
        existing_item.subtotal = _arredondar(product.price * Decimal(new_qty))
    else:
        item = BudgetItem(
            product_id=str(product.id),
            quantity=quantity,
            unit_price=product.price,
            subtotal=_arredondar(product.price * Decimal(quantity)),
        )
        budget.items.append(item)

    _recalculate(budget)
    await budget.save()
    return await get_budget(session_id)


async def update_item(
    session_id: str, item_id: str, quantity: int
) -> BudgetResponse:
    """Atualiza a quantidade de um item no orçamento."""
    if quantity < 1:
        raise ValueError("A quantidade mínima é 1.")

    budget = await _get_or_create_budget(session_id)
    item = next((i for i in budget.items if i.id == item_id), None)
    if not item:
        raise ValueError("Item não encontrado no orçamento.")

    product = await get_product_by_id(item.product_id)
    if product and product.stock_quantity < quantity:
        raise ValueError(
            f"Estoque insuficiente. Disponível: {product.stock_quantity} unidade(s)."
        )

    real_price = product.price if product else item.unit_price
    item.quantity = quantity
    item.unit_price = real_price
    item.subtotal = _arredondar(real_price * Decimal(quantity))

    _recalculate(budget)
    await budget.save()
    return await get_budget(session_id)


async def remove_item(
    session_id: str, item_id: str
) -> BudgetResponse:
    """Remove um item do orçamento."""
    budget = await _get_or_create_budget(session_id)
    initial_len = len(budget.items)
    budget.items = [i for i in budget.items if i.id != item_id]

    if len(budget.items) == initial_len:
        raise ValueError("Item não encontrado no orçamento.")

    _recalculate(budget)
    await budget.save()
    return await get_budget(session_id)


async def clear_budget(session_id: str) -> None:
    """Remove todos os itens do orçamento."""
    budget = await BudgetSession.find_one(BudgetSession.session_id == session_id)
    if budget:
        budget.items = []
        _recalculate(budget)
        await budget.save()


async def get_budget(session_id: str) -> BudgetResponse:
    """Retorna o orçamento completo com itens e dados do produto."""
    budget = await BudgetSession.find_one(BudgetSession.session_id == session_id)

    if not budget:
        return BudgetResponse(
            session_id=session_id,
            items=[],
            subtotal=Decimal("0.00"),
            discount_total=Decimal("0.00"),
            shipping=Decimal("0.00"),
            grand_total=Decimal("0.00"),
            is_estimate=True,
        )

    items_response = []
    for item in budget.items:
        prod = await get_product_by_id(item.product_id)
        prod_card = ProductCard.from_doc(prod) if prod else None
        items_response.append(
            BudgetItemResponse(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=item.subtotal,
                product=prod_card,
            )
        )

    discount_info = None
    if budget.subtotal >= MINIMO_PARA_DESCONTO:
        discount_info = f"Desconto de 10% aplicado para compras acima de R$ {MINIMO_PARA_DESCONTO:.2f}"

    shipping_info = (
        "Frete grátis!" if budget.shipping == Decimal("0.00")
        else f"Frete estimado de R$ {budget.shipping:.2f} (pode variar conforme o CEP)"
    )

    return BudgetResponse(
        session_id=session_id,
        items=items_response,
        subtotal=budget.subtotal,
        discount_total=budget.discount_total,
        shipping=budget.shipping,
        grand_total=budget.grand_total,
        is_estimate=budget.is_estimate,
        discount_info=discount_info,
        shipping_info=shipping_info,
    )
