from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Nexus Battles Chatbot API",
    description="Chatbot inteligente para THE NEXUS BATTLES V",
    version="1.0.0"
)

# Permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas del chatbot
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"status": "Chatbot API corriendo correctamente"}