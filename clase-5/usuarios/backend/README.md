# API Backend - Proyecto Usuarios

Este proyecto es una API REST desarrollada con Node.js, Express y TypeScript que proporciona endpoints para la gestión de usuarios, empleados y aviones, utilizando tanto MongoDB como MySQL como bases de datos.

## Tecnologías utilizadas

- **Node.js**: Entorno de ejecución para JavaScript
- **Express**: Framework web para Node.js
- **TypeScript**: Superset tipado de JavaScript
- **MongoDB**: Base de datos NoSQL
- **MySQL**: Base de datos relacional
- **TypeORM**: ORM para trabajar con bases de datos relacionales
- **Mongoose**: ODM para trabajar con MongoDB
- **JWT**: Autenticación basada en tokens
- **Bcrypt**: Encriptación de contraseñas
- **CORS**: Middleware para gestionar el acceso desde diferentes orígenes

## Estructura del proyecto

```
backend/
├── src/
│   ├── app.ts                   # Punto de entrada de la aplicación
│   ├── config/                  # Configuración de bases de datos y servicios
│   │   ├── database-mongo.config.ts
│   │   ├── database-mysql.config.ts
│   │   └── typeorm.config.ts
│   ├── controllers/             # Controladores de la aplicación
│   │   ├── mongodb/             # Controladores para MongoDB
│   │   │   ├── login.controller.ts
│   │   │   ├── planes.controller.ts
│   │   │   └── user.controller.ts
│   │   └── mysql/               # Controladores para MySQL
│   │       ├── auth.controller.ts
│   │       ├── empleado.controller.orm.ts
│   │       ├── empleado.controller.ts
│   │       └── user.controller.orm.ts
│   ├── dto/                     # Objetos de transferencia de datos
│   │   ├── empleado.model.ts
│   │   └── user.model.ts
│   ├── middleware/              # Middleware de la aplicación
│   │   └── auth.middleware.ts
│   ├── models/                  # Modelos de datos
│   │   ├── mongodb/             # Modelos para MongoDB
│   │   │   ├── plane.schema.ts
│   │   │   └── user.schema.ts
│   │   └── mysql/               # Modelos para MySQL
│   │       ├── empleado.entity.ts
│   │       ├── empleado.model.ts
│   │       ├── user.entity.ts
│   │       └── user.model.ts
│   └── routes/                  # Rutas de la API
│       ├── mongodb/             # Rutas para MongoDB
│       │   ├── login.router.ts
│       │   ├── plane.router.ts
│       │   └── user.router.ts
│       └── mysql/               # Rutas para MySQL
│           ├── auth.router.ts
│           ├── empleado.router.ts
│           └── user.router.orm.ts
├── scripts/                     # Scripts útiles
│   └── init-mysql-db.js
├── Dockerfile                   # Configuración para Docker
├── package.json                 # Dependencias y scripts
├── tsconfig.json                # Configuración de TypeScript
└── README.md                    # Este archivo
```

## Requisitos previos

- Node.js (v14 o superior)
- npm o pnpm
- MongoDB
- MySQL

## Instalación

1. Clone el repositorio
```bash
git clone <url-del-repositorio>
cd backend
```

2. Instale las dependencias
```bash
npm install
# o si usa pnpm
pnpm install
```

3. Configure las variables de entorno
Cree un archivo `.env` en la raíz del proyecto con la siguiente estructura:
```
PORT=3000
MONGO_URI=mongodb://localhost:27017/database
JWT_SECRET=your_jwt_secret_key

# Para MySQL
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=your_database

# Para TypeORM
TYPEORM_HOST=localhost
TYPEORM_USERNAME=root
TYPEORM_PASSWORD=your_password
TYPEORM_DATABASE=your_database
TYPEORM_PORT=3306
```

## Ejecución

### Desarrollo
```bash
npm run dev
# o
pnpm dev
```

### Producción
```bash
npm run build
npm start
# o
pnpm build
pnpm start
```

### Docker
```bash
docker build -t usuarios-backend .
docker run -p 3000:3000 usuarios-backend
```

## Endpoints de la API

### Rutas de MongoDB

#### Usuarios
- `POST /api/user`: Crear un nuevo usuario
  ```json
  // Request
  {
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan.perez@example.com",
    "password": "contraseña123",
    "role": "user"
  }
  
  // Response
  {
    "success": true,
    "message": "Usuario creado correctamente",
    "data": {
      "id": "60d21b4667d0d8992e610c85",
      "nombre": "Juan",
      "apellido": "Pérez",
      "email": "juan.perez@example.com",
      "role": "user",
      "createdAt": "2023-09-12T15:45:30.123Z"
    }
  }
  ```

