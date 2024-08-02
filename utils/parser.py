import re
from bs4 import BeautifulSoup
# import requests
# from fake_useragent import UserAgent
# from requests_html import HTMLSession
from sel_drive.driver_bot import GoogDrive


class HTMLParser:

    def __init__(self, db_path):
        self.db_path = db_path
        self.view_followers_path = '/Users/martinanikola/PycharmProjects/PropshtScrapping_V2/HTML_examples/view_followers/'
        self.answers_related_path = '/Users/martinanikola/PycharmProjects/PropshtScrapping_V2/HTML_examples/answers_related_ans/'

    def get_proxya(self, dict_element):
        proxy_username = dict_element["username"]
        proxy_password = dict_element["password"]
        proxy_ip = dict_element["ip"]
        proxy_port = dict_element["port"]

        prox = f'socks5://{proxy_username}:{proxy_password}@{proxy_ip}:{proxy_port}/'

        return {"http": prox,
                "https": prox}

    def get_proxya_for_selen(self, dict_element):
        proxy_username = dict_element["username"]
        proxy_password = dict_element["password"]
        proxy_ip = dict_element["ip"]
        proxy_port = dict_element["port"]

        prox = f'socks5://{proxy_username}:{proxy_password}@{proxy_ip}:{proxy_port}/'

        return prox

    # def fetch_followers_and_view_count(self, url, prox):
    #     # Корректируем URL
    #     url = url + '/log'
    #     print('LOG URL', url)
    #
    #     ua = UserAgent()
    #     headers = {
    #         "User-Agent": ua.random,
    #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    #         "Accept-Language": "en-US,en;q=0.5",
    #         "Upgrade-Insecure-Requests": "1"
    #     }
    #
    #     # Загружаем HTML-страницу
    #     response = requests.get(url, headers=headers, proxies=prox)
    #     html = response.text
    #     # print(html)
    #
    #     # Парсинг HTML
    #     soup = str(BeautifulSoup(html, 'html.parser'))
    #     # text = soup.get_text()  # Извлечение всего текста без HTML тегов
    #
    #     followers_number = self.__get_followers_info__(data=soup)
    #     view_number = self.__get_views_info__(data=soup)
    #
    #     return {'followers': followers_number, 'view': view_number}

    def fetch_followers_and_view_count(self, url, prox):
        # Корректируем URL
        url = url + '/log'
        print('LOG URL', url)

        # ua = UserAgent()
        # session = HTMLSession()
        goog_driver = GoogDrive(proxy=prox)

        # headers = {
        #     "User-Agent": ua.random,
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        #     "Accept-Language": "en-US,en;q=0.5",
        #     "Upgrade-Insecure-Requests": "1"
        # }

        # Загружаем HTML-страницу
        # response = session.get(url, headers=headers, proxies=prox)
        # html = response.html.html
        # print(html)
        # html = goog_driver.get_page_src_no_proxy(page_url=url)
        html = goog_driver.get_page_source(page_url=url)

        # Парсинг HTML
        soup = str(BeautifulSoup(html, 'html.parser'))
        # text = soup.get_text()  # Извлечение всего текста без HTML тегов

        followers_number = self.__get_followers_info__(data=soup)
        view_number = self.__get_views_info__(data=soup)

        # if followers_number is None and view_number is None:
        #     pass

        if followers_number is None and view_number is None:
            file_name = url.split('/')
            with open(f'{self.view_followers_path}{file_name[-2]}.html', 'w') as file:
                file.write(html)
                print()
                print('[INFO] Создан HTML-файл для дальнейшей проверки')

        return {'followers': followers_number, 'view': view_number}

    # def fetch_answers_and_related_answers(self, url, prox):
    #
    #     ua = UserAgent()
    #     headers = {
    #         "User-Agent": ua.random,
    #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    #         "Accept-Encoding": "gzip, deflate, br",
    #         "Accept-Language": "en-US,en;q=0.5",
    #         "Upgrade-Insecure-Requests": "1"
    #     }
    #
    #     # Загружаем HTML-страницу
    #     response = requests.get(url, headers=headers, proxies=prox)
    #     html = response.text
    #
    #     # Парсинг HTML
    #     soup = str(BeautifulSoup(html, 'html.parser'))
    #
    #     answers = self.__get_answers_info__(data=soup)
    #     related_answers = self.__get_related_answers_info__(data=soup)
    #
    #     return {'answers': answers, 'related_answers': related_answers}

    def fetch_answers_and_related_answers(self, url, prox):

        # ua = UserAgent()
        # session = HTMLSession()
        goog_driver = GoogDrive(proxy=prox)

        # headers = {
        #     "User-Agent": ua.random,
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        #     "Accept-Encoding": "gzip, deflate, br",
        #     "Accept-Language": "en-US,en;q=0.5",
        #     "Upgrade-Insecure-Requests": "1"
        # }

        # Загружаем HTML-страницу
        # response = session.get(url, headers=headers, proxies=prox)
        # html = response.html.html
        html = goog_driver.get_page_src_no_proxy(page_url=url)

        # Парсинг HTML
        soup = str(BeautifulSoup(html, 'html.parser'))

        answers = self.__get_answers_info__(data=soup)
        related_answers = self.__get_related_answers_info__(data=soup)

        if answers is None and related_answers is None:
            file_name = url.split('/')
            with open(f'{self.answers_related_path}{file_name[-1]}.html', 'w') as file:
                file.write(html)
                print()
                print('[INFO] Создан HTML-файл для дальнейшей проверки')

        return {'answers': answers, 'related_answers': related_answers}

    def __get_answers_info__(self, data):

        # Данный паттерн необходимо добавить в обработку и отловку по нему данных
        # answers_pattern_2 = r'numAnswers["\\:\s]*(\d+)'
        answers_pattern_2 = r'numAnswers\s*["\\:\s]*\s*(\d+)'

        # Используем регулярное выражение для поиска "decanonicalizedAnswerCount":<number>
        answers_match_2 = re.search(answers_pattern_2, data)

        # Паттерны регулярного выражения
        # answers_pattern = r'decanonicalizedAnswerCount["\\:\s]*(\d+)'
        answers_pattern = r'decanonicalizedAnswerCount\s*["\\:\s]*\s*(\d+)'

        # Используем регулярное выражение для поиска "decanonicalizedAnswerCount":<number>
        answers_match = re.search(answers_pattern, data)

        answers_match_number = None

        if answers_match:
            answers_match_number = int(answers_match.group(1))
            # Возвращаем количество ответов как целое число
        elif not answers_match:
            if answers_match_2:
                answers_match_number = int(answers_match_2.group(1))
                print('Найдено совпадение по второму паттерну')
        else:
            print('Number of answers not found')

        return answers_match_number

    def __get_related_answers_info__(self, data):
        # Паттерны регулярного выражения
        related_answers_pattern = r'mixRankedAnswersCount["\\:\s]*(\d+)'

        # Используем регулярное выражение для поиска "followerCount":<number>
        related_answers_match = re.search(related_answers_pattern, data)

        related_answers_number = None

        if related_answers_match:
            related_answers_number = int(related_answers_match.group(1))
            # Возвращаем количество подписчиков как целое число
        else:
            # Если не нашли, возвращаем None
            print('Number of answers not found')

        return related_answers_number

    def __get_followers_info__(self, data):
        # Паттерны регулярного выражения
        followers_pattern = r'\bfollowerCount\b["\\:\s]*(\d+)'

        # Используем регулярное выражение для поиска "followerCount":<number>
        followers_match = re.search(followers_pattern, data)

        followers_number = None

        if followers_match:
            followers_number = int(followers_match.group(1))
            # Возвращаем количество подписчиков как целое число
        else:
            # Если не нашли, возвращаем None
            print('Number of followers not found')

        return followers_number

    def __get_views_info__(self, data):

        # Паттерны регулярного выражения
        view_pattern = r'\bviewCount\b["\\:\s]*(\d+)'

        # Используем регулярное выражение для поиска "followerCount":<number>
        view_match = re.search(view_pattern, data)

        view_number = None

        if view_match:
            view_number = int(view_match.group(1))
        else:
            print('Number of views not found')

        return view_number
