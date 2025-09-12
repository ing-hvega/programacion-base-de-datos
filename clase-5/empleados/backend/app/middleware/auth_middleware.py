import os
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("auth_middleware")

security = HTTPBearer()

class AuthMiddleware:
    async def __call__(self, request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
        """
        Middleware para verificar el token JWT en las solicitudes
        """
        if not credentials:
            raise HTTPException(
                status_code=401,
                detail="No se proporcionó token de autenticación"
            )

        token = credentials.credentials

        if not token:
            raise HTTPException(
                status_code=401,
                detail="Formato de token inválido"
            )

        try:
            # Verificar el token
            payload = jwt.decode(
                token,
                os.getenv("JWT_SECRET", "your-secret-key"),
                algorithms=["HS256"]
            )

            # Guardar la información del usuario en el request state
            request.state.user = payload

            return payload
        except JWTError as e:
            logger.error(f"Error al validar token: {str(e)}")
            raise HTTPException(
                status_code=401,
                detail="Token inválido o expirado"
            )

# Instancia del middleware para ser usado como dependencia
auth_middleware = AuthMiddleware()
