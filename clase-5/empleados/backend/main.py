from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.config.database import connect_to_mongo
from app.routes.user_router import router as user_router
from app.routes.login_router import router as login_router

# Cargar variables de entorno
load_dotenv()

# Crear aplicación FastAPI
app = FastAPI(title="API Usuarios", description="API para gestión de usuarios")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar a MongoDB
connect_to_mongo()

# Rutas
@app.get("/")
async def root():
    return {"message": "ok!"}

app.include_router(user_router, prefix="/api", tags=["usuarios"])
app.include_router(login_router, prefix="/api", tags=["autenticación"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
