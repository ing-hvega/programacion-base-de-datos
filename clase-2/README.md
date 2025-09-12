# Sistema de Gestión Escolar con Bases de Datos

Este proyecto implementa un sistema de gestión escolar utilizando dos bases de datos diferentes (MySQL y MongoDB) con Docker para la containerización y scripts de Python para poblar las bases de datos con datos ficticios.

## Tecnologías utilizadas

- **Python 3.8+**: Lenguaje de programación principal
- **MySQL 8.0.23**: Base de datos relacional
- **MongoDB 8.0.12**: Base de datos NoSQL
- **Docker & Docker Compose**: Containerización y orquestación
- **Faker**: Generación de datos ficticios
- **pymongo**: Driver de Python para MongoDB
- **mysql-connector-python**: Driver de Python para MySQL

## Estructura del proyecto

```
clase-2/
├── .env                    # Variables de entorno (no incluido en git)
├── .env.example           # Ejemplo de variables de entorno
├── .gitignore            # Archivos ignorados por git
├── requirements.txt      # Dependencias de Python
├── README.md            # Este archivo
├── docker-compose.yml   # Configuración de Docker Compose
├── colegio.sql          # Script de creación de base de datos MySQL
├── faker_mongodb.py     # Script para poblar MongoDB
├── faker_mysql.py       # Script para poblar MySQL
├── mongodb/             # Configuración de MongoDB
│   ├── Dockerfile       # Imagen personalizada de MongoDB
│   └── createusers.sh   # Script de inicialización de usuarios
└── mysql/              # Configuración adicional de MySQL (si existe)
```

## Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.8 o superior**
- **Docker Desktop** (para Windows/Mac) o **Docker Engine** (para Linux)
- **Docker Compose** (incluido en Docker Desktop)
- **Git** (opcional, para clonar el repositorio)

### Verificar instalaciones

```bash
python --version
docker --version
docker-compose --version
```

## Instalación

### Paso 1: Clonar o descargar el proyecto

Si tienes acceso al repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd clase-2
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones (opcional, los valores por defecto funcionan)
```

## Configuración

### Variables de entorno (.env)

El archivo `.env` contiene las siguientes variables configurables:

```env
# MySQL variables
NAME_CONTAINER_MYSQL_DB=mysqldb      # Nombre del contenedor MySQL
DB_ROOT_PASSWORD_MYSQL=root          # Contraseña del usuario root
DB_PASSWORD_MYSQL=root               # Contraseña de la base de datos
FORWARD_MYSQL_PORT=3308              # Puerto expuesto para MySQL

# MongoDB variables
NAME_CONTAINER_MONGO_DB=mongodb      # Nombre del contenedor MongoDB
DB_USERNAME_MONGO=admin              # Usuario administrador de MongoDB
DB_PASSWORD_MONGO=admin              # Contraseña del administrador
DB_DATABASE_MONGO=main               # Nombre de la base de datos
FORWARD_MONGODB_PORT=27018           # Puerto expuesto para MongoDB
```

## Uso

### Iniciar los contenedores

```bash
# Construir e iniciar los contenedores
docker-compose up -d

# Verificar que los contenedores estén ejecutándose
docker-compose ps
```

### Crear la base de datos MySQL

```bash
# Ejecutar el script SQL en MySQL
docker exec -i mysqldb mysql -uroot -proot < colegio.sql
```

### Poblar las bases de datos

```bash
# Poblar MySQL con datos ficticios
python faker_mysql.py

