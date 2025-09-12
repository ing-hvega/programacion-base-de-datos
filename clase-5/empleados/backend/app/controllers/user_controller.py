import re
from passlib.context import CryptContext
from app.models.user_model import UserModel
from app.schemas.user_schema import UserCreate, PaginationParams

# Configuración para el hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserController:
    def __init__(self):
        self.user_model = UserModel()

    async def create_user(self, user_data: UserCreate):
        """
        Crea un nuevo usuario en la base de datos
        """
        try:
            # Generar hash de la contraseña
            hashed_password = self._get_password_hash(user_data.password)

            # Preparar datos del usuario
            user_dict = user_data.dict()
            user_dict["password"] = hashed_password

            # Crear usuario en la base de datos
            await self.user_model.create_user(user_dict)

            return {
                "message": "Usuario creado exitosamente",
                "status": True
            }
        except Exception as e:
            return {
                "message": "Error al crear usuario",
                "error": str(e),
                "status": False
            }

    async def get_users(self, params: PaginationParams):
        """
        Obtiene la lista de usuarios con paginación y búsqueda
        """
        try:
            # Calcular el índice de inicio para la paginación
            skip_index = (params.page - 1) * params.page_size

            # Preparar filtro de búsqueda
            filter_query = {}
            if params.search:
                # Crear expresión regular para la búsqueda
                search_regex = re.compile(params.search, re.IGNORECASE)
                filter_query = {
                    "$or": [
                        {"name": {"$regex": search_regex}},
                        {"email": {"$regex": search_regex}}
                    ]
                }

            # Obtener usuarios y total
            users = await self.user_model.find_users(filter_query, skip_index, params.page_size)
            total = await self.user_model.count_documents(filter_query)

            # Convertir ObjectId a string para serialización JSON
            for user in users:
                user["_id"] = str(user["_id"])

            return {
                "message": "Usuarios obtenidos exitosamente",
                "status": True,
                "data": users,
                "pagination": {
                    "page": params.page,
                    "page_size": params.page_size,
                    "total": total,
                    "total_pages": (total + params.page_size - 1) // params.page_size
                }
            }
        except Exception as e:
            return {
                "message": "Error al obtener usuarios",
                "error": str(e),
                "status": False
            }

    def _get_password_hash(self, password: str) -> str:
        """
        Genera un hash de la contraseña
        """
        return pwd_context.hash(password)
