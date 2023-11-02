from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC





chrome_options = Options()
chrome_options.add_argument("--headless")

urls = [
    'ovoshchi_frukty',
    'moloko_syr_yaytsa',
    'myaso_ptitsa_kolbasy',
    'gotovaya_eda',
    'napitki_soki_voda',
    'chay_kofe_kakao',
    'khleb_vypechka_sneki',
]

driver = webdriver.Chrome(options=chrome_options)

for url_suffix in urls:
    for page in range(1, 41):
        url = f'https://dostavka.magnit.ru/express/catalog/{url_suffix}?page={page}'
        driver.get(url)


        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(5):
            body.send_keys(Keys.PAGE_DOWN)

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        product_cards = soup.find_all(class_='product-card__inner')

        for card in product_cards:
            title = card.find(class_='text__content').text
            price = card.find(class_='m-price__current').text
            if "/" in price:
                price.split('/')
                price = price[0]
            # Product.objects.create(name=title, price=price)
            print(f"Название: {title}, Цена: {price.replace('₽', '')}")

driver.quit()
