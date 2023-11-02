from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm, RegistrationForm
from .models import Product
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
    return render(request, 'main/Products.html')


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
