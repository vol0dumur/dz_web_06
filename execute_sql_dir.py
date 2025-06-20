import os
from psycopg2 import DatabaseError
from connect import create_connection
import logging


SQL_DIR = "C:\\Documents\\enic\\My_repo\\2025-06\\2025-06-18\\sql"


def read_sql_files(directory: str):
    """Ітератор, який читає вміст SQL-файлів у заданій директорії та повертає їх як рядки."""

    try:
        for filename in os.listdir(directory):
            if filename.endswith('.sql'):  # Обробляємо тільки файли з розширенням .sql
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    yield file.read()
    except OSError as e:
        logging.error(f"Помилка при читанні директорії {directory}: {e}")
        return


def execute_sql_query(sql_query: str) -> str:
    """Виконує SQL-запит і повертає результат як рядок."""

    try:
        with create_connection() as conn:
            if conn is None:
                return "Помилка: не вдалося встановити з'єднання з базою даних"
            
            c = conn.cursor()
            try:
                c.execute(sql_query)
                conn.commit()
                
                # Якщо запит повертає дані (наприклад, SELECT)
                if c.description:  # Перевіряємо, чи є результат
                    rows = c.fetchall()
                    # Перетворюємо результат у рядок
                    result = "\n".join([str(row) for row in rows])
                    return result if result else "Запит виконано, але результат порожній"
                return "Запит успішно виконано"
                
            except DatabaseError as e:
                logging.error(f"Помилка виконання SQL-запиту: {e}")
                conn.rollback()
                return f"Помилка виконання запиту: {str(e)}"
            finally:
                c.close()
                
    except RuntimeError as e:
        logging.error(f"Помилка з'єднання: {e}")
        return f"Помилка з'єднання: {str(e)}"
    

def split_query(query):

    return query[2:query.find("\n")].strip(), query[query.find("\n")+1:]
    

if __name__ == "__main__":

    for query in read_sql_files(SQL_DIR):

        if query.startswith("--"):

            comment, query = split_query(query)
            print(f"* * *\n{comment}\n{execute_sql_query(query)}\n")