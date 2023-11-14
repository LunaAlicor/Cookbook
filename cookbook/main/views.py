from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from .filters import InventoryItemFilter
from .forms import CustomAuthenticationForm, RegistrationForm, InventoryItemForm
from .models import Product, InventoryList, InventoryItem
from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Create your views here.


def index(request):
    return render(request, 'main/index.html')


def products(request):
    query = request.GET.get('q', '')
    results = []

    if query and request.method == 'GET':
        results = Product.objects.filter(name__icontains=query)

    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.date_of_purchase = timezone.now()
            item.availability = True
            item.save()
            return redirect('products')
    else:
        form = InventoryItemForm()

    user_inventory = InventoryItem.objects.filter(user=request.user)

    return render(request, 'main/products.html', {'form': form, 'user_inventory': user_inventory, 'results': results, 'query': query})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'main/login.html', {'form': form})


def profile(request):
    return render(request, 'main/profile.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким логином уже существует.')
            return render(request, 'main/register.html')

        user = User.objects.create_user(username=username, password=password, email=email)
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('index')

    return render(request, 'main/register.html')


def parse(request):

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

            results = []
            for card in product_cards:
                title = card.find(class_='text__content').text
                price = card.find(class_='m-price__current').text
                if "/" in price:
                    price.split('/')
                    price = price[0]
                Product.objects.create(name=title, price=price.replace('₽', ''))
                results.append({"name": title, "price": price.replace('₽', '')})

    driver.quit()
    return JsonResponse({"results": results})


@csrf_exempt
def decrease_quantity(request, product_id):
    item = get_object_or_404(InventoryItem, product_id=product_id, user=request.user)
    item.quantity -= 1
    item.save()


@csrf_exempt
def delete_product(request, product_id):
    item = get_object_or_404(InventoryItem, product_id=product_id, user=request.user)
    item.delete()

    return JsonResponse({'success': True})


def parse2(request):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    urls = [
        'zamorozka-3e94909/morozhenoe-sladosti-5810632',
        'bakaleya/makaroni-6a87353',
        'sladosti_new/pechene-pryaniki-vafli-ce67498',
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
            url = f'https://sbermarket.ru/5ka/c/{url_suffix}?page={page}'
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            body = driver.find_element(By.TAG_NAME, 'body')

            for _ in range(5):
                body.send_keys(Keys.PAGE_DOWN)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            product_cards = soup.find_all(class_='ProductCard_root__K6IZK ProductCard_addToCartBig__h5PsY')
            skip_check = soup.find_all(class_="ProductsGrid_noProducts___TVHi")

            if skip_check != []:
                break

            results = []

            for card in product_cards:
                title = card.find(class_='ProductCard_title__iNsaD').text
                price = card.find(class_='ProductCardPrice_price__Kv7Q7').text.replace('Цена за 1 шт.', '')
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
                Product.objects.create(name=title, price=price.replace('₽', ''))
                results.append({"name": title, "price": price.replace('₽', '')})

    driver.quit()
    return JsonResponse({"results": results})