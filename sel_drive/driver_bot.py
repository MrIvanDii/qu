from fake_useragent import UserAgent
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service as ChromeService
import sel_drive.params as params
import httpagentparser
import random
import time
import re
from seleniumwire import webdriver
from urllib.parse import urlparse
from Proxy.main_proxy import ProxyFilter
from DB.data import proxies_list_3 as http_prox_list
from DB.data import list_of_proxies_2 as sock_prox_list


class GoogDrive:

    def __init__(self, proxy):
        self.drive_path = '/Users/martinanikola/PycharmProjects/PropshtScrapping_V2/sel_drive/chrom_drive/chromedriver'
        self.stealth_params = params
        self.proxies = proxy
        self.h_prox = http_prox_list
        self.s_prox = sock_prox_list

    def generate_sec_ch_ua_platform(self, user_agent):
        parsed_ua = httpagentparser.detect(user_agent)

        platform = parsed_ua.get('os', {}).get('name', 'Unknown')

        # Форматируем platform для Sec-CH-UA-Platform
        platform_mapping = {
            "Windows": "Windows",
            "Mac OS": "macOS",
            "Linux": "Linux",
            "Android": "Android",
            "iOS": "iOS"
        }

        sec_ch_ua_platform = platform_mapping.get(platform, "Unknown")

        return f'"{sec_ch_ua_platform}"'

    def generate_sec_ch_ua(self, user_agent):
        browser_patterns = {
            'Chrome': r'Chrome/([0-9.]+)',
            'Chromium': r'Chromium/([0-9.]+)',
            'Edge': r'Edg/([0-9.]+)',
            'Safari': r'Version/([0-9.]+).*Safari',
            'Firefox': r'Firefox/([0-9.]+)',
        }

        browser_info = []

        for browser, pattern in browser_patterns.items():
            match = re.search(pattern, user_agent)
            if match:
                version = match.group(1)
                browser_info.append(f'"{browser}";v="{version.split(".")[0]}"')

        # Adding the "Not A Brand" entry
        browser_info.append('"Not A Brand";v="99"')
        browser_info.append('"Chromium";v="91"')
        sec_ch_ua = ', '.join(browser_info)
        return sec_ch_ua

    def get_domain_from_url(self, ur_l):
        """
        Функция принимает ссылку на сайт и возвращает домен сайта.

        :param ur_l: URL сайта
        :return: домен сайта
        """
        parsed_url = urlparse(ur_l)
        return parsed_url.netloc

    def get_path_from_url(self, ur_l):
        """
        Функция принимает ссылку на сайт и возвращает путь сайта.

        :param ur_l: URL сайта
        :return: путь сайта
        """
        parsed_url = urlparse(ur_l)
        return parsed_url.path

    def check_cloudfl_capctcha(self, sourc):

        if 'cloudflare' in sourc.lower():

            if 'captcha' in sourc.lower():
                print(f'[BLOCKED by captcha and Cloudflare]')
                print()
                return

            print(f'[BLOCKED by cloudflare]')
            print()
            return

        elif 'captcha' in sourc.lower() and 'cloudflare' not in sourc.lower():
            print(f'[BLOCKED by Captcha]')
            print()
            return

        elif 'captcha' not in sourc.lower() and 'cloudflare' not in sourc.lower():
            print('NOT BLOCKED')

    def get_random_stealth_params(self):

        rand_params = {
            'languages': random.choice(self.stealth_params.accept_language_params),
            'vendor': random.choice(self.stealth_params.vendors_pc),
            'platform': random.choice(self.stealth_params.platforms_pc),
            'webgl_vendor': random.choice(self.stealth_params.webgl_vendors_pc),
            'renderer': random.choice(self.stealth_params.renderers_pc),
            'referer': random.choice(self.stealth_params.referers),
            'plugin': random.choice(self.stealth_params.plugin),  # Надо сделать так чтоб плагинов было от 1 до 4
            'custom_resolution': random.choice(self.stealth_params.custom_resolutions),
            'hardware_concurrency': random.choice(self.stealth_params.hardware_concurrency),
            'navigator_permissions': random.choice(self.stealth_params.navigator_permissions),
            'navigator_plugins': random.choice(self.stealth_params.navigator_plugins),
            'audio_codecs': random.choice(self.stealth_params.audio_codecs),
            'video_codecs': random.choice(self.stealth_params.video_codecs),
            'accept': random.choice(self.stealth_params.accept_list),
            'accept-Encoding': random.choice(self.stealth_params.accept_encodings)
        }

        return rand_params

    def get_proxy_driver(self, ur_l, proxy_tipe='s'):
        """
        Данная ф-я принимает аргументом ссылку на видео
        и результатом выдает название игры
        в которой данное видео было записанно.
        """
        host_name = self.get_domain_from_url(ur_l=ur_l)
        path_name = self.get_path_from_url(ur_l=ur_l)

        # путь к драйверу
        chromedriver_bin = self.drive_path

        # Фейковые юзерагенты для ПК
        ua = UserAgent(platforms="pc")
        random_ua = ua.random

        # Proxy
        prox_manager = ProxyFilter()
        proxies_list = prox_manager.check_http_proxies(self.h_prox)
        proxya = random.choice(proxies_list)
        print('PROXYA: ', proxya)

        sech = self.generate_sec_ch_ua(random_ua)
        sech_platform = self.generate_sec_ch_ua_platform(random_ua)

        # Настраиваем драйвер
        options = webdriver.ChromeOptions()

        # options.add_argument('--ignore-ssl-errors=yes')
        # options.add_argument('--ignore-certificate-errors')

        options.add_argument('"--log-level=3"')
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Работа в фоновом режиме
        # options.add_argument("--headless")

        # Путь к папке с профилем пользователя гугл
        # options.add_argument("--user-data-dir=/Users/martinanikola/PycharmProjects/YouTubeAutomation/Chrome/user")

        # Выбираем конкретного пользователя
        # options.add_argument("--profile-directory=Profile 1")

        # А вот тут я не знаю что за хуйня несется - но это надо!
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Передаем путь к файлу драйвера
        service = ChromeService(executable_path=chromedriver_bin)

        # Получаем данные о прокси
        proxy = self.proxies
        print('Используем проксю :', proxy)

        proxy_options = {}

        if proxy_tipe == 's':
            # Настройки Selenium-Wire
            proxy_options = {
                'proxy': {
                    'http': proxy['https'],
                    'https': proxy['https'],
                    'no_proxy': 'localhost,127.0.0.1'
                }
            }
            print('Используем проксю :', proxy)

        elif proxy_tipe == 'h':
            proxy_options = {
                'proxy': {
                    'https': proxya
                }
            }
            print('Используем проксю :', proxya)

        # Определяем драйвер
        driver = webdriver.Chrome(service=service, options=options, seleniumwire_options=proxy_options)

        stealth_params = self.get_random_stealth_params()

        # STEALTH
        stealth(driver,
                user_agent=random_ua,
                languages=stealth_params["languages"],
                vendor=stealth_params["vendor"],
                platform=sech_platform,  # Необходимо чтоб платформа соответствовала платформе юзерагента
                webgl_vendor=stealth_params["webgl_vendor"],
                renderer=stealth_params["renderer"],
                plugin=stealth_params["plugin"],  # Надо сделать так чтоб плагинов было от 1 до 4
                custom_resolution=stealth_params["custom_resolution"],
                hardware_concurrency=stealth_params["hardware_concurrency"],
                navigator_permissions=stealth_params["navigator_permissions"],
                navigator_plugins=stealth_params["navigator_plugins"],
                media_codecs={'audio': stealth_params["audio_codecs"], 'video': stealth_params["video_codecs"]},
                fix_hairline=False,
                do_not_track=True,
                )

        driver.header_overrides = {
            "authority": host_name,
            "method": "GET",
            "path": path_name,
            "scheme": "https",
            "Accept": stealth_params["accept"],
            "Accept-Encoding": stealth_params["accept-Encoding"],
            "Accept-Language": stealth_params["languages"],
            "Cache-Control": "max-age=0",
            "Dnt": "1",
            "Sec-Ch-Ua": sech,
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": sech_platform,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            
            "Referer": stealth_params["referer"],


        }
        return driver

    def get_page_source(self, page_url):

        goog_drive = self.get_proxy_driver(ur_l=page_url, proxy_tipe='h')
        goog_drive.get(page_url)
        time.sleep(60)
        html_page = goog_drive.page_source
        goog_drive.close()

        return html_page

    def get_page_src_no_proxy(self, page_url):
        goog_drive = self.get_no_proxy_driver(page_url)
        goog_drive.get(page_url)
        time.sleep(5)
        html_page = goog_drive.page_source

        return html_page

    def get_no_proxy_driver(self, ur_l):
        """
        Данная ф-я принимает аргументом ссылку на видео
        и результатом выдает название игры
        в которой данное видео было записанно.
        """

        # путь к драйверу
        chromedriver_bin = self.drive_path

        # Фейковые юзерагенты для ПК
        ua = UserAgent(platforms="pc")
        random_ua = ua.random

        host_name = self.get_domain_from_url(ur_l=ur_l)
        path_name = self.get_path_from_url(ur_l=ur_l)
        sech = self.generate_sec_ch_ua(random_ua)
        sech_platform = self.generate_sec_ch_ua_platform(random_ua)

        # Настраиваем драйвер
        options = webdriver.ChromeOptions()

        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')

        options.add_argument('"--log-level=3"')

        # Работа в фоновом режиме
        # options.add_argument("--headless")

        # Путь к папке с профилем пользователя гугл
        # options.add_argument("--user-data-dir=/Users/martinanikola/PycharmProjects/YouTubeAutomation/Chrome/user")

        # Выбираем конкретного пользователя
        # options.add_argument("--profile-directory=Profile 1")

        # А вот тут я не знаю что за хуйня несется - но это надо!
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Передаем путь к файлу драйвера
        service = ChromeService(executable_path=chromedriver_bin)

        # Определяем драйвер
        driver = webdriver.Chrome(service=service, options=options)

        stealth_params = self.get_random_stealth_params()

        # STEALTH
        stealth(driver,
                user_agent=random_ua,
                languages=stealth_params["languages"],
                vendor=stealth_params["vendor"],
                platform=sech_platform,  # Необходимо чтоб платформа соответствовала платформе юзерагента
                webgl_vendor=stealth_params["webgl_vendor"],
                renderer=stealth_params["renderer"],
                plugin=stealth_params["plugin"],  # Надо сделать так чтоб плагинов было от 1 до 4
                custom_resolution=stealth_params["custom_resolution"],
                hardware_concurrency=stealth_params["hardware_concurrency"],
                navigator_permissions=stealth_params["navigator_permissions"],
                navigator_plugins=stealth_params["navigator_plugins"],
                media_codecs={'audio': stealth_params["audio_codecs"], 'video': stealth_params["video_codecs"]},
                fix_hairline=False,
                do_not_track=True,
                )

        driver.header_overrides = {
            "authority": host_name,
            "method": "GET",
            "path": path_name,
            "scheme": "https",
            "Accept": stealth_params["accept"],
            "Accept-Encoding": stealth_params["accept-Encoding"],
            "Accept-Language": stealth_params["languages"],
            "Cache-Control": "max-age=0",
            "Dnt": "1",
            "Sec-Ch-Ua": sech,
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": sech_platform,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",

            "Referer": stealth_params["referer"],


        }
        return driver

"""
Возможно необходимо привязать определенный stealth и хедеры к одному IP
или же надо использовать много разных IP и тогда можно не парится и хедерах и аргументах stealth
"""

# if __name__ == "__main__":
#     db_path = '/Users/martinanikola/PycharmProjects/PropshtScrapping_V2/DB/australia_online_casinos.db'
#     prox_manager = ProxyFilter()
#     html_p = HTMLParser(db_path=db_path)
#     # proxies_list = list_of_proxies
#     proxies_list = prox_manager.check_proxies(list_of_proxies)
#
#     proxya = random.choice(proxies_list)
#
#     # url = 'https://www.quora.com/Can-you-win-on-online-slots/log'
#     # url = 'https://www.nowsecure.nl/'
#     url = 'https://httpbin.org/anything'
#
#     for one_proxya in proxies_list:
#         proxies = html_p.get_proxya_for_selen(one_proxya)
#         manager = GoogDrive(proxy=proxies)
#
#         proxy_src = manager.get_page_source(page_url=url)
#         print(proxy_src)
#         # no_proxy_src = manager.get_page_src_no_proxy(page_url=url)
#         # print(no_proxy_src)
