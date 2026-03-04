import os
import json
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

# ─── Base de conocimiento ───────────────────────────────────────────────────
def load_knowledge_base():
    try:
        with open("knowledge_base/data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

knowledge = load_knowledge_base()

# ─── Intenciones del chatbot ─────────────────────────────────────────────────
INTENTS = {
    "heroes":    ["héroe", "hero", "guerrero", "mago", "pícaro", "sanador", "tanque", "poder", "vida", "defensa", "ataque", "daño"],
    "items":     ["arma", "armadura", "ítem", "item", "carta", "mazo", "equipo"],
    "mecanicas": ["combate", "turno", "misión", "misiones", "reglas", "modalidad", "jugar", "como se juega"],
    "cuenta":    ["registro", "cuenta", "contraseña", "perfil", "login", "acceso"],
    "subasta":   ["subasta", "comprar", "vender", "comercio", "precio", "mercado"],
    "soporte":   ["error", "problema", "bug", "falla", "no funciona", "ayuda técnica"],
    "faq":       ["qué es", "para qué", "cómo funciona", "explicame", "cuéntame"],
}

# ─── Sugerencias por intención ───────────────────────────────────────────────
SUGGESTIONS = {
    "heroes":    ["¿Cuáles son los tipos de héroes?", "¿Qué estadísticas tiene el Guerrero Tanque?", "¿Cómo funciona el poder de los héroes?"],
    "items":     ["¿Qué armas están disponibles?", "¿Cómo funcionan las armaduras?", "¿Qué son las habilidades épicas?"],
    "mecanicas": ["¿Cómo funciona el sistema de combate?", "¿Qué son las misiones?", "¿Cuáles son las modalidades de juego?"],
    "cuenta":    ["¿Cómo me registro?", "¿Cómo recupero mi contraseña?", "¿Cómo edito mi perfil?"],
    "subasta":   ["¿Cómo funciona la subasta?", "¿Cómo vendo un ítem?", "¿Cómo compro en el mercado?"],
    "soporte":   ["¿Cuáles son los requisitos del sistema?", "¿Cómo reporto un error?", "¿Cómo contacto soporte humano?"],
    "faq":       ["¿Qué es Nexus Battles V?", "¿Cómo empiezo a jugar?", "¿Es gratis el juego?"],
}

# ─── Reconocimiento de intención ─────────────────────────────────────────────
def detect_intent(message: str) -> str:
    message_lower = message.lower()
    for intent, keywords in INTENTS.items():
        if any(keyword in message_lower for keyword in keywords):
            return intent
    return "general"

# ─── Filtro de contenido inapropiado ─────────────────────────────────────────
FORBIDDEN_WORDS = [
    "insulto", "idiota", "estúpido", "maldito", "imbécil",
    "hack", "cheat", "trampa", "exploit", "vulnerabilidad"
]

def is_inappropriate(message: str) -> bool:
    message_lower = message.lower()
    return any(word in message_lower for word in FORBIDDEN_WORDS)

# ─── Prompt del sistema ───────────────────────────────────────────────────────
def build_system_prompt() -> str:
    return f"""Eres NexusBot, el asistente oficial del juego THE NEXUS BATTLES V.
Tu función es ayudar a los usuarios con información precisa y amigable sobre:
- Héroes, armas, armaduras e ítems del juego
- Reglas y mecánicas de combate por turnos
- Sistema de misiones, subastas y comercio
- Registro y gestión de cuenta
- Soporte técnico básico
- Preguntas frecuentes

Reglas de comportamiento:
- Responde siempre en el mismo idioma del usuario (español o inglés)
- Sé claro, conciso y amigable
- Si no sabes algo, dilo honestamente y sugiere contactar soporte humano
- Nunca inventes información que no esté en la base de conocimiento
- No respondas preguntas que no estén relacionadas con el juego

Base de conocimiento del juego:
{json.dumps(knowledge, ensure_ascii=False, indent=2)}
"""

# ─── Función principal de respuesta ──────────────────────────────────────────
async def get_response(user_message: str, history: list) -> dict:

    # Filtro de contenido inapropiado
    if is_inappropriate(user_message):
        return {
            "response": "Por favor mantén un lenguaje respetuoso. Estoy aquí para ayudarte con cualquier duda sobre Nexus Battles V. 😊",
            "intent": "filtrado",
            "suggestions": ["¿Cómo funciona el juego?", "¿Cuáles son los héroes disponibles?", "¿Necesitas ayuda técnica?"]
        }

    # Detectar intención
    intent = detect_intent(user_message)

    # Sugerencias según intención
    suggestions = SUGGESTIONS.get(intent, [
        "¿Cómo funciona el combate?",
        "¿Cuáles son los héroes disponibles?",
        "¿Necesitas ayuda con tu cuenta?"
    ])

    # Construir historial para Groq
    messages = [{"role": "system", "content": build_system_prompt()}]
    for msg in history[:-1]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    messages.append({"role": "user", "content": user_message})

    try:
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )

        bot_reply = response.choices[0].message.content

        return {
            "response": bot_reply,
            "intent": intent,
            "suggestions": suggestions
        }

    except Exception as e:
        return {
            "response": f"Lo siento, ocurrió un error al procesar tu consulta. Por favor intenta de nuevo. Error: {str(e)}",
            "intent": "error",
            "suggestions": ["¿Necesitas ayuda técnica?", "¿Cómo contacto soporte?"]
        }