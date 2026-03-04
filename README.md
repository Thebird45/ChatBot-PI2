# NexusBot — Módulo Chatbot
### THE NEXUS BATTLES V | Proyecto Integrador II — UPB 2026

Descripción
Módulo de chatbot inteligente para THE NEXUS BATTLES V.
Desarrollado con FastAPI (Python) + JavaScript + Groq AI.
Disponible como widget flotante en todas las vistas del sistema.

Stack tecnológico
- **Backend:** Python 3.13, FastAPI, Uvicorn
- **Frontend:** JavaScript, HTML, CSS
- **IA:** Groq API (llama-3.3-70b-versatile)
- **Contenedores:** Docker, Docker Compose

---

## Instalación y ejecución local

### Requisitos previos
- [Python 3.13+](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop) *(opcional)*
- [Git](https://git-scm.com/)

### Sin Docker

**1. Clonar el repositorio**
```bash
git clone https://github.com/TU_USUARIO/nexus-battles-chatbot.git
cd nexus-battles-chatbot
```

**2. Configurar variables de entorno**
```bash
cp backend/.env.example backend/.env
```
Edita `backend/.env` y agrega tu `GROQ_API_KEY`.

**3. Instalar dependencias**
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
pip install -r requirements.txt
```

**4. Levantar el servidor**
```bash
uvicorn main:app --reload
```

**5. Abrir el frontend**
Abre `frontend/index.html` con Live Server en VS Code.

### Con Docker
```bash
docker-compose up --build
```
- Frontend: http://localhost
- Backend API: http://localhost:8000
- Documentación API: http://localhost:8000/docs

---

## 📁 Estructura del proyecto
```
nexus-battles-chatbot/
├── backend/
│   ├── api/
│   │   └── routes.py           # Endpoints REST
│   ├── bot/
│   │   ├── responses.py        # Lógica del chatbot + IA
│   │   ├── intent.py           # Reconocimiento de intención (Sprint 2)
│   │   └── nlp.py              # Procesamiento de lenguaje (Sprint 2)
│   ├── knowledge_base/
│   │   └── data.json           # Base de conocimiento del juego
│   ├── websocket/
│   │   └── handler.py          # Comunicación en tiempo real (Sprint 2)
│   ├── main.py                 # Punto de entrada FastAPI
│   ├── requirements.txt        # Dependencias Python
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── chat-widget.js          # Lógica del widget
│   ├── chat-widget.css         # Estilos tema Nexus Battles
│   └── index.html              # Página de prueba
├── tests/
│   ├── test_bot.py
│   └── test_api.py
├── docs/
│   └── sprint-1/
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Variables de entorno
| Variable | Descripción |
|----------|-------------|
| `GROQ_API_KEY` | API Key de Groq (obligatoria) |
| `HOST` | Host del servidor (default: 0.0.0.0) |
| `PORT` | Puerto del servidor (default: 8000) |
| `ENVIRONMENT` | Entorno de ejecución (development/production) |

---

## Ramas
| Rama | Descripción |
|------|-------------|
| `main` | Código estable, entregables de sprint |
| `develop` | Integración del equipo |
| `feature/*` | Desarrollo de funcionalidades |

---

## 👥 Equipo
Módulo 6.4 — Chatbot  
Proyecto Integrador II — Ingeniería de Sistemas e Informática  
Universidad Pontificia Bolivariana — Seccional Bucaramanga 2026