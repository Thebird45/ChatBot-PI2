// ─── Configuración ────────────────────────────────────────────────────────────
const API_URL = "http://localhost:8000/api";
const USER_ID = "user_" + Math.random().toString(36).substr(2, 9);

// ─── Estado del chat ──────────────────────────────────────────────────────────
let isOpen = false;
let isTyping = false;

// ─── Timestamp ────────────────────────────────────────────────────────────────
function getTimestamp() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, "0");
    const minutes = now.getMinutes().toString().padStart(2, "0");
    return `${hours}:${minutes}`;
}

// ─── Crear widget en el DOM ───────────────────────────────────────────────────
function createWidget() {
    const widget = document.createElement("div");
    widget.innerHTML = `
        <!-- Botón flotante -->
        <div id="chat-toggle" onclick="toggleChat()">
            <img src="https://cdn-icons-png.flaticon.com/512/4711/4711987.png" 
                 alt="Chat" width="30" height="30"/>
        </div>

        <!-- Ventana del chat -->
        <div id="chat-window">
            <!-- Header -->
            <div id="chat-header">
                <div id="chat-header-info">
                    <div id="chat-avatar">N</div>
                    <div>
                        <div id="chat-title">NexusBot</div>
                        <div id="chat-status">En línea</div>
                    </div>
                </div>
                <div id="chat-header-actions">
                    <button onclick="clearHistory()" title="Limpiar historial">🗑️</button>
                    <button onclick="toggleChat()" title="Cerrar">✕</button>
                </div>
            </div>

            <!-- Mensajes -->
            <div id="chat-messages">
                <div class="message bot-message">
                    <div class="message-content">
                        👋 ¡Hola! Soy <strong>NexusBot</strong>, tu asistente en THE NEXUS BATTLES V.
                        ¿En qué puedo ayudarte hoy?
                    </div>
                    <div class="message-timestamp">${getTimestamp()}</div>
                </div>
            </div>

            <!-- Sugerencias -->
            <div id="chat-suggestions">
                <button onclick="sendSuggestion('¿Cómo funciona el combate?')">⚔️ Combate</button>
                <button onclick="sendSuggestion('¿Cuáles son los héroes?')">🦸 Héroes</button>
                <button onclick="sendSuggestion('¿Cómo me registro?')">📝 Registro</button>
            </div>

            <!-- Input -->
            <div id="chat-input-area">
                <input 
                    type="text" 
                    id="chat-input" 
                    placeholder="Escribe tu mensaje..."
                    onkeypress="handleKeyPress(event)"
                    maxlength="500"
                />
                <button id="send-btn" onclick="sendMessage()">➤</button>
            </div>
        </div>
    `;
    document.body.appendChild(widget);
}

// ─── Abrir / cerrar chat ──────────────────────────────────────────────────────
function toggleChat() {
    isOpen = !isOpen;
    const chatWindow = document.getElementById("chat-window");
    const toggle = document.getElementById("chat-toggle");
    chatWindow.style.display = isOpen ? "flex" : "none";
    toggle.style.display = isOpen ? "none" : "flex";

    // Al abrir, scroll al último mensaje
    if (isOpen) scrollToBottom();
}

// ─── Auto-scroll al fondo ─────────────────────────────────────────────────────
function scrollToBottom() {
    const messagesDiv = document.getElementById("chat-messages");
    messagesDiv.scrollTo({
        top: messagesDiv.scrollHeight,
        behavior: "smooth"
    });
}

// ─── Mostrar mensaje en pantalla ──────────────────────────────────────────────
function appendMessage(content, sender = "bot") {
    const messagesDiv = document.getElementById("chat-messages");
    const msg = document.createElement("div");
    msg.classList.add("message", sender === "user" ? "user-message" : "bot-message");
    msg.innerHTML = `
        <div class="message-content">${content}</div>
        <div class="message-timestamp">${getTimestamp()}</div>
    `;
    messagesDiv.appendChild(msg);
    scrollToBottom();
}

// ─── Indicador "escribiendo..." ───────────────────────────────────────────────
function showTyping() {
    const messagesDiv = document.getElementById("chat-messages");
    const typing = document.createElement("div");
    typing.id = "typing-indicator";
    typing.classList.add("message", "bot-message");
    typing.innerHTML = `
        <div class="message-content">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
        </div>
    `;
    messagesDiv.appendChild(typing);
    scrollToBottom();
}

function hideTyping() {
    const typing = document.getElementById("typing-indicator");
    if (typing) typing.remove();
}

// ─── Actualizar sugerencias ───────────────────────────────────────────────────
function updateSuggestions(suggestions) {
    const container = document.getElementById("chat-suggestions");
    container.innerHTML = "";
    suggestions.forEach(s => {
        const btn = document.createElement("button");
        btn.textContent = s;
        btn.onclick = () => sendSuggestion(s);
        container.appendChild(btn);
    });
}

// ─── Enviar mensaje ───────────────────────────────────────────────────────────
async function sendMessage() {
    const input = document.getElementById("chat-input");
    const message = input.value.trim();
    if (!message || isTyping) return;

    input.value = "";
    isTyping = true;

    appendMessage(message, "user");
    showTyping();

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: USER_ID, message })
        });

        const data = await response.json();
        hideTyping();

        if (response.status === 429) {
            appendMessage("⚠️ Has enviado demasiados mensajes. Espera un momento.", "bot");
        } else {
            appendMessage(data.response, "bot");
            if (data.suggestions?.length) {
                updateSuggestions(data.suggestions);
            }
        }

    } catch (error) {
        hideTyping();
        appendMessage("❌ No se pudo conectar con el servidor. Verifica tu conexión.", "bot");
    }

    isTyping = false;
}

// ─── Enviar sugerencia ────────────────────────────────────────────────────────
function sendSuggestion(text) {
    document.getElementById("chat-input").value = text;
    sendMessage();
}

// ─── Enter para enviar ────────────────────────────────────────────────────────
function handleKeyPress(event) {
    if (event.key === "Enter") sendMessage();
}

// ─── Limpiar historial ────────────────────────────────────────────────────────
async function clearHistory() {
    try {
        await fetch(`${API_URL}/chat/${USER_ID}`, { method: "DELETE" });
    } catch (e) {}

    const messagesDiv = document.getElementById("chat-messages");
    messagesDiv.innerHTML = `
        <div class="message bot-message">
            <div class="message-content">🗑️ Historial limpiado. ¿En qué puedo ayudarte?</div>
            <div class="message-timestamp">${getTimestamp()}</div>
        </div>
    `;
}

// ─── Inicializar ──────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", createWidget);