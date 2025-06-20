import logging
from random import randint, choice, sample
from faker import Faker
from psycopg2 import DatabaseError
from connect import create_connection
from datetime import datetime

# Кількість студентів
N_STUDENTS = 50
# Кількість груп
N_GROUPS = 3
# Кількість предметів
N_SUBJECTS = 8
# Предмети для випадкового обирання
SUBJECTS = ["Вища математика", "Фізика", "Хімія", "Інформатика та програмування", "Іноземна мова", "Філософія",\
            "Історія України", "Економічна теорія", "Правознавство", "Українська мова", "Психологія", "Екологія"\
            "Механіка та опір матеріалів", "Промисловий дизайн", "Накреслювальна геометрія", "Бухгалтерський облік"]
# Кількість викладачів
N_TEACHERS = 5
# Кількість оцінок у кожного студента з усіх предметів
N_MARKS = 20

fake = Faker("uk-UA")


def insert_data():
    try:
        with create_connection() as conn:
            cur = conn.cursor()

            # Додаємо групи
            group_ids = []
            for i in range(N_GROUPS):
                cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id;", (f"GR-{datetime.now().year}-{i+1}",))
                group_ids.append(cur.fetchone()[0])

            # Додаємо викладачів
            teacher_ids = []
            for _ in range(N_TEACHERS):
                cur.execute("INSERT INTO teachers (full_name) VALUES (%s) RETURNING id;", (fake.name(),))
                teacher_ids.append(cur.fetchone()[0])

            # Додаємо предмети
            subject_ids = []
            for i in range(N_SUBJECTS):
                subject_name = choice(SUBJECTS)
                teacher_id = choice(teacher_ids)
                cur.execute("INSERT INTO subjects (name, teacher_id) VALUES (%s, %s) RETURNING id;",
                            (subject_name, teacher_id))
                subject_ids.append(cur.fetchone()[0])

            # Додаємо студентів
            student_ids = []
            for _ in range(N_STUDENTS):
                full_name = fake.name()
                group_id = choice(group_ids)
                cur.execute("INSERT INTO students (full_name, group_id) VALUES (%s, %s) RETURNING id;",
                            (full_name, group_id))
                student_id = cur.fetchone()[0]
                student_ids.append(student_id)

                # Призначаємо студенту випадкові курси (3–5)
                subjects_for_student = sample(subject_ids, k=randint(3, 5))
                for subject_id in subjects_for_student:
                    cur.execute("""
                        INSERT INTO student_subjects (student_id, subject_id)
                        VALUES (%s, %s);
                    """, (student_id, subject_id))

            # Додаємо оцінки
            for student_id in student_ids:
                # Отримуємо курси, які відвідує студент
                cur.execute("""
                    SELECT subject_id FROM student_subjects
                    WHERE student_id = %s;
                """, (student_id,))
                enrolled_subjects = [row[0] for row in cur.fetchall()]

                for _ in range(N_MARKS):
                    subject_id = choice(enrolled_subjects)
                    grade = randint(60, 100)
                    date = fake.date_between(start_date="-1y", end_date="today")
                    cur.execute("""
                        INSERT INTO grades (student_id, subject_id, grade, grade_date)
                        VALUES (%s, %s, %s, %s);
                    """, (student_id, subject_id, grade, date))

            conn.commit()
            cur.close()
            
            print("Дані успішно додані!")

    except DatabaseError as e:
        logging.error(e)
        if conn:
            conn.rollback()


if __name__ == "__main__":
    insert_data()