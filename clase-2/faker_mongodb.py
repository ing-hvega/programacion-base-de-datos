# Script para poblar la base de datos MongoDB de escuela con datos ficticios
from pymongo import MongoClient
from faker import Faker
from datetime import datetime, timedelta
import random
from bson import ObjectId

# Inicializar Faker
fake = Faker('es_ES')  # Configurado para español

MONGO_CONFIG = {
    'host': 'localhost',
    'port': 27018,
    'username': 'admin',
    'password': 'admin',
    'database': 'main',
    'authSource': 'admin'
}

NUM_STUDENTS = 5000
NUM_TEACHERS = 1000
NUM_COURSES = 30
NUM_ENROLLMENTS = 6000


def generate_unique_email(used_emails):
    """Genera un email único que no esté en el conjunto de emails usados"""
    max_attempts = 1000
    attempts = 0

    while attempts < max_attempts:
        email = fake.email()
        if email not in used_emails:
            used_emails.add(email)
            return email
        attempts += 1

    # Si después de muchos intentos no encuentra uno único, crear uno con timestamp
    unique_email = f"{fake.user_name()}{int(datetime.now().timestamp())}@{fake.domain_name()}"
    used_emails.add(unique_email)
    return unique_email


def main():
    try:
        # Conectar a MongoDB
        client = MongoClient(
            host=MONGO_CONFIG['host'],
            port=MONGO_CONFIG['port'],
            username=MONGO_CONFIG['username'],
            password=MONGO_CONFIG['password'],
            authSource=MONGO_CONFIG['authSource']
        )

        # Seleccionar la base de datos
        db = client[MONGO_CONFIG['database']]

        # Conjunto para rastrear emails únicos
        used_emails = set()

        # Limpiar colecciones existentes
        db.teachers.delete_many({})
        db.courses.delete_many({})
        db.students.delete_many({})
        db.enrollments.delete_many({})
        print("Colecciones limpiadas")

        # Poblar teachers (profesores) - usando inserción por lotes para mejor rendimiento
        print("Insertando profesores...")
        teachers_data = []

        for i in range(NUM_TEACHERS):
            teacher_doc = {
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': generate_unique_email(used_emails),
                'department': fake.job(),
                'phone': fake.phone_number(),
                'created_at': datetime.now()
            }
            teachers_data.append(teacher_doc)

            # Mostrar progreso cada 100 registros
            if (i + 1) % 100 == 0:
                print(f"Preparando profesores: {i + 1}/{NUM_TEACHERS}")

        # Insertar teachers en lote
        result = db.teachers.insert_many(teachers_data)
        print(f"Insertados {NUM_TEACHERS} profesores")

        # Poblar courses (cursos)
        course_subjects = [
            'Matemáticas Avanzadas', 'Historia Mundial', 'Química Orgánica', 'Literatura Española',
            'Física Cuántica', 'Biología Molecular', 'Programación Python', 'Arte Contemporáneo',
            'Geografía Humana', 'Filosofía Moderna', 'Inglés Básico', 'Francés Intermedio',
            'Estadística', 'Economía', 'Sociología', 'Psicología', 'Arquitectura',
            'Ingeniería Civil', 'Medicina General', 'Derecho Constitucional', 'Administración',
            'Marketing Digital', 'Diseño Gráfico', 'Música Clásica', 'Educación Física',
            'Nutrición', 'Veterinaria', 'Agricultura', 'Astronomía', 'Geología'
        ]

        print("Insertando cursos...")
        courses_data = []

        for i in range(NUM_COURSES):
            teacher = random.choice(teachers_data)
            course_doc = {
                'name': random.choice(course_subjects),
                'description': fake.text(max_nb_chars=200),
                'teacher_id': teacher['_id'] if '_id' in teacher else None,
                'teacher_info': {
                    'first_name': teacher['first_name'],
                    'last_name': teacher['last_name'],
                    'email': teacher['email']
                },
                'credits': random.choice([3, 4, 5, 6]),
                'duration_weeks': random.choice([12, 16, 20]),
                'created_at': datetime.now()
            }
            courses_data.append(course_doc)

        # Insertar courses en lote
        result = db.courses.insert_many(courses_data)

        # Actualizar courses_data con los IDs generados
        for i, course_id in enumerate(result.inserted_ids):
            courses_data[i]['_id'] = course_id

        print(f"Insertados {NUM_COURSES} cursos")

        # Poblar students (estudiantes) - usando inserción por lotes
        print("Insertando estudiantes...")
        students_data = []

        for i in range(NUM_STUDENTS):
            birth_date = fake.date_of_birth(minimum_age=16, maximum_age=25)
            student_doc = {
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'birth_date': datetime.combine(birth_date, datetime.min.time()),  # Convertir date a datetime
                'email': generate_unique_email(used_emails),
                'address': {
                    'street': fake.street_address(),
                    'city': fake.city(),
                    'state': fake.state(),
                    'postal_code': fake.postcode(),
                    'country': 'España'
                },
                'phone': fake.phone_number(),
                'student_id': f"STU{str(i+1).zfill(6)}",
                'enrollment_year': random.choice([2020, 2021, 2022, 2023, 2024]),
                'status': random.choice(['active', 'inactive', 'graduated']),
                'created_at': datetime.now()
            }
            students_data.append(student_doc)

            # Mostrar progreso cada 500 registros
            if (i + 1) % 500 == 0:
                print(f"Preparando estudiantes: {i + 1}/{NUM_STUDENTS}")

        # Insertar students en lotes de 1000 para mejor rendimiento
        batch_size = 1000
        for i in range(0, len(students_data), batch_size):
            batch = students_data[i:i + batch_size]
            result = db.students.insert_many(batch)

            # Actualizar con los IDs generados
            for j, student_id in enumerate(result.inserted_ids):
                students_data[i + j]['_id'] = student_id

            print(f"Insertado lote de estudiantes: {min(i + batch_size, len(students_data))}/{NUM_STUDENTS}")

        print(f"Insertados {NUM_STUDENTS} estudiantes")

        # Poblar enrollments (matrículas)
        print("Insertando matrículas...")
        enrollments_data = []
        enrollment_combinations = set()
        enrollments_created = 0

        for i in range(NUM_ENROLLMENTS):
            student = random.choice(students_data)
            course = random.choice(courses_data)
            combination = (student['_id'], course['_id'])

            # Evitar combinaciones duplicadas
            if combination in enrollment_combinations:
                continue

            enrollment_combinations.add(combination)

            enrollment_doc = {
                'student_id': student['_id'],
                'course_id': course['_id'],
                'student_info': {
                    'first_name': student['first_name'],
                    'last_name': student['last_name'],
                    'email': student['email'],
                    'student_id': student['student_id']
                },
                'course_info': {
                    'name': course['name'],
                    'description': course['description'],
                    'credits': course['credits']
                },
                'enrollment_date': datetime.combine(fake.date_between(start_date='-90d', end_date='today'), datetime.min.time()),  # Convertir date a datetime
                'status': random.choice(['enrolled', 'completed', 'withdrawn', 'pending']),
                'grade': random.choice([None, fake.random_int(min=60, max=100)]),
                'semester': random.choice(['2024-1', '2024-2', '2025-1']),
                'created_at': datetime.now()
            }

            enrollments_data.append(enrollment_doc)
            enrollments_created += 1

            # Insertar en lotes de 1000
            if len(enrollments_data) >= 1000:
                db.enrollments.insert_many(enrollments_data)
                print(f"Matrículas insertadas: {enrollments_created}")
                enrollments_data = []

        # Insertar el lote restante
        if enrollments_data:
            db.enrollments.insert_many(enrollments_data)

        print(f"Insertadas {enrollments_created} matrículas")

        # Crear índices para mejorar el rendimiento
        print("Creando índices...")
        db.teachers.create_index("email", unique=True)
        db.students.create_index("email", unique=True)
        db.students.create_index("student_id", unique=True)
        db.courses.create_index("teacher_id")
        db.enrollments.create_index([("student_id", 1), ("course_id", 1)], unique=True)
        db.enrollments.create_index("enrollment_date")
        print("Índices creados")

        # Mostrar estadísticas finales
        print("\n--- Estadísticas Finales ---")
        print(f"Teachers: {db.teachers.count_documents({})}")
        print(f"Students: {db.students.count_documents({})}")
        print(f"Courses: {db.courses.count_documents({})}")
        print(f"Enrollments: {db.enrollments.count_documents({})}")
        print(f"Emails únicos utilizados: {len(used_emails)}")

        client.close()
        print('\nDatos generados exitosamente en MongoDB.')

    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()
