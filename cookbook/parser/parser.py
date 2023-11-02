from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


chrome_options = Options()
chrome_options.add_argument("--headless")


driver = webdriver.Chrome(options=chrome_options)


url = 'https://dostavka.magnit.ru/express/catalog/moloko_syr_yaytsa?page=1'


driver.get(url)


driver.implicitly_wait(10)


body = driver.find_element(By.TAG_NAME, 'body')
for _ in range(5):
    body.send_keys(Keys.PAGE_DOWN)
    driver.implicitly_wait(2)


page_source = driver.page_source


driver.quit()


soup = BeautifulSoup(page_source, 'html.parser')


product_cards = soup.find_all(class_='product-card__inner')

for card in product_cards:
    title = card.find(class_='text__content').text
    price = card.find(class_='m-price__current').text
    print(f"Название: {title}, Цена: {price}")

