import os
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.models.user_model import UserModel
from app.schemas.user_schema import LoginRequest

# Configuración para el hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginController:
    def __init__(self):
        self.user_model = UserModel()

    async def login(self, login_data: LoginRequest):
        """
        Autentica a un usuario y genera un token JWT
        """
        # Buscar usuario por email
        user = await self.user_model.find_by_email(login_data.email)

        if not user:
            return {
                "message": "Credenciales incorrectas",
                "status": False
            }

        # Verificar contraseña
        if not self._verify_password(login_data.password, user["password"]):
            return {
                "message": "Credenciales incorrectas",
                "status": False
            }

        # Generar token JWT
        token = self._create_token({
            "id": str(user["_id"]),
            "email": user["email"],
            "type": user["type"]
        })

        return {
            "message": "Login exitoso",
            "status": True,
            "token": token
        }

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si la contraseña coincide con el hash almacenado
        """
        return pwd_context.verify(plain_password, hashed_password)

    def _create_token(self, data: dict) -> str:
        """
        Crea un token JWT con los datos proporcionados
        """
        to_encode = data.copy()

        # Establecer tiempo de expiración (1 día)
        expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update({"exp": expire})

        # Crear token JWT
        encoded_jwt = jwt.encode(
            to_encode,
            os.getenv("JWT_SECRET", "your-secret-key"),
            algorithm="HS256"
        )

        return encoded_jwt
