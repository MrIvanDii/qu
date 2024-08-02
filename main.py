from facade import FacadeAPI
from DB.data_cassino import data as australia_data
from DB.data import data as qu_data


# from google_api.search import GoogleSearch
# from google_api.google_transfer import GoogSheetsTransfer
# from data.database import DatabaseManager
# from DB.data import data as dict_data
# from DB.data import accounts
# from DB.australia_data import data
# from utils.parser import HTMLParser
# import time
# import random
#
#
# def db_get_list_tables(db_pth):
#     db_manager = DatabaseManager(db_path=db_pth)
#     tables = db_manager.get_list_of_tables()
#     return tables
#
#
# def transfer_data_from_db_into_sheets(db_pth):
#     question = input('Перенести данные из БД в Goog-таблицу?: y/n ')
#     if question == 'y':
#         goog_sheet_manager = GoogSheetsTransfer(db_pth=db_pth)
#         goog_sheet_manager.combine_tables_and_upload_to_google_sheets()
#
#
# def keywords_processing(db_pth):
#     question = input('Выполнить обработку ключевых фраз? y/n: ')
#     if question == 'y':
#
#         # Получаем список ключевых фраз для обработки
#         querys = db_get_querys(db_pth=db_pth)
#
#         # Проходим циклом по каждому ключевому слову для сбора данных
#         for one_query in querys:
#             google_request = 'site:quora.com ' + one_query
#             google_collect_data(db_pth=db_pth, goog_req=google_request)
#
#
# def db_refresh_all_data_except_accounts(db_pth):
#     untouchebl_tables = ['accounts', 'sqlite_sequence']
#     db_manager = DatabaseManager(db_path=db_pth)
#     list_of_tables = db_get_list_tables(db_pth)
#     print(list_of_tables)
#
#     removed_tables = []
#     for table in list_of_tables:
#         clear_table_name = table[0]
#         if clear_table_name in untouchebl_tables:
#             continue
#         elif clear_table_name not in list_of_tables:
#             print(clear_table_name)
#             removed_tables.append(clear_table_name)
#             db_manager.remove_table(clear_table_name)
#
#     print(f'Removed tables: {removed_tables}')
#
#     db_manager.create_table_competition_data()
#     db_manager.insert_data_into_db(data_list=data)
#
#
# def db_add_data_from_list(db_pth):
#     db_manager = DatabaseManager(db_path=db_pth)
#     db_manager.insert_keywords_to_db(table_name='CompetitionData', column_name='keyword', keywords=data)
#
#
# def db_add_data_dict(db_pth):
#     question = input('Добавить ключевые фразы в базу данных? y/n: ')
#     if question == 'y':
#         db_manager = DatabaseManager(db_path=db_pth)
#         db_manager.insert_data_into_db(data_list=dict_data)
#
#
# def db_add_accounts_into_db(db_pth, acc_data):
#     question = input('Добавить данные из списка словарей в БД? y/n: ')
#     if question == 'y':
#         db_manager = DatabaseManager(db_path=db_pth)
#         db_manager.insert_accounts_into_db(accounts_list=acc_data)
#     if question == 'n':
#         return
#
#
# def db_data_checks(db_pth):
#     db_manager = DatabaseManager(db_path=db_pth)
#     db_manager.update_usage_dates()
#
#
# def db_check(db_pth):
#     db_manager = DatabaseManager(db_path=db_pth)
#
#     if not db_manager.check_database_exists():
#         question = input('Создать базу данных? y/n')
#         if question == 'y':
#             db_manager.init_data_base()
#         if question == 'n':
#             print('База данных не создалась')
#     if db_manager.check_database_exists():
#         print('Data Base file found saccesfully')
#
#
# def db_get_querys(db_pth):
#     db_manager = DatabaseManager(db_path=db_pth)
#     querys_list = db_manager.get_keywords()
#     return querys_list
#
#
# def google_collect_data(db_pth, goog_req):
#     goog_manager = GoogleSearch(db_path=db_pth)
#     goog_manager.google_search_all_results(goog_req)
#
#
# def automated_html_data_collectio(db_pth):
#     db_manager = DatabaseManager(db_path=db_pth)
#     html_p = HTMLParser(db_path=db_pth)
#
#     # Генерируем список имен таблиц которые есть в БД
#     tables_list = db_manager.get_list_of_tables()
#     print(tables_list)
#
#     # Проходим по каждому имени таблицы
#     for one_table in tables_list:
#         print(one_table[0])
#         # Получить список url из каждой таблицы, которые нобходимо обработать
#         list_of_url = db_manager.get_urls_from_table(table_name=one_table[0])
#
#         # Пройти циклом по каждой из url
#         for one_url in list_of_url:
#             # Ждем 1-2 секунды чтоб не грузить сервер Кворы
#             sec = random.randint(1, 2)
#             print('sec to wait: ', sec)
#             time.sleep(sec)
#
#             # Получить followers и view с HTML страницы вызванной из полученной url + \log
#             folow_views_dict = html_p.fetch_followers_and_view_count(url=one_url)
#
#             # Добавить полученные данные о followers и views в базу данных
#             db_manager.update_followers_and_views(table_name=one_table[0], data=folow_views_dict, url=one_url)
#
#             # Получить answers и related_answers с HTML страницы вызванной из полученной url
#             answers_and_related_answers = html_p.fetch_answers_and_related_answers(url=one_url)
#
#             # Добавить полученные данные о answers и related_answers в базу данных
#             db_manager.update_answers_and_related_answers(table_name=one_table[0], data=answers_and_related_answers,
#                                                           url=one_url)
#
#
# def get_answers(db_pth, ur_l):
#     html_p = HTMLParser(db_path=db_pth)
#     return html_p.fetch_answers_and_related_answers(url=ur_l)
#

