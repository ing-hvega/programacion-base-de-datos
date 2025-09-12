from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union

# Esquema para la creación de usuarios
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    type: int
    description: Optional[str] = None

# Esquema para la respuesta de usuarios (sin password)
class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: EmailStr
    type: int
    description: Optional[str] = None

    class Config:
        # Actualizado para Pydantic v2
        populate_by_name = True
        from_attributes = True  # Reemplaza el antiguo orm_mode

# Esquema para la autenticación
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Esquema para la respuesta de token
class TokenResponse(BaseModel):
    message: str
    status: bool
    token: str

# Esquema para la paginación
class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)
    search: Optional[str] = None

# Esquema para la respuesta general
class GenericResponse(BaseModel):
    message: str
    status: bool
