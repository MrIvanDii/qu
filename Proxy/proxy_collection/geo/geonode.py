import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re


class GeoNode:

    def __init__(self):
        self.base_url = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc'

    def get_page_html(self, page_url):
        ua = UserAgent()

        headers = {
            "User-Agent": ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Upgrade-Insecure-Requests": "1"
        }

        # Загружаем HTML-страницу
        response = requests.get(url=page_url, headers=headers)

        json_data = response.json()

        return json_data

    def get_page_number(self, page_url):
        match = re.search(r'page=(\d+)', page_url)
        if match:
            return int(match.group(1))
        else:
            return None

    def get_next_page_url(self, prev_page_url=None):

        if prev_page_url is None:
            return self.base_url

        elif prev_page_url is not None:
            prev_page_number = self.get_page_number(prev_page_url)
            next_page_number = prev_page_number + 1
            template = f'https://proxylist.geonode.com/api/proxy-list?limit=500&page={next_page_number}&sort_by=lastChecked&sort_type=desc'
            return template

    def data_collection_proces(self):

        url = self.base_url

        flag = True

        while flag is True:
            j_dat = self.get_page_html(page_url=url)
            if len(j_dat) == 500:
                flag = True
            if len(j_dat) < 500:
                flag = False



if __name__ == "__main__":
    pg_url = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc'
    geo_manager = GeoNode()
    j_data = geo_manager.get_page_html(page_url=pg_url)
    # print(len(j_data['data']))
    for _ in j_data['data']:
        print(_)
        # print(f'{_}: ', j_data[_])

    # print(geo_manager.get_page_number(pg_url))
