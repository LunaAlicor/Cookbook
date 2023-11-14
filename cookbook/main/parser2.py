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
    'zamorozka-3e94909/morozhenoe-sladosti-5810632',

    'kolbasi-sosiski-delikatesy/kolbasi',
    'riba-ikra-dari-morya-31ba8ac/riiba',
    'sousi-spetsii-maslo/sousi-zapravki',
    'chipsi-sneki-sukhofrukti/chipsi',
    'ovoshchi-frukti-orekhi/ovoshchi',
    'konservi-solenya-copy/ovoshchnie-konservi-gribi',
    'miaso-ptitsa/ptitsa',
    'khleb-khlebtsi-vipechka/svezhaya-vipechka',
    'voda-soki-napitki-copy/voda',
]

driver = webdriver.Chrome(options=chrome_options)

for url_suffix in urls:
    for page in range(1, 41):
        skip_check = []
        url = f'https://sbermarket.ru/lenta/c/{url_suffix}?page={page}'
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(5):
            body.send_keys(Keys.PAGE_DOWN)

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        product_cards = soup.find_all(class_='ProductCard_root__zO_B9 ProductCard_addToCartBig__mmVRI')
        skip_check = soup.find_all(class_="ProductsGrid_noProducts__lcZRk")

        if skip_check != []:
            break

        for card in product_cards:
            title = card.find(class_='ProductCard_title__iB_Dr').text
            price = card.find(class_='ProductCardPrice_price__zSwp0').text.replace('Цена за 1 шт.', '')
            price = price.replace(',', '.')

            if "Цена со скидкой за 1 шт." in price:
                price = price.replace('Цена со скидкой за 1 шт.', '')

            if 'Цена со скидкой за 1 кг' in price:
                price = price.replace('Цена со скидкой за 1 кг', '')
                title += ' цена за 1 кг'

            if 'Цена за 1 кг' in price:
                price = price.replace('Цена за 1 кг', '')
                title += ' цена за 1 кг'

            if "/" in price:
                price.split('/')
                price = price[0]

            price = price.replace(' ', '')
            # Product.objects.create(name=title, price=price)
            print(f"Название: {title}, Цена: {price.replace('₽', '')}")

driver.quit()
