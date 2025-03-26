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
            return None
        finally:
            self.cursor.close()
            self.connection.close()

    def get_data_by_id(self, record_id):
        try:
            select_query = "SELECT * FROM pereval_added WHERE id = %s;"
            self.cursor.execute(select_query, (record_id,))
            record = self.cursor.fetchone()
            if record:
                return record  # Вернуть всю информацию о записи
            return None
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def update_data(self, record_id, data):
        try:
            # Проверяем статус записи
            select_query = "SELECT status FROM pereval_added WHERE id = %s;"
            self.cursor.execute(select_query, (record_id,))
            status = self.cursor.fetchone()
            if not status or status[0] != 'new':
                return False  # Запись не может быть обновлена

            # Формируем запрос на обновление
            update_query = """
            UPDATE pereval_added SET raw_data = %s WHERE id = %s;
            """
            self.cursor.execute(update_query, (data['raw_data'], record_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating data: {e}")
            self.connection.rollback()
            return False

    def get_data_by_email(self, email):
        try:
            select_query = "SELECT * FROM pereval_added WHERE user_email = %s;"  # Предполагаем, что в raw_data есть поле user_email
            self.cursor.execute(select_query, (email,))
            records = self.cursor.fetchall()
            return records
        except Exception as e:
            print(f"Error fetching data by email: {e}")
            return []