def main(db_pth, data_list, results_per_req=None):
    """
    Функция должна принимать три параметра:
    - Название проекта
    - Путь к БД проекта
    - Путь к файлу с исходными данными проекта
    - Ограничитель результатов
    """
    api_manager = FacadeAPI()
    accounts = api_manager.accounts

    # # Проверка наличия базы данных
    # # Если базы данных нет - мы ее создаем
    # api_manager.db_check(db_pth=db_pth)
    #
    # # Добавляем аккаунты в базу данных
    # # Нужно добавить логику которая будет проверять наличие аккаунтов в БД
    # # И если аккаунты уже есть в БД - пропускать повторное добавление
    # api_manager.db_add_accounts_into_db(db_pth=db_pth, acc_data=accounts)
    #
    # # Обновляем информацию о колличестве возможных запросов по каждому аккаунту
    # # Обновляем данные об актуальной дате и запросах
    # api_manager.db_data_checks(db_pth=db_pth)
    #
    # # Заполняем базу данных ключевыми фразами из списка
    # api_manager.db_add_data_dict(db_pth=db_pth, data_list=data_list)
    #
    # # Получаем список ключевых фраз для обработки
    # # Проходим циклом по каждому ключевому слову для сбора данных
    # api_manager.keywords_processing(db_pth=db_pth, results_per_req=results_per_req)

    # Автоматически проходим по всем url и собираем данные
    # Тут можно разместить процесс поддтверждения действия у пользователя
    # Типа:
    # "Вы хотите запустить автоматический процесс сбора данных о views и followers каждой страницы? y/n"
    api_manager.automated_html_data_collectio(db_pth=db_pth)

    # Формируем гугл-таблицу
    # Перед созданием гугл-таблицы можно запросить имя гугл-файла
    api_manager.transfer_data_from_db_into_sheets(db_pth=db_pth)


if __name__ == "__main__":
    casino_db_path = '/Users/martinanikola/PycharmProjects/PropshtScrapping_V2/DB/australia_online_casinos.db'
    quora_db_path = '/Users/martinanikola/PycharmProjects/PropshtScrapping_V2/DB/quora_stat.db'

    cassino_data = australia_data
    quora_data = qu_data

    # main(db_pth=quora_db_path, data_list=qu_data, results_per_req=20)
    main(db_pth=casino_db_path, data_list=cassino_data, results_per_req=100)
