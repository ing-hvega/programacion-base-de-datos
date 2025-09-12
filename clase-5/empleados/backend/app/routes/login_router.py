from fastapi import APIRouter
from app.controllers.login_controller import LoginController
from app.schemas.user_schema import LoginRequest, TokenResponse

router = APIRouter()
login_controller = LoginController()

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """
    Autenticar usuario y generar token JWT
    """
    return await login_controller.login(login_data)
