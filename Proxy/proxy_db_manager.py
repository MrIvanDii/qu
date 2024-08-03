import sqlite3
import os


class ProxyDBmanager:

    def __init__(self):
        self.db_path = '/Users/martinanikola/PycharmProjects/PropshtScrapping_V2/Proxy/proxies.db'
        pass

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

    def create_table_proxies(self):

        # Подключение к базе данных (или создание, если она не существует)
        conn = sqlite3.connect(self.db_path)

        # Создание курсора для выполнения SQL команд
        c = conn.cursor()

        # SQL запрос на создание таблицы
        create_table_query = """
                    CREATE TABLE IF NOT EXISTS proxies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ip TEXT,
                        Port INT,
                        format TEXT,
                        country TEXT,
                        work_status INT DEFAULT 1,
                        using_status INT DEFAULT 0,
                        UNIQUE(ip, port)
                    );
                    """
        # Выполнение SQL запроса
        if c.execute(create_table_query):
            print(f'Table "proxies" was successfully installed into ({self.db_path}) data base')
        else:
            print('Table "proxies" was not installed')


# if __name__ == "__main__":
#     db_test = ProxyDBmanager()
#     db_test.create_table_proxies()