- `GET /api/users`: Obtener la lista de usuarios
  ```json
  // Response
  {
    "success": true,
    "data": [
      {
        "id": "60d21b4667d0d8992e610c85",
        "nombre": "Juan",
        "apellido": "Pérez",
        "email": "juan.perez@example.com",
        "role": "user",
        "createdAt": "2023-09-12T15:45:30.123Z"
      },
      {
        "id": "60d21b4667d0d8992e610c86",
        "nombre": "María",
        "apellido": "González",
        "email": "maria.gonzalez@example.com",
        "role": "admin",
        "createdAt": "2023-09-12T16:30:20.456Z"
      }
    ]
  }
  ```

#### Autenticación
- `POST /api/login`: Autenticación de usuario
  ```json
  // Request
  {
    "email": "juan.perez@example.com",
    "password": "contraseña123"
  }
  
  // Response
  {
    "success": true,
    "message": "Inicio de sesión exitoso",
    "data": {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "user": {
        "id": "60d21b4667d0d8992e610c85",
        "nombre": "Juan",
        "apellido": "Pérez",
        "email": "juan.perez@example.com",
        "role": "user"
      }
    }
  }
  ```

#### Aviones
- `POST /api/plane`: Crear un nuevo avión
  ```json
  // Request
  {
    "modelo": "Boeing 737",
    "capacidad": 180,
    "aerolinea": "Aerolíneas Argentinas",
    "activo": true
  }
  
  // Response
  {
    "success": true,
    "message": "Avión creado correctamente",
    "data": {
      "id": "60d21b4667d0d8992e610c87",
      "modelo": "Boeing 737",
      "capacidad": 180,
      "aerolinea": "Aerolíneas Argentinas",
      "activo": true,
      "createdAt": "2023-09-12T17:20:10.789Z"
    }
  }
  ```

- `GET /api/planes`: Obtener la lista de aviones
  ```json
  // Response
  {
    "success": true,
    "data": [
      {
        "id": "60d21b4667d0d8992e610c87",
        "modelo": "Boeing 737",
        "capacidad": 180,
        "aerolinea": "Aerolíneas Argentinas",
        "activo": true,
        "createdAt": "2023-09-12T17:20:10.789Z"
      },
      {
        "id": "60d21b4667d0d8992e610c88",
        "modelo": "Airbus A320",
        "capacidad": 150,
        "aerolinea": "LATAM",
        "activo": true,
        "createdAt": "2023-09-12T17:25:45.123Z"
      }
    ]
  }
  ```

- `PUT /api/plane/:id`: Actualizar un avión específico
  ```json
  // Request - PUT /api/plane/60d21b4667d0d8992e610c87
  {
    "modelo": "Boeing 737-800",
    "capacidad": 189,
    "aerolinea": "Aerolíneas Argentinas",
    "activo": true
  }
  
  // Response
  {
    "success": true,
    "message": "Avión actualizado correctamente",
    "data": {
      "id": "60d21b4667d0d8992e610c87",
      "modelo": "Boeing 737-800",
      "capacidad": 189,
      "aerolinea": "Aerolíneas Argentinas",
      "activo": true,
      "updatedAt": "2023-09-12T18:10:05.456Z"
    }
  }
  ```

- `DELETE /api/plane/:id`: Eliminar un avión específico
  ```json
  // Request - DELETE /api/plane/60d21b4667d0d8992e610c88
  
  // Response
  {
    "success": true,
    "message": "Avión eliminado correctamente"
  }
  ```

- `GET /api/plane/:id`: Obtener un avión específico por ID
  ```json
  // Response - GET /api/plane/60d21b4667d0d8992e610c87
  {
    "success": true,
    "data": {
      "id": "60d21b4667d0d8992e610c87",
      "modelo": "Boeing 737-800",
      "capacidad": 189,
      "aerolinea": "Aerolíneas Argentinas",
      "activo": true,
      "createdAt": "2023-09-12T17:20:10.789Z",
      "updatedAt": "2023-09-12T18:10:05.456Z"
    }
  }
  ```

### Rutas de MySQL

