import requests
from data.database import DatabaseManager
import json
import time


class GoogleSearch:

    def __init__(self, db_path):
        self.db_path = db_path
        self.db_manager = DatabaseManager(db_path=db_path)

    def create_query(self, keyword):
        return 'site:quora.com ' + keyword

    def search(self, query, page, api_key, cse_id):
        # Инициализируем start_index перед отправкой запроса
        start_index = None

        # Список для сохранения данных ответов
        data = []

        # URL для Google Custom Search JSON API
        url = "https://www.googleapis.com/customsearch/v1"

        # Параметры запроса
        params = {
            'key': api_key,
            'cx': cse_id,
            'q': query,
            'start': page
        }

        # Отправка запроса
        response = requests.get(url, params=params)
        search_results = response.json()
        print(json.dumps(search_results, indent=4, ensure_ascii=False))

        # Уменьшаем колличество доступных запросов в аккаунте
        self.db_manager.decrement_req_limits(api_key=api_key, cse_id=cse_id)

        # Обработка ответа
        if response.status_code == 200:

            # Проверяю наличие блока с информацией в полученом JSON ответе
            if 'items' in search_results:
                # Обробатыва информацию
                for item in search_results['items']:
                    if 'htmlSnippet' in item:
                        title = item['title'].replace(' - Quora', '')
                        link = item['link']
                        date = item['htmlSnippet'].split('<b>')[0].replace(',', '')
                        data.append({'title': title, 'link': link, 'date': date})

                    elif 'htmlSnippet' not in item:
                        print('РЕКЛАМНЫЙ БЛОК')
                        print('*_*_*_*_**_*_*_*_*_*_*_*_*_**_*_*_*_**_*_*_*_**_*_*_*_*')
                        print(item)

                    else:
                        print('Не предвиденная ошибка в файле serach.py')
                        print('Строка 59')
                        print('что-то не так с htmlSnippet')

            if 'nextPage' in search_results['queries']:
                start_index = search_results['queries']['nextPage'][0]['startIndex']
            elif 'nextPage' not in search_results['queries']:
                start_index = None

            return data, start_index

        # Обработка ответа 400 - привышено количество доступных результатов в Google
        if response.status_code == 400:
            # Извлекаем из гугл-запроса только ключевое слово
            clean_query = query.replace("site:quora.com ", "")

            # Обновляем статус ключевого слово с 0 на 1
            # Тоесть с "необработано" на "обработано"
            self.db_manager.update_keyword_status(clean_query)
            print(f'Достигнут лимит результатов п оключевому слову: {clean_query}')

            # Обновляем статус аккаунта
            self.db_manager.update_status_accounts(cse_id=cse_id)
            return search_results, None

        elif response.status_code == 429:
            print('Достигнут лимит запросов с аккаунта')
            return search_results, None

    def google_search_all_results(self, query, num_results=20):
        print(f'Запрос : {query}')

        # Извлекаем из гугл-запроса только ключевое слово
        clean_query = query.replace("site:quora.com ", "")
        print(f'Ключевое слово:{clean_query}')

        # Создаем таблицу в БД
        self.db_manager.__create_keyword_table__(keyword_query=clean_query)

        # Счетчик колличества необходимых результатов, которые осталось добавить в БД
        records_left = num_results - self.db_manager.count_records_in_table(db_path=self.db_path,
                                                                            table_name=clean_query)
        print('records_left: ', records_left)
        while records_left > 0:

            # Определение начального индекса страницы для поиска
            start_index = self.db_manager.get_page_index(query=query)
            print('query: ', query)
            print('start_index: ', start_index)

            time.sleep(3)

            # Получение данных аккаунтов
            account = self.db_manager.get_acc_data()
            print(f'Используем данные аккаунта: {account}')
            acc_api_key = account[2]
            acc_cse_id = account[3]

            try:
                # Выполнение поиска в Google
                data, next_page = self.search(query=query, page=start_index, api_key=acc_api_key, cse_id=acc_cse_id)
                print(f'Страница №: {start_index}')
                print(f'Собранно  {len(data)}  результатов')

                # Вставка следующей страницы в базу данных
                if next_page is not None:
                    self.db_manager.insert_next_page_into_db(next_page=next_page, query=query)

                elif next_page is None:
                    print(f'Достигнут лимит доступных гугл-результатов по запросу: "{clean_query}"')
                    break

                # Обновление начального индекса для следующей страницы
                start_index = next_page

                # Вставка данных в базу данных
                self.db_manager.process_query_data(data=data, query=query)
                print(f'Данные добавленны в базу данных')

                records_left = num_results - self.db_manager.count_records_in_table(db_path=self.db_path,
                                                                                    table_name=clean_query)

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 400:
                    print("Ошибка во время поиска: 400. Достигнут лимит запросов.")
                    break  # Прекращение цикла, если возникает ошибка 400

                elif e.response.status_code == 429:
                    print('Достигнут лимит запросов с аккаунта')
                    break
