from fastapi import APIRouter, Depends, Query
from app.controllers.user_controller import UserController
from app.schemas.user_schema import UserCreate, GenericResponse, UserResponse, PaginationParams
from app.middleware.auth_middleware import auth_middleware
from typing import List, Dict, Any

router = APIRouter()
user_controller = UserController()

@router.post("/user", response_model=GenericResponse)
async def create_user(user_data: UserCreate, user=Depends(auth_middleware)):
    """
    Crea un nuevo usuario (requiere autenticación)
    """
    return await user_controller.create_user(user_data)

@router.get("/users", response_model=Dict[str, Any])
async def get_users(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    search: str = Query(None, description="Término de búsqueda (nombre o email)"),
    user=Depends(auth_middleware)
):
    """
    Obtiene la lista de usuarios con paginación y búsqueda (requiere autenticación)
    """
    params = PaginationParams(page=page, page_size=page_size, search=search)
    return await user_controller.get_users(params)