#### Autenticación
- `POST /api/auth/login`: Autenticación con MySQL
  ```json
  // Request
  {
    "email": "usuario@example.com",
    "password": "contraseña123"
  }
  
  // Response
  {
    "success": true,
    "message": "Inicio de sesión exitoso",
    "data": {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "user": {
        "id": 1,
        "nombre": "Usuario",
        "apellido": "Demo",
        "email": "usuario@example.com",
        "role": "user"
      }
    }
  }
  ```

- `GET /api/auth/verify`: Verificar token (protegida)
  ```json
  // Request - Headers
  {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  
  // Response
  {
    "success": true,
    "message": "Token válido",
    "data": {
      "id": 1,
      "nombre": "Usuario",
      "apellido": "Demo",
      "email": "usuario@example.com",
      "role": "user"
    }
  }
  ```

#### Empleados
- `GET /api/empleado/:id`: Obtener empleado por ID (protegida)
  ```json
  // Request - Headers - GET /api/empleado/1
  {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  
  // Response
  {
    "success": true,
    "data": {
      "id": 1,
      "nombre": "Carlos",
      "apellido": "López",
      "email": "carlos.lopez@empresa.com",
      "departamento": "Tecnología",
      "cargo": "Desarrollador Senior",
      "salario": 5000,
      "fechaContratacion": "2022-01-15T00:00:00.000Z"
    }
  }
  ```

- `GET /api/empleados`: Obtener todos los empleados (protegida)
  ```json
  // Request - Headers
  {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  
  // Response
  {
    "success": true,
    "data": [
      {
        "id": 1,
        "nombre": "Carlos",
        "apellido": "López",
        "email": "carlos.lopez@empresa.com",
        "departamento": "Tecnología",
        "cargo": "Desarrollador Senior",
        "salario": 5000,
        "fechaContratacion": "2022-01-15T00:00:00.000Z"
      },
      {
        "id": 2,
        "nombre": "Ana",
        "apellido": "Martínez",
        "email": "ana.martinez@empresa.com",
        "departamento": "Marketing",
        "cargo": "Coordinadora",
        "salario": 4500,
        "fechaContratacion": "2022-03-10T00:00:00.000Z"
      }
    ],
    "total": 2,
    "page": 1,
    "limit": 10
  }
  ```

- `GET /api/empleados/departamentos`: Obtener departamentos (protegida)
  ```json
  // Request - Headers
  {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  
  // Response
  {
    "success": true,
    "data": [
      "Tecnología",
      "Marketing",
      "Recursos Humanos",
      "Finanzas",
      "Operaciones"
    ]
  }
  ```

- `GET /api/empleados/cargos`: Obtener cargos (protegida)
  ```json
  // Request - Headers
  {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  
  // Response
  {
    "success": true,
    "data": [
      "Desarrollador Senior",
      "Coordinadora",
      "Gerente",
      "Analista",
      "Director"
    ]
  }
  ```

- `POST /api/empleado`: Crear empleado (protegida)
  ```json
  // Request - Headers
  {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  
  // Request - Body
  {
    "nombre": "Luis",
    "apellido": "García",
    "email": "luis.garcia@empresa.com",
    "departamento": "Tecnología",
    "cargo": "Desarrollador Junior",
    "salario": 3000,
    "fechaContratacion": "2023-09-01"
  }
  
  // Response
  {
    "success": true,
    "message": "Empleado creado correctamente",
    "data": {
      "id": 3,
      "nombre": "Luis",
      "apellido": "García",
      "email": "luis.garcia@empresa.com",
      "departamento": "Tecnología",
      "cargo": "Desarrollador Junior",
      "salario": 3000,
      "fechaContratacion": "2023-09-01T00:00:00.000Z",
      "createdAt": "2023-09-12T19:30:15.789Z"
    }
  }
  ```

- `PUT /api/empleado/:id`: Actualizar empleado (protegida)
  ```json
  // Request - Headers - PUT /api/empleado/3
  {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  
  // Request - Body
  {
    "nombre": "Luis",
    "apellido": "García",
    "email": "luis.garcia@empresa.com",
    "departamento": "Tecnología",
    "cargo": "Desarrollador Semi-Senior",
    "salario": 3500,
    "fechaContratacion": "2023-09-01"
  }
  
  // Response
  {
    "success": true,
    "message": "Empleado actualizado correctamente",
    "data": {
      "id": 3,
      "nombre": "Luis",
      "apellido": "García",
      "email": "luis.garcia@empresa.com",
      "departamento": "Tecnología",
      "cargo": "Desarrollador Semi-Senior",
      "salario": 3500,
      "fechaContratacion": "2023-09-01T00:00:00.000Z",
      "updatedAt": "2023-09-12T20:15:30.456Z"
    }
  }
  ```

