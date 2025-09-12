# Sistema de Gestión de Empleados - Backend

Este es el backend de un sistema de gestión de empleados desarrollado con FastAPI y Python. El sistema proporciona una API RESTful para manejar la autenticación y gestión de usuarios/empleados.

## Estructura del Proyecto

```
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
└── app/
    ├── config/            # Configuraciones (base de datos, etc.)
    ├── controllers/       # Lógica de negocio
    ├── middleware/        # Middlewares (autenticación)
    ├── models/           # Modelos de datos
    ├── routes/           # Rutas de la API
    └── schemas/          # Esquemas de validación (Pydantic)
```

## Características

- Autenticación mediante JWT
- CRUD completo de usuarios/empleados
- Paginación de resultados
- Búsqueda de usuarios
- Validación de datos mediante Pydantic
- Tipos de usuario/roles

## Modelos de Datos

### Usuario (User)
- Nombre
- Email
- Contraseña (hash)
- Tipo de usuario
- Descripción (opcional)

## Endpoints de la API

### Autenticación
- `POST /login` - Iniciar sesión y obtener token

### Usuarios
- `GET /users` - Listar usuarios (con paginación)
- `POST /users` - Crear nuevo usuario
- `GET /users/{id}` - Obtener usuario por ID
- `PUT /users/{id}` - Actualizar usuario
- `DELETE /users/{id}` - Eliminar usuario

## Requisitos del Sistema

- Python 3.11+
- FastAPI
- MongoDB
- Pydantic v2

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno (si es necesario)

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
uvicorn main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

## Documentación de la API

Una vez que el servidor esté corriendo, puedes acceder a:
- Documentación Swagger UI: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc`

## Seguridad

- Autenticación mediante JWT (JSON Web Tokens)
- Contraseñas hasheadas
- Middleware de autenticación para rutas protegidas
- Validación de datos con Pydantic

## Esquemas de Datos

### UserCreate
```python
{
    "name": "string",
    "email": "user@example.com",
    "password": "string",
    "type": "integer",
    "description": "string (opcional)"
}
```

### UserResponse
```python
{
    "id": "string",
    "name": "string",
    "email": "user@example.com",
    "type": "integer",
    "description": "string (opcional)"
}
```

## Estado de Respuestas

El API utiliza respuestas estandarizadas:
- 200: Operación exitosa
- 201: Recurso creado
- 400: Error de validación
- 401: No autorizado
- 404: Recurso no encontrado
- 500: Error interno del servidor

Las respuestas siguen el formato:
```json
{
    "message": "string",
    "status": boolean,
    "data": object (opcional)
}
```
