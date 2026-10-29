"""
chat.py — Endpoints de chat com a IA Nini (MongoDB).
"""
from fastapi import APIRouter, HTTPException

from models import Conversation, ChatMessage
from schemas import (
    ChatMessageRequest, ChatMessageResponse,
    ConversationHistoryResponse, MessageResponse, SuccessResponse
)
from services import ai_service

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(body: ChatMessageRequest):
    """
    Processa uma mensagem do cliente e retorna a resposta da IA Nini.
    """
    conversation = await Conversation.find_one(Conversation.session_id == body.session_id)
    if not conversation:
        conversation = Conversation(session_id=body.session_id)
        await conversation.insert()

    # Histórico recente
    recent_messages = conversation.messages[-20:]
    history = [{"role": m.role, "content": m.content} for m in recent_messages]

    # Salva mensagem do usuário
    user_msg = ChatMessage(role="user", content=body.message)
    conversation.messages.append(user_msg)
    await conversation.save()

    # Processa com a IA
    try:
        ai_text, products = await ai_service.process_message(
            session_id=body.session_id,
            user_message=body.message,
            history=history,
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Serviço de IA temporariamente indisponível: {str(e)}"
        )

    # Salva resposta da IA
    ai_msg = ChatMessage(role="assistant", content=ai_text)
    conversation.messages.append(ai_msg)
    await conversation.save()

    return ChatMessageResponse(
        session_id=body.session_id,
        response=ai_text,
        products=products,
    )


@router.get("/history/{session_id}", response_model=ConversationHistoryResponse)
async def get_history(session_id: str):
    """Retorna o histórico de mensagens de uma sessão."""
    conversation = await Conversation.find_one(Conversation.session_id == session_id)
    if not conversation:
        return ConversationHistoryResponse(session_id=session_id, messages=[])

    messages = [
        MessageResponse(
            id=m.id,
            role=m.role,
            content=m.content,
            created_at=m.created_at,
        )
        for m in conversation.messages
    ]
    return ConversationHistoryResponse(session_id=session_id, messages=messages)


@router.delete("/session/{session_id}", response_model=SuccessResponse)
async def clear_session(session_id: str):
    """Apaga o histórico de uma conversa."""
    conversation = await Conversation.find_one(Conversation.session_id == session_id)
    if conversation:
        await conversation.delete()

    return SuccessResponse(message="Conversa encerrada com sucesso.")
