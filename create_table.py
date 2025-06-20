from psycopg2 import DatabaseError
from connect import create_connection
import logging


def create_table(conn, sql_exression: str):

    c = conn.cursor()
    try:
        c.execute(sql_exression)
        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        c.close()


if __name__ == "__main__":

    sql_queries = ["""
                   CREATE TABLE groups (
                       id SERIAL PRIMARY KEY,
                       name VARCHAR(50) NOT NULL
                   );
                   """,
                   """
                   CREATE TABLE teachers (
                       id SERIAL PRIMARY KEY,
                       full_name VARCHAR(100) NOT NULL
                   );
                   """,
                   """
                   CREATE TABLE subjects (
                       id SERIAL PRIMARY KEY,
                       name VARCHAR(100) NOT NULL,
                       teacher_id INTEGER REFERENCES teachers(id)
                   );
                   """,
                   """
                   CREATE TABLE students (
                       id SERIAL PRIMARY KEY,
                       full_name VARCHAR(100) NOT NULL,
                       group_id INTEGER REFERENCES groups(id)
                   );
                   """,
                   """
                   CREATE TABLE student_subjects (
                       student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
                       subject_id INTEGER REFERENCES subjects(id) ON DELETE CASCADE,
                       PRIMARY KEY (student_id, subject_id)
                   );
                   """,
                   """
                   CREATE TABLE grades (
                       id SERIAL PRIMARY KEY,
                       student_id INTEGER REFERENCES students(id),
                       subject_id INTEGER REFERENCES subjects(id),
                       grade INTEGER CHECK (grade >= 0 AND grade <= 100),
                       grade_date DATE
                   );
                   """]

    for sql_exression in sql_queries:
        try:
            with create_connection() as conn:
                if conn is not None:
                    create_table(conn, sql_exression)
                else:
                    print("Error! cannot create the database connection.")
        except RuntimeError as err:
            logging.error(err)
            
        print("Таблиці успішно створені!")