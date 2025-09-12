import logging
from motor.motor_asyncio import AsyncIOMotorClient
import os

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("user_model")

class UserModel:
    def __init__(self):
        # Utilizamos motor.motor_asyncio para operaciones asíncronas
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/userdb")
        self.client = AsyncIOMotorClient(mongo_uri)
        db_name = os.getenv("MONGODB_DATABASE", "userdb")
        self.db = self.client[db_name]
        self.collection = self.db["users"]

    async def create_user(self, user_data: dict):
        """
        Crea un nuevo usuario en la base de datos
        """
        try:
            result = await self.collection.insert_one(user_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error al crear usuario: {str(e)}")
            raise

    async def find_by_email(self, email: str):
        """
        Busca un usuario por su email
        """
        try:
            return await self.collection.find_one({"email": email})
        except Exception as e:
            logger.error(f"Error al buscar usuario por email: {str(e)}")
            raise

    async def find_users(self, filter_query: dict, skip: int, limit: int):
        """
        Busca usuarios con filtros y paginación
        """
        try:
            cursor = self.collection.find(filter_query, {
                "name": 1,
                "email": 1,
                "type": 1,
                "description": 1
            }).skip(skip).limit(limit)

            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Error al buscar usuarios: {str(e)}")
            raise

    async def count_documents(self, filter_query: dict):
        """
        Cuenta el número de documentos que cumplen con el filtro
        """
        try:
            return await self.collection.count_documents(filter_query)
        except Exception as e:
            logger.error(f"Error al contar documentos: {str(e)}")
            raise
