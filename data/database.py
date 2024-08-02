import sqlite3
import os
from datetime import datetime
from tests.decorators import handle_db_errors


class DatabaseManager:
    """
    Класс для управления базой данных SQLite.

    Attributes:
        db_path (str): Путь к файлу базы данных.
    """

    def __init__(self, db_path):
        """
        Инициализация DatabaseManager с указанием пути к базе данных.

        Args:
            db_path (str): Путь к файлу базы данных.
        """
        self.db_path = db_path
        self.ignor_tbales = ['CompetitionData', 'sqlite_sequence', 'accounts', 'statistics']

    @handle_db_errors
    def delete_database(self):
        """
        Удаление базы данных.

        Returns:
            None
        """
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f"Database {self.db_path} has been deleted.\n")
        else:
            print(f"No database found at {self.db_path} to delete.\n")

    @handle_db_errors
    def remove_table(self, table_name):
        """
        Удаление таблицы из базы данных.

        Args:
            table_name (str): Имя таблицы для удаления.

        Returns:
            None
        """
        # Подключение к базе данных (или создание, если она не существует)
        conn = sqlite3.connect(self.db_path)

        # Создание курсора для выполнения SQL команд
        c = conn.cursor()

        # SQL запрос на создание таблицы
        create_table_query = f"""
            DROP TABLE IF EXISTS '{table_name}';
            """

        # Выполнение SQL запроса
        c.execute(create_table_query)

        # Сохранение изменений
        conn.commit()

        # Закрытие соединения с базой данных
        conn.close()

    def check_database_exists(self):
        """
        Проверяет наличие базы данных по указанному пути.

        Returns:
            bool: True, если база данных существует, иначе False.
        """
        return os.path.isfile(self.db_path)

    def insert_keywords_to_db(self, table_name, column_name, keywords):
        """
        Вставляет ключевые фразы в указанную таблицу и колонку базы данных SQLite.

        Args:
            table_name (str): Имя таблицы, в которую нужно вставить данные.
            column_name (str): Имя колонки, в которую нужно вставить данные.
            keywords (list of str): Список ключевых фраз для вставки.

        Returns:
            None
        """
        try:
            # Подключение к базе данных SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Проверка существования таблицы и колонки
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [info[1] for info in cursor.fetchall()]

            if column_name not in columns:
                print(f"Column '{column_name}' does not exist in table '{table_name}'.")
                return

            # Вставка ключевых фраз
            for keyword in keywords:
                cursor.execute(f"INSERT INTO {table_name} ({column_name}) VALUES (?)", (keyword,))

            # Сохранение изменений
            conn.commit()
            print(f"Keywords have been successfully inserted into '{column_name}' of '{table_name}'.")
            conn.close()

        except sqlite3.Error as e:
            print(f"Error with SQLite database: {e}")

    @handle_db_errors
    def __create_keyword_table__(self, keyword_query):
        """
        Создание таблицы для хранения данных по ключевому слову.

        Args:
            keyword_query (str): Ключевое слово.

        Returns:
            None
        """
        # Подключение к базе данных (или создание, если она не существует)
        conn = sqlite3.connect(self.db_path)

        # Создание курсора для выполнения SQL команд
        c = conn.cursor()

        # Запрос для cоздания БД
        create_table_query = f"""
                        CREATE TABLE IF NOT EXISTS '{keyword_query}' (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT,
                            url TEXT UNIQUE,
                            date TEXT,
                            key_word TEXT,
                            views INTEGER,
                            followers INTEGER,
                            answers INTEGER,
                            related_answers INTEGER,
                            avg_top3_upvotes INTEGER
                        );
                        """

        # Выполнение SQL запроса
        c.execute(create_table_query)

        # Сохранение изменений
        conn.commit()

        # Закрытие соединения с базой данных
        conn.close()

    @handle_db_errors
    def create_table_competition_data(self):
        """
        Создание таблицы CompetitionData в базе данных, если она еще не существует.

        Таблица включает следующие столбцы:
            - id: Уникальный идентификатор (PRIMARY KEY)
            - title: Заголовок записи
            - url: Уникальный URL (UNIQUE)
            - date: Дата записи
            - key_word: Ключевое слово
            - totalResults: Общее количество результатов
            - next_page: Следующая страница
            - status: Статус записи

        Returns:
            None
        """
        # Подключение к базе данных (или создание, если она не существует)
        conn = sqlite3.connect(self.db_path)

        # Создание курсора для выполнения SQL команд
        c = conn.cursor()

        # SQL запрос на создание таблицы
        create_table_query = """
            CREATE TABLE IF NOT EXISTS CompetitionData (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                competition_index INT,
                competition TEXT,
                high_top_of_page_bid INT,
                low_top_of_page_bid INT,
                totalResults INT,
                next_page INT,
                status INT
            );
            """

        # Выполнение SQL запроса
        if c.execute(create_table_query):
            print(f'Table "CompetitionData" was successfully installed into ({self.db_path}) data base')
        else:
            print('Table "CompetitionData" was not installed')

        # Сохранение изменений
        conn.commit()

        # Закрытие соединения с базой данных
        conn.close()

    @handle_db_errors
    def create_table_queries(self):
        """
        Создание таблицы queries в базе данных, если она еще не существует.

        Таблица включает следующие столбцы:
            - id: Уникальный идентификатор (PRIMARY KEY)
            - title: Заголовок записи
            - url: Уникальный URL (UNIQUE)
            - date: Дата записи
            - key_word: Ключевое слово

        Returns:
            None
        """
        # Подключение к базе данных (или создание, если она не существует)
        conn = sqlite3.connect(self.db_path)

        # Создание курсора для выполнения SQL команд
        c = conn.cursor()

        create_table_query = """
                CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    url TEXT UNIQUE,
                    date TEXT,
                    key_word TEXT
                );
                """

        # Выполнение SQL запроса
        if c.execute(create_table_query):
            print(f'Table "queries" was successfully installed into ({self.db_path}) data base\n')
        else:
            print('Table "queries" was not installed\n')

        # Сохранение изменений
        conn.commit()

        # Закрытие соединения с базой данных
        conn.close()

    @handle_db_errors
    def create_table_accounts(self):
        """
        Создание таблицы accounts в базе данных, если она еще не существует.

        Таблица включает следующие столбцы:
            - id: Уникальный идентификатор (PRIMARY KEY)
            - email: Email адрес
            - api_key: API ключ
            - cse_id: Идентификатор CSE
            - usage_date: Дата использования
            - request_count: Количество запросов (по умолчанию 0)

        Returns:
            None
        """
        # Подключение к базе данных (или создание, если она не существует)
        conn = sqlite3.connect(self.db_path)

        # Создание курсора для выполнения SQL команд
        c = conn.cursor()

        create_table_query = """
                    CREATE TABLE IF NOT EXISTS accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT,
                        api_key TEXT,
                        cse_id TEXT,
                        usage_date TEXT,
                        req_limits INT,
                        status INT DEFAULT 0
                    );
                    """

        # Выполнение SQL запроса
        if c.execute(create_table_query):
            print(f'Table "accounts" was successfully installed into ({self.db_path}) data base')
        else:
            print('Table "accounts" was not installed')

        # Сохранение изменений
        conn.commit()

        # Закрытие соединения с базой данных
        conn.close()

    def update_status_accounts(self, cse_id):
        """
        Обновляет статус в колонке status в строке, соответствующей значению cse_id.

        Args:
            cse_id (str): Значение cse_id для строки, в которой нужно обновить статус.

        Returns:
            bool: True, если обновление выполнено успешно, иначе False.
        """

        conn = None

        try:
            # Подключение к базе данных SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Обновление статуса в таблице
            query = "UPDATE accounts SET status = 1 WHERE cse_id = ?"
            cursor.execute(query, cse_id)
            conn.commit()

            if cursor.rowcount > 0:
                print(f"Status updated successfully for cse_id: {cse_id}")
                conn.close()
                return True
            else:
                print(f"No rows updated for cse_id: {cse_id}")
                conn.close()
                return False

        except sqlite3.Error as e:
            print(f"Error with SQLite database: {e}")
            return False

        finally:
            if conn:
                conn.close()

    def refresh_status_accounts(self):
        """
        Сбрасывает все значения в колонке status с 1 на 0.

        Returns:
            bool: True, если обновление выполнено успешно, иначе False.
        """

        conn = None  # Инициализация переменной conn

        try:
            # Подключение к базе данных SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Обновление статуса в таблице
            cursor.execute('UPDATE "accounts" SET status = 0 WHERE status = 1')
            conn.commit()

            if cursor.rowcount > 0:
                print(f"Status reset successfully in table: accounts")
                return True
            else:
                print(f"No rows updated in table: accounts. All status == 0")
                return False

        except sqlite3.Error as e:
            print(f"Error with SQLite database: {e}")
            return False

        finally:
            if conn:
                conn.close()

    @handle_db_errors
    def init_data_base(self):
        """
        Инициализация базы данных, создание необходимых таблиц.

        Returns:
            None
        """
        self.create_table_competition_data()
        self.create_table_accounts()
        # self.create_table_queries()

    @handle_db_errors
    def insert_data_into_db(self, data_list):
        """
        Вставка данных в указанную таблицу.

        Args:
            data_list (list of dictioneries): Список кортежей с данными для вставки.

        Returns:
            None
        """
        # Подключение к базе данных
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Подготовка SQL запроса для вставки данных
        insert_query = """
        INSERT INTO CompetitionData (keyword, competition_index, competition, high_top_of_page_bid, low_top_of_page_bid) 
        VALUES (?, ?, ?, ?, ?);
        """

        # Обработка списка словарей
        for one_data in data_list:
            # Извлечение данных из каждого словаря
            keyword = one_data.get('keyword')
            competition_index = one_data.get('competition_index')
            competition = one_data.get('competition')
            high_top_of_page_bid = one_data.get('high_top_of_page_bid')
            low_top_of_page_bid = one_data.get('low_top_of_page_bid')

            # Вставка данных в базу данных
            c.execute(insert_query,
                      (keyword, competition_index, competition, high_top_of_page_bid, low_top_of_page_bid))

        # Сохранение изменений
        conn.commit()
        print(f'KeyWords data was successfully added to database: ({self.db_path})')

        # Формирование SQL-запроса для обновления данных
        sql_query = "UPDATE CompetitionData SET status = 0"
        print('All KeyWords status was successfully updated to "0"\n')

        # Выполнение SQL запроса
        c.execute(sql_query)

        # Сохранение изменений
        conn.commit()

        # Закрытие соединения с базой данных
        conn.close()

    @handle_db_errors
    def insert_accounts_into_db(self, accounts_list):
        """
        Вставка нескольких записей в таблицу accounts.

        Args:
            accounts_list (list of dict): Список словарей с данными для вставки.

        Returns:
            None
        """
        # Подключение к базе данных
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Подготовка SQL запроса для вставки данных
        insert_query = """
                INSERT INTO accounts (email, api_key, cse_id) 
                VALUES (?, ?, ?);
                """

        for one_account in accounts_list:
            email = one_account['email']
            api_key = one_account['api_key']
            cs_key = one_account['cs_key']

            # Вставка данных в базу данных
            c.execute(insert_query, (email, api_key, cs_key))

            # Сохранение изменений
            conn.commit()

        print(f'Accounts data was successfully added to database: ({self.db_path})\n')
        # Закрытие соединения с базой данных
        conn.close()

    @handle_db_errors
    def restart_db(self, data_list, accounts_list):
        """
        Удаление и повторная инициализация базы данных.

        Returns:
            None
        """
        self.delete_database()
        self.init_data_base()
        self.insert_data_into_db(data_list=data_list)
        self.insert_accounts_into_db(accounts_list=accounts_list)
        self.update_usage_dates()

    @handle_db_errors
    def update_usage_dates(self):
        """
        Обновление даты использования для указанного аккаунта.

        Returns:
            None
        """
        # Устанавливаем сегодняшнюю дату в нужном формате
        today_date = datetime.now().strftime("%Y-%m-%d")

        # Подключаемся к базе данных
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Проверяем, есть ли даты, отличные от текущей
        check_query = """
            SELECT COUNT(*) FROM accounts
            WHERE usage_date != ? OR usage_date IS NULL
            """

        cursor.execute(check_query, (today_date,))
        count = cursor.fetchone()[0]

        if count == 0:
            print("All dates in DB are up to date.\n Nothing to update.")
            cursor.close()
            conn.close()
            return

        # Обновляем данные в базе
        update_query = """
        UPDATE accounts
        SET usage_date = ?, req_limits = 100
        WHERE usage_date != ? OR usage_date IS NULL
        """

        cursor.execute(update_query, (today_date, today_date))
        print(f'usage_date updated to: {today_date}')
        print('req_limits updated to: 100')

        # Проверяем, были ли обновлены какие-либо строки
        if cursor.rowcount > 0:
            print(f"Updated {cursor.rowcount} rows.\n")
        else:
            print("No rows updated. All dates are up to date.\n")

        # Сохраняем изменения и закрываем соединение
        conn.commit()
        cursor.close()
        conn.close()

    @handle_db_errors
    def update_keyword_status(self, keyword):
        """
        Обновление статуса для указанного ключевого слова.

        Args:
            keyword (str): Ключевое слово.

        Returns:
            None
        """
        # Создание соединения с базой данных
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Формирование и выполнение SQL-запроса для обновления статуса
        sql_query = "UPDATE CompetitionData SET status = 1 WHERE keyword = ? AND status = 0"
        cursor.execute(sql_query, (keyword,))

        # Проверяем, были ли изменены какие-либо строки
        if cursor.rowcount > 0:
            print(f"Status updated for keyword '{keyword}'.")
        else:
            print(f"No rows updated for keyword '{keyword}'. Perhaps it doesn't exist or the status is not 0.")

        # Фиксация изменений
        conn.commit()

        # Закрытие соединения
        cursor.close()
        conn.close()

    @handle_db_errors
    def decrement_req_limits(self, api_key, cse_id):
        """
        Уменьшение лимита запросов для указанного аккаунта.

        Args:
            api_key (int): Идентификатор аккаунта.
            cse_id (int): Идентификатор аккаунта.

        Returns:
            None
        """
        # Подключаемся к базе данных
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Подготавливаем SQL-запрос для уменьшения значения req_limits на 1
        # только для записей, где req_limits больше 0
        update_query = """
        UPDATE accounts
        SET req_limits = req_limits - 1
        WHERE api_key = ? AND cse_id = ? AND req_limits > 0
        """
        cursor.execute(update_query, (api_key, cse_id))

        # Проверяем, были ли обновлены какие-либо строки
        if cursor.rowcount > 0:
            print(f"Decremented req_limits by 1 for api_key: {api_key}, cse_id: {cse_id}.")
        else:
            print("No rows updated. Check if api_key and cse_id are correct or if req_limits is already at zero.")

        # Сохраняем изменения и закрываем соединение
        conn.commit()
        cursor.close()
        conn.close()

    @handle_db_errors
    def get_keywords(self):
        """
        Получение списка всех ключевых слов из таблицы queries.

        Returns:
            list of str: Список ключевых слов.
        """

        # Подключение к базе данных
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Подготовка SQL запроса для поиска ключевого слова
        select_query = f"""
        SELECT keyword 
        FROM CompetitionData
        WHERE status <> 1;
        """

        # Выполнение запроса
        c.execute(select_query)

        # Получение результата
        keywords = c.fetchall()

        # Закрытие соединения
        conn.close()

        return [keyword[0] for keyword in keywords]

    @handle_db_errors
    def count_records_in_table(self, db_path, table_name):
        """
        Подсчет количества записей в указанной таблице.

        Args:
            table_name (str): Имя таблицы.
            db_path (str): Путь к базе данных.

        Returns:
            int: Количество записей.
        """
        try:
            # Подключаемся к базе данных
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            cursor.execute(f"SELECT COUNT(*) FROM '{table_name}';")

            count = cursor.fetchone()
            # print('count: ', count[0])

            # Если таблица не существует возвращаем 0
            if count is None:
                print('TYT 2')
                print(f"Table '{table_name}' does not exist.")

                # Закрываем соединение
                cursor.close()
                conn.close()
                return 0

            # Если таблица существует возвращаем колличество строк записей в таблице
            if count:
                print('TYT 3')
                # Проверяем количество записей в таблице
                # cursor.execute(f"SELECT COUNT(*) FROM '{table_name}';")
                # count = cursor.fetchone()[0]
                print(f"Number of records in table '{table_name}': {count[0]}")

                # Закрываем соединение
                cursor.close()
                conn.close()
                return count[0]

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0

        except Exception as e:
            print(f"Exception in counting records: {e}")
            return 0

    @handle_db_errors
    def check_table_exists(self, keyword):
        """
        Проверка существования указанной таблицы в базе данных.

        Args:
            keyword (str): Ключевое слово/фраза использованное для имени таблицы.

        Returns:
            bool: True, если таблица существует, иначе False.
        """
        # Подключение к базе данных
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Запрос на проверку существования таблицы
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (keyword,))

        # Проверяем результат запроса
        exists = c.fetchone()

        if exists:
            # Таблица существует
            c.close()
            conn.close()
            return True
        else:
            # Таблица не найдена
            c.close()
            conn.close()
            return False

    @handle_db_errors
    def get_list_of_tables(self):
        """
        Получение списка всех таблиц в базе данных.

        Returns:
            list of str: Список имен таблиц.
        """
        # Подключение к базе данных
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Выполнение запроса на получение списка всех таблиц
        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name NOT IN ('CompetitionData', 'sqlite_sequence', 'accounts', 'statistics');")

        # Получение всех результатов запроса
        tables = c.fetchall()

        return tables

    @handle_db_errors
    def get_index(self, query):
        """
        Получение индекса записи по URL в указанной таблице.

        Args:
            query (str): Ключевое слово/фраза для поиска нужного номера следующей страницы.

        Returns:
            int: Индекс записи.
        """

        # Подключение к базе данных
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Подготовка SQL запроса для поиска ключевого слова
        select_query = f"""
            SELECT next_page
            FROM CompetitionData 
            WHERE keyword = ?;
            """

        # Выполнение запроса
        c.execute(select_query, (query,))

        # Получение результата
        count = c.fetchone()
        print('COUNT', count)

        if count[0] is None:
            conn.close()
            return 1

        if isinstance(count[0], int):
            conn.close()
            return int(count[0])
        # if not isinstance(count[0], int):
        #     print(f'Ключевое слово: {query}')
        #     print(f'Значение ячейки "next_page" : {count[0]}')
        #     print('Если число не целое - проанализируйте причину. Число обязанно быть целым.')
        #     return False

        # Закрытие соединения
        # conn.close()
        #
        # return int(count[0])

    @handle_db_errors
    def get_page_index(self, query):
        """
        Получение индекса страницы в указанной таблице.

        Args:
            query (str): Ключевое слово/фраза для поиска нужного номера следующей страницы.

        Returns:
            int: Индекс страницы.
        """

        clean_query = query.replace('site:quora.com ', '')
        # Определение начального индекса страницы для поиска
        if self.check_table_exists(clean_query):
            start_index = self.get_index(clean_query)
            return start_index
        else:
            start_index = 1
            return start_index

    @handle_db_errors
    def get_acc_data(self):

        """
        Получение данных аккаунта по его идентификатору.
        Получаем первую строку из БД аккаунтов с наименьшим колличеством доступных запросов

        Returns:
            dict: Данные аккаунта.
        """

        # Подключение к базе данных
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Подготовка SQL запроса для поиска ключевого слова
        select_query = f"""
        SELECT * 
        FROM accounts
        WHERE req_limits > 1 AND status = 0
        ORDER BY req_limits ASC;
        """

        # Выполнение запроса
        c.execute(select_query)

        # Получение результата
        count = c.fetchone()
        # print(count)

        # Закрытие соединения
        conn.close()

        return count

    @handle_db_errors
    def get_urls_from_table(self, table_name):
        """
        Получение списка всех URL из указанной таблицы.

        Args:
            table_name (str): Имя таблицы.

        Returns:
            list of str: Список URL.
        """
        # Подключение к базе данных SQLite
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Формирование SQL запроса для извлечения данных из колонки url
        query = f"""
        SELECT url FROM "{table_name}"
        WHERE views IS NULL AND followers IS NULL
        """

        try:
            # Выполнение запроса
            cursor.execute(query)

            # Получение всех URL из колонки
            urls = cursor.fetchall()  # fetchall() возвращает список кортежей

            # Преобразование списка кортежей в список строк
            url_list = [url[0] for url in urls]  # Извлечение каждого URL из кортежа
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            url_list = []  # Возвращаем пустой список в случае ошибки

        finally:
            # Закрытие соединения с базой данных
            cursor.close()
            conn.close()

        return url_list

    @handle_db_errors
    def insert_next_page_into_db(self, next_page, query):
        """
        Вставка данных для следующей страницы в указанную таблицу.

        Args:
            next_page (int):
            query (str):

        Returns:
            None
        """
        clean_query = query.replace('site:quora.com ', '')

        # Подключение к базе данных
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Подготовка SQL запроса для вставки данных
        insert_query = '''
        UPDATE CompetitionData 
        SET next_page = ? 
        WHERE keyword = ?;
        '''

        print(f'Следующая страница: {next_page}')
        print(f'Ключевое слово: {clean_query}')
        # Вставка данных в базу данных
        c.execute(insert_query, (next_page, clean_query))
        print('Данные следующей страницы ключевого слова добавленно в базу данных')

        # Сохранение изменений
        conn.commit()

        # Закрытие соединения с базой данных
        conn.close()

    @handle_db_errors
    def update_followers_and_views(self, table_name, data, url):
        """
        Обновление количества подписчиков и просмотров для записи по URL в указанной таблице.

        Args:
            table_name (str): Имя таблицы.
            url (str): URL записи.
            data (dict): словарь с данными о followers и view

        Returns:
            None
        """
        followers_number = data.get('followers')
        view_number = data.get('view')

        if followers_number is None or view_number is None:
            print("Invalid data: 'followers' and 'view' must be present in the dictionary")
            return

        try:
            # Подключаемся к базе данных
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Проверяем, существует ли таблица
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            if cursor.fetchone() is None:
                print(f"Table '{table_name}' does not exist.")
                return

            # Обновляем данные в таблице
            update_query = f"""
            UPDATE '{table_name}'
            SET followers = ?, views = ?
            WHERE url = ?;
            """
            cursor.execute(update_query, (followers_number, view_number, url))

            # Проверяем, были ли обновлены какие-либо строки
            if cursor.rowcount > 0:
                print(f"Updated {cursor.rowcount} (followers_number and view_number) rows in table '{table_name}'.")
            else:
                print("No rows updated. Check if the URL exists in the table.")

            # Сохраняем изменения и закрываем соединение
            conn.commit()
            cursor.close()
            conn.close()

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in updating records: {e}")

    def update_answers_and_related_answers(self, table_name, data, url):

        answers_number = data.get('answers')
        related_answers_number = data.get('related_answers')

        if answers_number is None or related_answers_number is None:
            print("Invalid data: 'followers' and 'view' must be present in the dictionary")
            print(
                '--------------------------------------------------------------------------------------------------------------')
            return

        try:
            # Подключаемся к базе данных
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Проверяем, существует ли таблица
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            if cursor.fetchone() is None:
                print(f"Table '{table_name}' does not exist.")
                return

            # Обновляем данные в таблице
            update_query = f"""
            UPDATE '{table_name}'
            SET answers = ?, related_answers = ?
            WHERE url = ?;
            """
            cursor.execute(update_query, (answers_number, related_answers_number, url))

            # Проверяем, были ли обновлены какие-либо строки
            if cursor.rowcount > 0:
                print(f"Updated {cursor.rowcount} (answers_number, related_answers_number) rows in table '{table_name}'.")
                print('--------------------------------------------------------------------------------------------------------------')
            else:
                print("No rows updated. Check if the URL exists in the table.")
                print('--------------------------------------------------------------------------------------------------------------')


            # Сохраняем изменения и закрываем соединение
            conn.commit()
            cursor.close()
            conn.close()

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in updating records: {e}")

    @handle_db_errors
    def process_query_data(self, data, query):
        """
        Функция для вставки данных в базу данных.

        Аргументы:
        data (list): Список словарей с данными для вставки.
        Query (str): Поисковый запрос.

        Возвращает:
        None
        """
        clean_query = query.replace('site:quora.com ', '')

        # Создаем базу данных для этого ключевого слова
        self.__create_keyword_table__(clean_query)

        # Подключение к базе данных
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Подготовка SQL запроса для вставки данных
        insert_query = f"""
            INSERT OR IGNORE INTO '{clean_query}' (title, url, date, key_word) 
            VALUES (?, ?, ?, ?);
            """

        # Обработка списка словарей
        for one_data in data:
            # Извлечение данных из каждого словаря
            title = one_data['title']
            link = one_data['link']
            date = one_data['date']
            qu = query.replace('site:quora.com ', '')

            # Вставка данных в базу данных
            c.execute(insert_query, (title, link, date, qu))

        # Сохранение изменений
        conn.commit()

        # Закрытие соединения с базой данных
        conn.close()
