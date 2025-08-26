# Script para poblar la base de datos MySQL de escuela con datos ficticios
import mysql.connector
from faker import Faker
from datetime import datetime, timedelta
import random

# Inicializar Faker
fake = Faker('es_ES')  # Configurado para español

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'school',
    'port': 3308
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
        # Conectar a la base de datos
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Conjunto para rastrear emails únicos
        used_emails = set()

        # Poblar teachers (profesores)
        teachers = []
        print("Insertando profesores...")
        for i in range(NUM_TEACHERS):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = generate_unique_email(used_emails)

            cursor.execute(
                'INSERT INTO teachers (first_name, last_name, email) VALUES (%s, %s, %s)',
                (first_name, last_name, email)
            )
            teacher_id = cursor.lastrowid
            teachers.append({
                'id': teacher_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            })

            # Mostrar progreso cada 100 registros
            if (i + 1) % 100 == 0:
                print(f"Profesores insertados: {i + 1}/{NUM_TEACHERS}")

        conn.commit()
        print(f"Insertados {NUM_TEACHERS} profesores")

        # Poblar courses (cursos)
        courses = []
        course_subjects = [
            'Matemáticas Avanzadas',
            'Historia Mundial',
            'Química Orgánica',
            'Literatura Española',
            'Física Cuántica',
            'Biología Molecular',
            'Programación Python',
            'Arte Contemporáneo',
            'Geografía Humana',
            'Filosofía Moderna',
            'Inglés Básico',
            'Francés Intermedio',
            'Estadística',
            'Economía',
            'Sociología',
            'Psicología',
            'Arquitectura',
            'Ingeniería Civil',
            'Medicina General',
            'Derecho Constitucional',
            'Administración',
            'Marketing Digital',
            'Diseño Gráfico',
            'Música Clásica',
            'Educación Física',
            'Nutrición',
            'Veterinaria',
            'Agricultura',
            'Astronomía',
            'Geología'
        ]

        print("Insertando cursos...")
        for i in range(NUM_COURSES):
            name = random.choice(course_subjects)
            description = fake.text(max_nb_chars=200)
            teacher_id = random.choice(teachers)['id']

            cursor.execute(
                'INSERT INTO courses (name, description, teacher_id) VALUES (%s, %s, %s)',
                (name, description, teacher_id)
            )
            course_id = cursor.lastrowid
            courses.append({
                'id': course_id,
                'name': name,
                'description': description,
                'teacher_id': teacher_id
            })

        conn.commit()
        print(f"Insertados {NUM_COURSES} cursos")

        # Poblar students (estudiantes)
        students = []
        print("Insertando estudiantes...")
        for i in range(NUM_STUDENTS):
            first_name = fake.first_name()
            last_name = fake.last_name()
            # Generar fecha de nacimiento para estudiantes entre 16-25 años
            birth_date = fake.date_of_birth(minimum_age=16, maximum_age=25)
            email = generate_unique_email(used_emails)

            cursor.execute(
                'INSERT INTO students (first_name, last_name, birth_date, email) VALUES (%s, %s, %s, %s)',
                (first_name, last_name, birth_date, email)
            )
            student_id = cursor.lastrowid
            students.append({
                'id': student_id,
                'first_name': first_name,
                'last_name': last_name,
                'birth_date': birth_date,
                'email': email
            })

            # Mostrar progreso cada 500 registros
            if (i + 1) % 500 == 0:
                print(f"Estudiantes insertados: {i + 1}/{NUM_STUDENTS}")

        conn.commit()
        print(f"Insertados {NUM_STUDENTS} estudiantes")

        # Poblar enrollments (matrículas)
        print("Insertando matrículas...")
        enrollments_created = 0
        enrollment_combinations = set()  # Para evitar duplicados

        for i in range(NUM_ENROLLMENTS):
            student_id = random.choice(students)['id']
            course_id = random.choice(courses)['id']
            combination = (student_id, course_id)

            # Evitar combinaciones duplicadas
            if combination in enrollment_combinations:
                continue

            enrollment_combinations.add(combination)
            # Fecha de matrícula en los últimos 90 días
            enrollment_date = fake.date_between(start_date='-90d', end_date='today')

            try:
                cursor.execute(
                    'INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES (%s, %s, %s)',
                    (student_id, course_id, enrollment_date)
                )
                enrollments_created += 1

                # Mostrar progreso cada 500 registros
                if enrollments_created % 500 == 0:
                    print(f"Matrículas insertadas: {enrollments_created}")

            except mysql.connector.IntegrityError:
                # Si hay un constraint de unicidad, continuar con la siguiente matrícula
                continue

        conn.commit()
        print(f"Insertadas {enrollments_created} matrículas")

        cursor.close()
        conn.close()
        print('Datos generados exitosamente en MySQL.')

    except mysql.connector.Error as error:
        print(f"Error al conectar con MySQL: {error}")
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()
