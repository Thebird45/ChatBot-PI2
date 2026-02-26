from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bot.responses import get_response
import time

router = APIRouter()

# Modelo del mensaje entrante
class Message(BaseModel):
    user_id: str
    message: str

# Historial de conversaciones por usuario
conversation_history = {}

# Control de tasa de consultas (max 10 mensajes por minuto por usuario)
rate_limit = {}
MAX_REQUESTS = 10
TIME_WINDOW = 60  # segundos

# ─── Rate limiting ────────────────────────────────────────────────────────────
def check_rate_limit(user_id: str) -> bool:
    now = time.time()

    if user_id not in rate_limit:
        rate_limit[user_id] = []

    # Limpiar requests fuera de la ventana de tiempo
    rate_limit[user_id] = [t for t in rate_limit[user_id] if now - t < TIME_WINDOW]

    if len(rate_limit[user_id]) >= MAX_REQUESTS:
        return False

    rate_limit[user_id].append(now)
    return True

# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/chat")
async def chat(data: Message):
    # Verificar rate limit
    if not check_rate_limit(data.user_id):
        raise HTTPException(
            status_code=429,
            detail="Has enviado demasiados mensajes. Espera un momento antes de continuar."
        )

    # Inicializar historial si es usuario nuevo
    if data.user_id not in conversation_history:
        conversation_history[data.user_id] = []

    # Agregar mensaje del usuario al historial
    conversation_history[data.user_id].append({
        "role": "user",
        "content": data.message
    })

    # Obtener respuesta del bot
    result = await get_response(data.message, conversation_history[data.user_id])

    # Agregar respuesta al historial
    conversation_history[data.user_id].append({
        "role": "assistant",
        "content": result["response"]
    })

    return {
        "user_id": data.user_id,
        "response": result["response"],
        "intent": result["intent"],
        "suggestions": result["suggestions"]
    }


@router.get("/chat/history/{user_id}")
async def get_history(user_id: str):
    if user_id not in conversation_history:
        raise HTTPException(status_code=404, detail="No se encontró historial para este usuario.")
    return {
        "user_id": user_id,
        "history": conversation_history[user_id]
    }


@router.delete("/chat/{user_id}")
async def clear_history(user_id: str):
    if user_id in conversation_history:
        conversation_history.pop(user_id)
    if user_id in rate_limit:
        rate_limit.pop(user_id)
    return {"message": "Historial eliminado correctamente"}


@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Chatbot API funcionando correctamente"}