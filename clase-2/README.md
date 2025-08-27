# Proyecto Clase-2: Sistema de Gestión Escolar con Bases de Datos

Este proyecto implementa un sistema de gestión escolar utilizando dos bases de datos diferentes (MySQL y MongoDB) con Docker para la containerización y scripts de Python para poblar las bases de datos con datos ficticios.

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Base de Datos](#base-de-datos)
- [Scripts de Población](#scripts-de-población)
- [Docker](#docker)
- [Solución de Problemas](#solución-de-problemas)

## 🎯 Descripción del Proyecto

El proyecto **Clase-2** es un sistema de gestión escolar que demuestra el uso de dos sistemas de gestión de bases de datos diferentes:

- **MySQL**: Base de datos relacional para almacenar información estructurada de estudiantes, profesores, cursos e inscripciones
- **MongoDB**: Base de datos NoSQL para almacenar la misma información en formato de documentos JSON

El sistema incluye scripts automatizados para poblar ambas bases de datos con datos ficticios realistas utilizando la librería Faker.

## 📁 Estructura del Proyecto

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

## 🛠 Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje de programación principal
- **MySQL 8.0.23**: Base de datos relacional
- **MongoDB 8.0.12**: Base de datos NoSQL
- **Docker & Docker Compose**: Containerización y orquestación
- **Faker**: Generación de datos ficticios
- **pymongo**: Driver de Python para MongoDB
- **mysql-connector-python**: Driver de Python para MySQL

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.8 o superior**
- **Docker Desktop** (para Windows/Mac) o **Docker Engine** (para Linux)
- **Docker Compose** (incluido en Docker Desktop)
- **Git** (opcional, para clonar el repositorio)

### Verificar Instalaciones

```bash
python --version
docker --version
docker-compose --version
```

## 🚀 Instalación

### Paso 1: Clonar o Descargar el Proyecto

Si tienes acceso al repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd clase-2
```

### Paso 2: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones (opcional, los valores por defecto funcionan)
```

## ⚙️ Configuración

### Variables de Entorno (.env)

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

### Configuración de Puertos

- **MySQL**: Puerto 3308 (para evitar conflictos con instalaciones locales)
- **MongoDB**: Puerto 27018 (para evitar conflictos con instalaciones locales)

## 🖥 Uso

### Paso 1: Iniciar los Contenedores

```bash
# Construir e iniciar los contenedores
docker-compose up -d

# Verificar que los contenedores estén ejecutándose
docker-compose ps
```

### Paso 2: Crear la Base de Datos MySQL

```bash
# Ejecutar el script SQL en MySQL
docker exec -i mysqldb mysql -uroot -proot < colegio.sql
```

### Paso 3: Poblar las Bases de Datos

```bash
# Poblar MySQL con datos ficticios
python faker_mysql.py

# Poblar MongoDB con datos ficticios
python faker_mongodb.py
```

### Comandos Útiles de Docker

```bash
# Ver logs de los contenedores
docker-compose logs mysql
docker-compose logs mongo

# Detener los contenedores
docker-compose stop

# Reiniciar los contenedores
docker-compose restart

# Eliminar contenedores y volúmenes
docker-compose down -v
```

## 🗄 Base de Datos

### Esquema MySQL

La base de datos `school` contiene las siguientes tablas:

1. **students** (estudiantes)
   - `id`: Clave primaria auto-incrementable
   - `first_name`: Nombre del estudiante
   - `last_name`: Apellido del estudiante
   - `birth_date`: Fecha de nacimiento
   - `email`: Correo electrónico único

2. **teachers** (profesores)
   - `id`: Clave primaria auto-incrementable
   - `first_name`: Nombre del profesor
   - `last_name`: Apellido del profesor
   - `email`: Correo electrónico único

3. **courses** (cursos)
   - `id`: Clave primaria auto-incrementable
   - `name`: Nombre del curso
   - `description`: Descripción del curso
   - `teacher_id`: Clave foránea hacia teachers

4. **enrollments** (inscripciones)
   - `id`: Clave primaria auto-incrementable
   - `student_id`: Clave foránea hacia students
   - `course_id`: Clave foránea hacia courses
   - `enrollment_date`: Fecha de inscripción
   - `grade`: Calificación (opcional)

### Esquema MongoDB

La base de datos `main` contiene las siguientes colecciones:

- **students**: Documentos con información de estudiantes
- **teachers**: Documentos con información de profesores
- **courses**: Documentos con información de cursos
- **enrollments**: Documentos con información de inscripciones

Cada documento mantiene la misma estructura lógica que las tablas MySQL pero en formato JSON.

## 🔄 Scripts de Población

### faker_mysql.py

Este script se conecta a la base de datos MySQL y genera:
- **5,000 estudiantes** con datos ficticios realistas
- **1,000 profesores** con información completa
- **30 cursos** con descripciones y asignaciones de profesores
- **6,000 inscripciones** con fechas y calificaciones aleatorias

### faker_mongodb.py

Este script replica la misma funcionalidad para MongoDB:
- Genera los mismos volúmenes de datos
- Mantiene coherencia referencial mediante ObjectIds
- Utiliza el mismo generador Faker configurado para español

### Características de los Scripts

- **Emails únicos**: Garantizan que no se repitan direcciones de correo
- **Datos realistas**: Utilizan Faker configurado para español (es_ES)
- **Relaciones coherentes**: Mantienen integridad referencial
- **Manejo de errores**: Incluyen try-catch para capturar problemas de conexión
- **Progreso visual**: Muestran el progreso de la población de datos

## 🐳 Docker

### docker-compose.yml

El archivo de Docker Compose define dos servicios:

1. **mysql**:
   - Imagen: mysql:8.0.23
   - Puerto: 3308:3306
   - Variables de entorno configurables
   - Volumen persistente para datos

2. **mongo**:
   - Imagen personalizada basada en mongo:8.0.12
   - Puerto: 27018:27017
   - Script de inicialización personalizado
   - Volumen persistente para datos

### Volúmenes

- `mysql_data`: Persiste los datos de MySQL
- `mongo_data`: Persiste los datos de MongoDB

## 🔧 Solución de Problemas

### Error de Conexión a MySQL

```bash
# Verificar que el contenedor esté ejecutándose
docker-compose ps

# Ver logs del contenedor MySQL
docker-compose logs mysql

# Reiniciar el contenedor
docker-compose restart mysql
```

### Error de Conexión a MongoDB

```bash
# Verificar logs de MongoDB
docker-compose logs mongo

# Conectar manualmente para verificar
docker exec -it mongodb mongosh -u admin -p admin
```

### Error de Dependencias de Python

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Reinstalar dependencias
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Puertos en Uso

Si los puertos 3308 o 27018 están ocupados:

1. Editar el archivo `.env`
2. Cambiar las variables `FORWARD_MYSQL_PORT` y `FORWARD_MONGODB_PORT`
3. Actualizar las configuraciones en los scripts Python
4. Reiniciar los contenedores

### Limpiar y Reiniciar

```bash
# Detener y eliminar todo
docker-compose down -v

# Eliminar imágenes (opcional)
docker rmi clase-2_mongo mysql:8.0.23

# Volver a construir
docker-compose up -d --build
```

## 📝 Notas Adicionales

- Los datos generados son completamente ficticios y seguros para usar en desarrollo
- Los scripts pueden tardar varios minutos en completarse dependiendo del hardware
- Se recomienda usar un entorno virtual para evitar conflictos de dependencias
- Los volúmenes de Docker persisten los datos entre reinicios de contenedores

## 🤝 Contribuciones

Este proyecto es parte de un curso educativo. Para mejoras o sugerencias:

1. Crea una rama con tu feature
2. Realiza los cambios necesarios
3. Asegúrate de que los scripts funcionen correctamente
4. Envía un pull request con descripción detallada

---

**Autor**: Henry Vega   
**Fecha**: 2025  
**Versión**: 1.0
