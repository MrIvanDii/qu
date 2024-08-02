import seleniumwire.undetected_chromedriver as uc
import time
from selenium.webdriver.chrome.service import Service as ChromeService

# set Chrome Options
chrome_options = uc.ChromeOptions()

chromedriver_bin = '/Users/martinanikola/PycharmProjects/PropshtScrapping_V2/sel_drive/chrom_drive/chromedriver'
service = ChromeService(executable_path=chromedriver_bin)

# define your proxy settings
proxy_options = {
    'proxy': {
        'http': 'https://propsht:39769A1376183220F93DC1FBB0DC88AB@5.181.40.13:12333',
        'https': 'https://propsht:39769A1376183220F93DC1FBB0DC88AB@5.181.40.13:12333'
    }
}

# initialize Chrome driver instance with specified proxy settings
driver = uc.Chrome(
    options=chrome_options,
    seleniumwire_options=proxy_options,
    service=service
)

# navigate to target website
driver.get('https://www.quora.com/My-son-deposited-my-money-to-gambling-site-big-amount-of-money-I-asked-for-a-full-refund-they-said-that-they-will-investigate-Will-they-refund-me')
time.sleep(5)
html = driver.page_source

with open('test.html', 'w') as file:
    file.write(html)

driver.quit()
