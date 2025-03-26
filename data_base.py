import os
import psycopg2

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('FSTR_DB_HOST'),
                port=os.getenv('FSTR_DB_PORT'),
                user=os.getenv('FSTR_DB_LOGIN'),
                password=os.getenv('FSTR_DB_PASS'),
                dbname='your_database_name'  # Укажите имя Вашей базы данных
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def submit_data(self, raw_data):
        status = 'new'
        # Предполагается, что raw_data содержит необходимые поля для вставки
        try:
            insert_query = """
            INSERT INTO pereval_added (raw_data, status)
            VALUES (%s, %s) RETURNING id;
            """
            self.cursor.execute(insert_query, (raw_data, status))
            self.connection.commit()
            return self.cursor.fetchone()[0]  # Возвращаем ID вставленной записи
        except Exception as e:
            print(f"Error inserting data: {e}")
            self.connection.rollback()
        finally:
            self.cursor.close()
            self.connection.close()