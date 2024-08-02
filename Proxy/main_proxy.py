import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import base64
# from DB.data import list_of_proxies


class ProxyFilter:

    def __init__(self):
        self.countries = ['']
        self.url_freeproxy = 'https://advanced.name/freeproxy'
        self.url_freeproxy_country = 'https://advanced.name/freeproxy?country='

    def get_proxies(self):
        pass

    def check_proxies(self, prox_list):
        print('Preparing proxies to work...')

        new_prox_list = []

        for one_proxya in prox_list:
            proxy_username = one_proxya["username"]
            proxy_password = one_proxya["password"]
            proxy_ip = one_proxya["ip"]
            proxy_port = one_proxya["port"]

            proxies = {
                "http": "socks5://{0}:{1}@{2}:{3}/".format(proxy_username, proxy_password, proxy_ip, proxy_port),
                "https": "socks5h://{0}:{1}@{2}:{3}/".format(proxy_username, proxy_password, proxy_ip, proxy_port)
            }

            try:
                response = requests.get("https://api.infoip.io/", proxies=proxies, timeout=5)
                print(response.status_code)
                if response.status_code == 200:
                    new_prox_list.append(one_proxya)
                print()
            except Exception as _ex:
                print(f'PROX: {proxies}')
                print('FAILED')
                print(_ex)
                print()
        print(f'Prepared {len(new_prox_list)} proxies...')

        # print(new_prox_list)
        return new_prox_list

    def check_http_proxies(self, prox_list):
        print('Preparing proxies to work...')

        new_prox_list = []

        for one_proxya in prox_list:
            proxy_username = one_proxya["username"]
            proxy_password = one_proxya["password"]
            proxy_ip = one_proxya["ip"]
            proxy_port = one_proxya["port"]

            proxies = {
                "http": "https://{0}:{1}@{2}:{3}/".format(proxy_username, proxy_password, proxy_ip, proxy_port)
            }

            try:
                response = requests.get("https://api.infoip.io/", proxies=proxies, timeout=5)
                print(response.status_code)
                if response.status_code == 200:
                    new_prox_list.append(proxies["http"])
                print()
            except Exception as _ex:
                print(f'PROX: {proxies}')
                print('FAILED')
                print(_ex)
                print()
        print(f'Prepared {len(new_prox_list)} proxies...')

        # print(new_prox_list)
        return new_prox_list

    def get_proxya(self, prox_list):
        pass

    def pars_proxies(self):
        pass

    def decode_base64(self, data):
        """Декодирует Base64 строку."""
        decoded_bytes = base64.b64decode(data)
        decoded_str = decoded_bytes.decode('utf-8')
        return decoded_str

    def get_locations_values(self):
        ua = UserAgent()
        headers = {
            "User-Agent": ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Upgrade-Insecure-Requests": "1"
        }

        # Загружаем HTML-страницу
        response = requests.get(self.url_freeproxy, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        country_values = []

        # Найти элемент select с классом form-control input-sm
        select_elements = soup.find_all('select', class_='form-control input-sm')
        # print(select_elements)

        # Найти нужный select элемент, содержащий аббревиатуры стран (второй в списке)
        if len(select_elements) > 1:
            country_select = select_elements[1]

            # Найти все option элементы внутри select
            options = country_select.find_all('option')

            for option in options:
                value = option['value']
                # Извлечь аббревиатуру страны из URL, если присутствует параметр country
                if 'country=' in value:
                    country_value = value.split('country=')[1]
                    country_values.append(country_value)

        return country_values

    def get_proxy_by_country(self, country):
        url = f'{self.url_freeproxy_country}{country}'
        list_of_data = []

        ua = UserAgent()
        headers = {
            "User-Agent": ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Upgrade-Insecure-Requests": "1"
        }

        # Загружаем HTML-страницу
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Найти таблицу с id="table_proxies"
        table = soup.find('table', id='table_proxies')

        if table:
            # Найти все строки таблицы, исключая заголовок (thead)
            rows = table.find('tbody').find_all('tr')
            # print(rows)
            for row in rows:
                columns = row.find_all('td')
                if len(columns) > 2:
                    encoded_ip = columns[1].get('data-ip')
                    encoded_port = columns[2].get('data-port')

                    if encoded_ip and encoded_port:
                        ip = self.decode_base64(encoded_ip)
                        port = self.decode_base64(encoded_port)
                        data = {"ip": ip, "port": port, "country": country}
                        list_of_data.append(data)
        print(list_of_data)

        return list_of_data

