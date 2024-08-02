import sqlite3
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogSheetsTransfer:

    def __init__(self, db_pth):
        self.db_path = db_pth
        self.json_file = '/Users/martinanikola/PycharmProjects/PropshtScrapping_V2/DB/propsht-project-e18f3d3ccd44.json'
        self.google_sheet_name = input("Input google sheet name: ")
        self.email = 'ivanodessadii@gmail.com'

    def combine_tables_and_upload_to_google_sheets(self):
        # Шаг 1: Подключение к базе данных SQLite
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Шаг 2: Получение списка названий таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT IN ('CompetitionData', 'sqlite_sequence', 'accounts', 'statistics');")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]

        # Шаг 3: Объединение всех таблиц в одну
        combined_df = pd.DataFrame()
        for table in table_names:
            df = pd.read_sql_query(f"SELECT * FROM '{table}'", conn)
            # print(df)
            if not df.empty:
                combined_df = pd.concat([combined_df, df], ignore_index=True)
            # print()
            # print('------------')
            # print()
            # print(combined_df)

        conn.close()

        # Обработка значений NaN, inf и -inf
        combined_df = combined_df.replace({float('nan'): None, float('inf'): None, -float('inf'): None})

        # Шаг 4: Подготовка к аутентификации и подключению к Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.json_file, scope)
        # print(credentials)
        client = gspread.authorize(credentials)
        # print(client)

        # Шаг 5: Создание новой Google Sheets и загрузка данных
        goog_sheet_name = self.google_sheet_name
        spreadsheet = client.create(title=goog_sheet_name)
        sheet = spreadsheet.get_worksheet(0)
        # print(sheet)
        sheet.update([combined_df.columns.values.tolist()] + combined_df.values.tolist())

        # Предоставление доступа пользователю
        spreadsheet.share(self.email, perm_type='user', role='writer')
        print('Данные транспортированны успешно')
        print('URL Google-таблицы: ', spreadsheet.url)

        print(f"Data has been successfully uploaded to Google Sheets: {goog_sheet_name}")

