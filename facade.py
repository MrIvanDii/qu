from google_api.search import GoogleSearch
from DB.data import list_of_proxies_2 as list_of_proxies
from google_api.google_transfer import GoogSheetsTransfer
from data.database import DatabaseManager
from DB.data import accounts
from DB.australia_data import data
from utils.parser import HTMLParser
import time
import random
from Proxy.main_proxy import ProxyFilter


class FacadeAPI:

    def __init__(self):
        self.accounts = accounts
        self.ignore_urls = ['https://www.quora.com/profile/Susan-Hadlow', 'https://miesrosq.quora.com/No-Deposit-Slots?ch=15&oid=5293328&share=bfccd5fc&target_type=post']

    def db_get_list_tables(self, db_pth):
        db_manager = DatabaseManager(db_path=db_pth)
        tables = db_manager.get_list_of_tables()
        return tables

    def transfer_data_from_db_into_sheets(self, db_pth):
        question = input('Перенести данные из БД в Goog-таблицу?: y/n ')
        if question == 'y':
            goog_sheet_manager = GoogSheetsTransfer(db_pth=db_pth)
            goog_sheet_manager.combine_tables_and_upload_to_google_sheets()

    def keywords_processing(self, db_pth, results_per_req=None):
        question = input('Выполнить обработку ключевых фраз? y/n: ')
        if question == 'y':

            # Получаем список ключевых фраз для обработки
            querys = self.db_get_querys(db_pth=db_pth)

            # Проходим циклом по каждому ключевому слову для сбора данных
            for one_query in querys:
                google_request = 'site:quora.com ' + one_query
                self.google_collect_data(db_pth=db_pth, goog_req=google_request, results_per_req=results_per_req)

    def db_refresh_all_data_except_accounts(self, db_pth):
        untouchebl_tables = ['accounts', 'sqlite_sequence']
        db_manager = DatabaseManager(db_path=db_pth)
        list_of_tables = self.db_get_list_tables(db_pth)
        print(list_of_tables)

        removed_tables = []
        for table in list_of_tables:
            clear_table_name = table[0]
            if clear_table_name in untouchebl_tables:
                continue
            elif clear_table_name not in list_of_tables:
                print(clear_table_name)
                removed_tables.append(clear_table_name)
                db_manager.remove_table(clear_table_name)

        print(f'Removed tables: {removed_tables}')

        db_manager.create_table_competition_data()
        db_manager.insert_data_into_db(data_list=data)

    def db_add_data_from_list(self, db_pth):
        db_manager = DatabaseManager(db_path=db_pth)
        db_manager.insert_keywords_to_db(table_name='CompetitionData', column_name='keyword', keywords=data)

    def db_add_data_dict(self, db_pth, data_list):
        question = input('Добавить ключевые фразы в базу данных? y/n: ')
        if question == 'y':
            db_manager = DatabaseManager(db_path=db_pth)
            db_manager.insert_data_into_db(data_list=data_list)

    def db_add_accounts_into_db(self, db_pth, acc_data):
        question = input('Добавить данные из списка словарей в БД? y/n: ')
        if question == 'y':
            db_manager = DatabaseManager(db_path=db_pth)
            db_manager.insert_accounts_into_db(accounts_list=acc_data)
        if question == 'n':
            return

    def db_data_checks(self, db_pth):
        db_manager = DatabaseManager(db_path=db_pth)
        db_manager.update_usage_dates()
        db_manager.refresh_status_accounts()

    def db_check(self, db_pth):
        db_manager = DatabaseManager(db_path=db_pth)

        if not db_manager.check_database_exists():
            question = input('Создать базу данных? y/n')
            if question == 'y':
                db_manager.init_data_base()
            if question == 'n':
                print('База данных не создалась')
        if db_manager.check_database_exists():
            print('Data Base file found saccesfully')

    def db_get_querys(self, db_pth):
        db_manager = DatabaseManager(db_path=db_pth)
        querys_list = db_manager.get_keywords()
        return querys_list

    def google_collect_data(self, db_pth, goog_req, results_per_req=None):
        goog_manager = GoogleSearch(db_path=db_pth)
        goog_manager.google_search_all_results(goog_req, num_results=results_per_req)

    def automated_html_data_collectio(self, db_pth):
        question = input('Запустить сбор данных с HTML-страниц? y/n: ')
        if question == 'y':
            db_manager = DatabaseManager(db_path=db_pth)
            html_p = HTMLParser(db_path=db_pth)
            prox_manager = ProxyFilter()
            # proxies_list = list_of_proxies
            proxies_list = prox_manager.check_proxies(list_of_proxies)

            # Генерируем список имен таблиц которые есть в БД
            tables_list = db_manager.get_list_of_tables()
            # print(tables_list)

            # Считаем количество отправленных запросов, чтоб понимать лимит кворы
            req_count = 1

            # Проходим по каждому имени таблицы
            for one_table in tables_list:

                # proxya = random.choice(proxies_list)
                # proxies = html_p.get_proxya(proxya)
                # print('Используем проксю: ', proxies)
                # print()

                # Получить список url из каждой таблицы, которые нобходимо обработать
                list_of_url = db_manager.get_urls_from_table(table_name=one_table[0])
                if len(list_of_url) == 0:
                    print(f'Table: {one_table} doesnt have free URL')

                # print(one_table)
                # print(list_of_url)

                # Пройти циклом по каждой из url
                for one_url in list_of_url:

                    if one_url in self.ignore_urls:
                        print(f'Пропускаем {one_url}')
                        continue

                    proxya = random.choice(proxies_list)
                    proxies = html_p.get_proxya(proxya)

                    print()
                    print(f'REQUESTS: {req_count}')
                    # print('Используем проксю: ', proxies)
                    print()
                    # Ждем 1-2 секунды чтоб не грузить сервер Кворы
                    sec = random.randint(3, 7)
                    print('sec to wait: ', sec)
                    time.sleep(sec)

                    # Получить followers и view с HTML страницы вызванной из полученной url + \log
                    folow_views_dict = html_p.fetch_followers_and_view_count(url=one_url, prox=proxies)
                    print(f'Followers and views :  {folow_views_dict}')

                    # Добавить полученные данные о followers и views в базу данных
                    db_manager.update_followers_and_views(table_name=one_table[0], data=folow_views_dict, url=one_url)

                    # Ждем 1-2 секунды чтоб не грузить сервер Кворы
                    sec = random.randint(3, 7)
                    print('sec to wait: ', sec)
                    print()
                    time.sleep(sec)

                    print('URL: ', one_url)
                    # Получить answers и related_answers с HTML страницы вызванной из полученной url
                    answers_and_related_answers = html_p.fetch_answers_and_related_answers(url=one_url, prox=proxies)
                    print(f'Answers and related answers: {answers_and_related_answers}')

                    # Добавить полученные данные о answers и related_answers в базу данных
                    db_manager.update_answers_and_related_answers(table_name=one_table[0], data=answers_and_related_answers,
                                                                  url=one_url)
                    req_count += 2

    # def get_answers(self, db_pth, ur_l):
    #     html_p = HTMLParser(db_path=db_pth)
    #     return html_p.fetch_answers_and_related_answers(url=ur_l)
