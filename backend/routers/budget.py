"""
budget.py — Endpoints da calculadora de orçamento (MongoDB).
"""
from fastapi import APIRouter, HTTPException

from schemas import BudgetResponse, AddItemRequest, UpdateItemRequest, SuccessResponse
from services import budget_service

router = APIRouter(prefix="/budget", tags=["Orçamento"])


@router.get("/{session_id}", response_model=BudgetResponse)
async def get_budget(session_id: str):
    """Retorna o orçamento atual da sessão."""
    return await budget_service.get_budget(session_id)


@router.post("/{session_id}/add", response_model=BudgetResponse)
async def add_item(session_id: str, body: AddItemRequest):
    """
    Adiciona um produto ao orçamento.
    O preço é obtido diretamente do MongoDB — nunca do cliente.
    """
    try:
        return await budget_service.add_item(
            session_id, body.product_id, body.quantity
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{session_id}/item/{item_id}", response_model=BudgetResponse)
async def update_item(session_id: str, item_id: str, body: UpdateItemRequest):
    """Atualiza a quantidade de um item no orçamento."""
    try:
        return await budget_service.update_item(
            session_id, item_id, body.quantity
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{session_id}/item/{item_id}", response_model=BudgetResponse)
async def remove_item(session_id: str, item_id: str):
    """Remove um item do orçamento."""
    try:
        return await budget_service.remove_item(session_id, item_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{session_id}", response_model=SuccessResponse)
async def clear_budget(session_id: str):
    """Limpa todos os itens do orçamento."""
    await budget_service.clear_budget(session_id)
    return SuccessResponse(message="Orçamento limpo com sucesso.")


@router.post("/{session_id}/calculate", response_model=BudgetResponse)
async def recalculate(session_id: str):
    """Força o recálculo do orçamento no servidor."""
    return await budget_service.get_budget(session_id)