- `DELETE /api/empleado/:id`: Eliminar empleado (protegida)
  ```json
  // Request - Headers - DELETE /api/empleado/3
  {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  
  // Response
  {
    "success": true,
    "message": "Empleado eliminado correctamente"
  }
  ```

#### Usuarios (ORM)
- `POST /api/users/register`: Registrar un nuevo usuario (pública)
  ```json
  // Request
  {
    "nombre": "Roberto",
    "apellido": "Sánchez",
    "email": "roberto.sanchez@example.com",
    "password": "contraseña123",
    "role": "user"
  }
  
  // Response
  {
    "success": true,
    "message": "Usuario registrado correctamente",
    "data": {
      "id": 2,
      "nombre": "Roberto",
      "apellido": "Sánchez",
      "email": "roberto.sanchez@example.com",
      "role": "user",
      "createdAt": "2023-09-12T21:05:15.123Z"
    }
  }
  ```

- `GET /api/users`: Obtener todos los usuarios (protegida)
  ```json
  // Request - Headers
  {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  
  // Response
  {
    "success": true,
    "data": [
      {
        "id": 1,
        "nombre": "Usuario",
        "apellido": "Demo",
        "email": "usuario@example.com",
        "role": "admin",
        "createdAt": "2023-09-10T14:25:30.456Z"
      },
      {
        "id": 2,
        "nombre": "Roberto",
        "apellido": "Sánchez",
        "email": "roberto.sanchez@example.com",
        "role": "user",
        "createdAt": "2023-09-12T21:05:15.123Z"
      }
    ]
  }
  ```

- `GET /api/users/:id`: Obtener usuario por ID (protegida)
  ```json
  // Request - Headers - GET /api/users/2
  {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  
  // Response
  {
    "success": true,
    "data": {
      "id": 2,
      "nombre": "Roberto",
      "apellido": "Sánchez",
      "email": "roberto.sanchez@example.com",
      "role": "user",
      "createdAt": "2023-09-12T21:05:15.123Z",
      "updatedAt": "2023-09-12T21:05:15.123Z"
    }
  }
  ```

- `PUT /api/users/:id`: Actualizar usuario (protegida)
  ```json
  // Request - Headers - PUT /api/users/2
  {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  
  // Request - Body
  {
    "nombre": "Roberto",
    "apellido": "Sánchez González",
    "email": "roberto.sanchez@example.com",
    "role": "user"
  }
  
  // Response
  {
    "success": true,
    "message": "Usuario actualizado correctamente",
    "data": {
      "id": 2,
      "nombre": "Roberto",
      "apellido": "Sánchez González",
      "email": "roberto.sanchez@example.com",
      "role": "user",
      "updatedAt": "2023-09-12T21:30:45.789Z"
    }
  }
  ```

- `DELETE /api/users/:id`: Eliminar usuario (protegida)
  ```json
  // Request - Headers - DELETE /api/users/2
  {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  
  // Response
  {
    "success": true,
    "message": "Usuario eliminado correctamente"
  }
  ```

## Autenticación

La API utiliza autenticación basada en JWT (JSON Web Tokens). Para acceder a las rutas protegidas, es necesario incluir un token válido en el encabezado `Authorization` de la solicitud:

```
Authorization: Bearer <token>
```

El token se obtiene al autenticarse correctamente con los endpoints `/api/login` (MongoDB) o `/api/auth/login` (MySQL).

## Bases de datos

El proyecto está configurado para trabajar con dos bases de datos:

1. **MongoDB**: Para almacenar usuarios y aviones
2. **MySQL**: Para almacenar empleados y usuarios utilizando TypeORM

La conexión a ambas bases de datos se inicializa en el archivo `app.ts`.

## Scripts disponibles

- `npm run build`: Compila el código TypeScript a JavaScript
- `npm start`: Inicia la aplicación desde los archivos compilados
- `npm run dev`: Inicia la aplicación en modo desarrollo con recarga automática
- `npm run git`: Facilita el proceso de commit y push a Git

## Licencia

Este proyecto está licenciado bajo la licencia MIT.