# Poblar MongoDB con datos ficticios
python faker_mongodb.py
```

## Endpoints y Operaciones

Este proyecto implementa operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para gestionar entidades educativas en dos bases de datos diferentes. A continuación se detallan los endpoints y operaciones disponibles con sus estructuras de request:

### Endpoints MySQL

Las siguientes operaciones se ejecutan directamente a través de consultas SQL en la base de datos MySQL:

#### Operaciones de Estudiantes

- **Crear estudiante**: 
  ```
  Endpoint: POST /api/mysql/students
  Método: SQL INSERT
  Request:
  {
    "first_name": "string", // Nombre del estudiante
    "last_name": "string",  // Apellido del estudiante
    "birth_date": "date",   // Formato YYYY-MM-DD
    "email": "string"       // Correo electrónico único
  }
  Query SQL:
  INSERT INTO students (first_name, last_name, birth_date, email) 
  VALUES (?, ?, ?, ?)
  ```

- **Listar estudiantes**: 
  ```
  Endpoint: GET /api/mysql/students
  Método: SQL SELECT
  Request: No requiere parámetros
  Query SQL:
  SELECT * FROM students
  ```

- **Buscar estudiante por ID**: 
  ```
  Endpoint: GET /api/mysql/students/{id}
  Método: SQL SELECT
  Request:
  {
    "id": integer  // ID del estudiante
  }
  Query SQL:
  SELECT * FROM students WHERE id = ?
  ```

- **Buscar estudiante por email**: 
  ```
  Endpoint: GET /api/mysql/students/search?email={email}
  Método: SQL SELECT
  Request:
  {
    "email": "string"  // Correo del estudiante
  }
  Query SQL:
  SELECT * FROM students WHERE email = ?
  ```

#### Operaciones de Profesores

- **Crear profesor**: 
  ```
  Endpoint: POST /api/mysql/teachers
  Método: SQL INSERT
  Request:
  {
    "first_name": "string", // Nombre del profesor
    "last_name": "string",  // Apellido del profesor
    "email": "string"       // Correo electrónico único
  }
  Query SQL:
  INSERT INTO teachers (first_name, last_name, email) 
  VALUES (?, ?, ?)
  ```

- **Listar profesores**: 
  ```
  Endpoint: GET /api/mysql/teachers
  Método: SQL SELECT
  Request: No requiere parámetros
  Query SQL:
  SELECT * FROM teachers
  ```

- **Buscar profesor por ID**: 
  ```
  Endpoint: GET /api/mysql/teachers/{id}
  Método: SQL SELECT
  Request:
  {
    "id": integer  // ID del profesor
  }
  Query SQL:
  SELECT * FROM teachers WHERE id = ?
  ```

#### Operaciones de Cursos

- **Crear curso**: 
  ```
  Endpoint: POST /api/mysql/courses
  Método: SQL INSERT
  Request:
  {
    "name": "string",        // Nombre del curso
    "description": "string", // Descripción del curso
    "teacher_id": integer    // ID del profesor asignado
  }
  Query SQL:
  INSERT INTO courses (name, description, teacher_id) 
  VALUES (?, ?, ?)
  ```

- **Listar cursos**: 
  ```
  Endpoint: GET /api/mysql/courses
  Método: SQL SELECT
  Request: No requiere parámetros
  Query SQL:
  SELECT * FROM courses
  ```

- **Buscar cursos por profesor**: 
  ```
  Endpoint: GET /api/mysql/courses/teacher/{teacher_id}
  Método: SQL SELECT
  Request:
  {
    "teacher_id": integer  // ID del profesor
  }
  Query SQL:
  SELECT * FROM courses WHERE teacher_id = ?
  ```

#### Operaciones de Inscripciones

- **Crear inscripción**: 
  ```
  Endpoint: POST /api/mysql/enrollments
  Método: SQL INSERT
  Request:
  {
    "student_id": integer,     // ID del estudiante
    "course_id": integer,      // ID del curso
    "enrollment_date": "date"  // Fecha de inscripción (YYYY-MM-DD)
  }
  Query SQL:
  INSERT INTO enrollments (student_id, course_id, enrollment_date) 
  VALUES (?, ?, ?)
  ```

- **Listar inscripciones**: 
  ```
  Endpoint: GET /api/mysql/enrollments
  Método: SQL SELECT
  Request: No requiere parámetros
  Query SQL:
  SELECT * FROM enrollments
  ```

- **Buscar inscripciones por estudiante**: 
  ```
  Endpoint: GET /api/mysql/enrollments/student/{student_id}
  Método: SQL SELECT
  Request:
  {
    "student_id": integer  // ID del estudiante
  }
  Query SQL:
  SELECT c.* FROM courses c
  JOIN enrollments e ON c.id = e.course_id
  WHERE e.student_id = ?
  ```

- **Buscar estudiantes por curso**: 
  ```
  Endpoint: GET /api/mysql/enrollments/course/{course_id}
  Método: SQL SELECT
  Request:
  {
    "course_id": integer  // ID del curso
  }
  Query SQL:
  SELECT s.* FROM students s
  JOIN enrollments e ON s.id = e.student_id
  WHERE e.course_id = ?
  ```

### Endpoints MongoDB

Las siguientes operaciones se realizan mediante el driver de Python para MongoDB:

#### Operaciones de Estudiantes

- **Crear estudiante**: 
  ```
  Endpoint: POST /api/mongo/students
  Método: insert_one
  Request:
  {
    "first_name": "string",    // Nombre del estudiante
    "last_name": "string",     // Apellido del estudiante
    "birth_date": ISODate,     // Fecha de nacimiento
    "email": "string",         // Correo electrónico único
    "address": {
      "street": "string",      // Dirección
      "city": "string",        // Ciudad
      "state": "string",       // Estado/Provincia
      "postal_code": "string", // Código postal
      "country": "string"      // País
    },
    "phone": "string",         // Número telefónico
    "student_id": "string",    // ID de estudiante (formato: "STU000001")
    "enrollment_year": number  // Año de inscripción
  }
  Operación MongoDB:
  db.students.insert_one({...})
  ```

- **Listar estudiantes**: 
  ```
  Endpoint: GET /api/mongo/students
  Método: find
  Request: No requiere parámetros
  Operación MongoDB:
  db.students.find({})
  ```

- **Buscar estudiante por ID**: 
  ```
  Endpoint: GET /api/mongo/students/{id}
  Método: find_one
  Request:
  {
    "_id": ObjectId  // ID de MongoDB
  }
  Operación MongoDB:
  db.students.find_one({"_id": ObjectId("id")})
  ```

- **Buscar estudiante por email**: 
  ```
  Endpoint: GET /api/mongo/students/search?email={email}
  Método: find_one
  Request:
  {
    "email": "string"  // Correo del estudiante
  }
  Operación MongoDB:
  db.students.find_one({"email": "correo@ejemplo.com"})
  ```

#### Operaciones de Profesores

- **Crear profesor**: 
  ```
  Endpoint: POST /api/mongo/teachers
  Método: insert_one/insert_many
  Request:
  {
    "first_name": "string",  // Nombre del profesor
    "last_name": "string",   // Apellido del profesor
    "email": "string",       // Correo electrónico único
    "department": "string",  // Departamento académico
    "phone": "string",       // Número telefónico
    "created_at": ISODate    // Fecha de creación
  }
  Operación MongoDB:
  db.teachers.insert_one({...})
  db.teachers.insert_many([{...}, {...}, ...])
  ```

- **Listar profesores**: 
  ```
  Endpoint: GET /api/mongo/teachers
  Método: find
  Request: No requiere parámetros
  Operación MongoDB:
  db.teachers.find({})
  ```

- **Buscar profesor por ID**: 
  ```
  Endpoint: GET /api/mongo/teachers/{id}
  Método: find_one
  Request:
  {
    "_id": ObjectId  // ID de MongoDB
  }
  Operación MongoDB:
  db.teachers.find_one({"_id": ObjectId("id")})
  ```

#### Operaciones de Cursos

- **Crear curso**: 
  ```
  Endpoint: POST /api/mongo/courses
  Método: insert_one/insert_many
  Request:
  {
    "name": "string",          // Nombre del curso
    "description": "string",   // Descripción del curso
    "teacher_id": ObjectId,    // ID del profesor (referencia)
    "teacher_info": {          // Datos embebidos del profesor
      "first_name": "string",
      "last_name": "string",
      "email": "string"
    },
    "credits": number,         // Créditos académicos
    "duration_weeks": number,  // Duración en semanas
    "created_at": ISODate      // Fecha de creación
  }
  Operación MongoDB:
  db.courses.insert_one({...})
  db.courses.insert_many([{...}, {...}, ...])
  ```

- **Listar cursos**: 
  ```
  Endpoint: GET /api/mongo/courses
  Método: find
  Request: No requiere parámetros
  Operación MongoDB:
  db.courses.find({})
  ```

- **Buscar cursos por profesor**: 
  ```
  Endpoint: GET /api/mongo/courses/teacher/{teacher_id}
  Método: find
  Request:
  {
    "teacher_id": ObjectId  // ID del profesor
  }
  Operación MongoDB:
  db.courses.find({"teacher_id": ObjectId("id")})
  ```

#### Operaciones de Inscripciones

- **Crear inscripción**: 
  ```
  Endpoint: POST /api/mongo/enrollments
  Método: insert_one/insert_many
  Request:
  {
    "student_id": ObjectId,     // ID del estudiante (referencia)
    "course_id": ObjectId,      // ID del curso (referencia)
    "enrollment_date": ISODate,  // Fecha de inscripción
    "status": "string",          // Estado (ej: "active", "completed")
    "grade": number,             // Calificación (opcional)
    "student_info": {            // Datos embebidos del estudiante
      "first_name": "string",
      "last_name": "string",
      "email": "string"
    },
    "course_info": {             // Datos embebidos del curso
      "name": "string",
      "description": "string"
    }
  }
  Operación MongoDB:
  db.enrollments.insert_one({...})
  db.enrollments.insert_many([{...}, {...}, ...])
  ```

- **Listar inscripciones**: 
  ```
  Endpoint: GET /api/mongo/enrollments
  Método: find
  Request: No requiere parámetros
  Operación MongoDB:
  db.enrollments.find({})
  ```

- **Buscar inscripciones por estudiante**: 
  ```
  Endpoint: GET /api/mongo/enrollments/student/{student_id}
  Método: find
  Request:
  {
    "student_id": ObjectId  // ID del estudiante
  }
  Operación MongoDB:
  db.enrollments.find({"student_id": ObjectId("id")})
  ```

- **Buscar inscripciones por curso**: 
  ```
  Endpoint: GET /api/mongo/enrollments/course/{course_id}
  Método: find
  Request:
  {
    "course_id": ObjectId  // ID del curso
  }
  Operación MongoDB:
  db.enrollments.find({"course_id": ObjectId("id")})
  ```

### Operaciones por Lotes

Los scripts `faker_mysql.py` y `faker_mongodb.py` implementan las siguientes operaciones por lotes:

#### MySQL (faker_mysql.py)

- **Inserción masiva de profesores**: Inserta 1,000 registros en la tabla `teachers`
  ```
  Endpoint: Script Python (ejecución directa)
  Comando: python faker_mysql.py
  Operación: Múltiples INSERTs
  Datos generados: 1,000 profesores con información ficticia
  ```

- **Inserción masiva de cursos**: Inserta 30 registros en la tabla `courses`
  ```
  Endpoint: Script Python (ejecución directa)
  Comando: python faker_mysql.py
  Operación: Múltiples INSERTs
  Datos generados: 30 cursos con descripciones y asignaciones de profesores
  ```

- **Inserción masiva de estudiantes**: Inserta 5,000 registros en la tabla `students`
  ```
  Endpoint: Script Python (ejecución directa)
  Comando: python faker_mysql.py
  Operación: Múltiples INSERTs
  Datos generados: 5,000 estudiantes con información personal
  ```

- **Inserción masiva de inscripciones**: Inserta hasta 6,000 registros en la tabla `enrollments`
  ```
  Endpoint: Script Python (ejecución directa)
  Comando: python faker_mysql.py
  Operación: Múltiples INSERTs
  Datos generados: Aproximadamente 6,000 inscripciones con fechas aleatorias
  ```

#### MongoDB (faker_mongodb.py)

- **Inserción masiva de profesores**: Inserta 1,000 documentos en la colección `teachers`
  ```
  Endpoint: Script Python (ejecución directa)
  Comando: python faker_mongodb.py
  Operación: insert_many
  Datos generados: 1,000 profesores con información ampliada
  ```

- **Inserción masiva de cursos**: Inserta 30 documentos en la colección `courses`
  ```
  Endpoint: Script Python (ejecución directa)
  Comando: python faker_mongodb.py
  Operación: insert_many
  Datos generados: 30 cursos con datos de profesores embebidos
  ```

- **Inserción masiva de estudiantes**: Inserta 5,000 documentos en la colección `students`
  ```
  Endpoint: Script Python (ejecución directa)
  Comando: python faker_mongodb.py
  Operación: insert_many
  Datos generados: 5,000 estudiantes con información detallada y dirección
  ```

- **Inserción masiva de inscripciones**: Inserta hasta 6,000 documentos en la colección `enrollments`
  ```
  Endpoint: Script Python (ejecución directa)
  Comando: python faker_mongodb.py
  Operación: insert_many
  Datos generados: Aproximadamente 6,000 inscripciones con referencias a estudiantes y cursos
  ```

