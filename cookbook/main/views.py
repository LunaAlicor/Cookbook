from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q, Sum
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .filters import InventoryItemFilter
from .forms import CustomAuthenticationForm, RegistrationForm, InventoryItemForm, RecipeForm
from .models import Product, InventoryList, InventoryItem, Shopping_list_item, Recipe, Recipes, Shopping_list
from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django_select2.forms import ModelSelect2MultipleWidget
from rest_framework.response import Response
from .serializers import ProductSerializer, RecipesSerializer, InventoryItemSerializer, InventoryListSerializer, \
    Shopping_list_itemSerializer, Shopping_listSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView


def index(request):
    return render(request, 'main/index.html')


def products(request):
    query = request.GET.get('q', '')
    inventory_query = request.GET.get('inventory_q', '')
    inventory_results = []
    results = []
    shop_list = Shopping_list_item.objects.filter(user=request.user)

    if query and request.method == 'GET':
        results = Product.objects.filter(name__icontains=query)

    if inventory_query and request.method == 'GET':
        inventory_results = InventoryItem.objects.filter(
            Q(product__name__icontains=inventory_query) &
            Q(user=request.user)
        )

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

    if not inventory_results:
        user_inventory = InventoryItem.objects.filter(user=request.user)
    else:
        user_inventory = inventory_results

    return render(request, 'main/products.html', {'form': form, 'user_inventory': user_inventory, 'results': results,
                                                  'query': query, 'inventory_results': inventory_results,
                                                  'shop_list':shop_list})


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
def increase_quantity(request, product_id):
    item = get_object_or_404(InventoryItem, product_id=product_id, user=request.user)
    item.quantity += 1
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

            results = []

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

                Product.objects.create(name=title, price=price.replace('₽', ''))
                results.append({"name": title, "price": price.replace('₽', '')})

    driver.quit()
    return JsonResponse({"results": results})


def shopping(request):
    query = request.GET.get('q', '')
    results = []
    user_inventory = Shopping_list_item.objects.filter(user=request.user)
    if query and request.method == 'GET':
        results = Product.objects.filter(name__icontains=query)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        if product_id and quantity:
            product = Product.objects.get(pk=product_id)
            shopping_item, created = Shopping_list_item.objects.get_or_create(user=request.user, product=product)
            if created:
                shopping_item.quantity = int(quantity)

            shopping_item.save()

    return render(request, 'main/shoping.html', {
        'results': results,
        'user_inventory': user_inventory,
    })


def remove_from_shopping_list(request, item_id):
    shopping_item = get_object_or_404(Shopping_list_item, id=item_id, user=request.user)
    shopping_item.delete()
    return redirect('shopping')


def remove_from_shopping_list_in_products(request, item_id):
    shopping_item = get_object_or_404(Shopping_list_item, id=item_id, user=request.user)
    item = InventoryItem(user=request.user, product=shopping_item.product, availability=True,
                         quantity=shopping_item.quantity, date_of_purchase=timezone.now())
    item.save()
    shopping_item.delete()
    return redirect('products')


def recipes(request):
    user_recipe_objects = Recipes.objects.filter(user=request.user)
    user_recipes = []

    for user_recipe in user_recipe_objects:
        user_recipes.extend(list(user_recipe.recipes.all()))

    return render(request, 'main/Recipes.html', {'user_recipes': user_recipes})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    total_cost = recipe.products.aggregate(total=Sum('price'))['total'] or 0
    return render(request, 'main/recipe_detail.html', {'recipe': recipe, 'total_cost': total_cost})


def all_recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'main/all_recipes.html', {'recipes': recipes})


@csrf_exempt
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            current_user = request.user
            user_recipes, created = Recipes.objects.get_or_create(user=current_user)
            user_recipes.recipes.add(recipe)
            form.save_m2m()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()

    return render(request, 'main/create_recipe.html', {'form': form})


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = ProductSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer


class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer


class InventoryListViewSet(viewsets.ModelViewSet):
    queryset = InventoryList.objects.all()
    serializer_class = InventoryListSerializer


class Shopping_list_itemViewSet(viewsets.ModelViewSet):
    queryset = Shopping_list_item.objects.all()
    serializer_class = Shopping_list_itemSerializer


class Shopping_listViewSet(viewsets.ModelViewSet):
    queryset = Shopping_list.objects.all()
    serializer_class = Shopping_listSerializer


class ProductSearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get('name')
        if query:
            products = Product.objects.filter(name__icontains=query)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response("No query provided", status=status.HTTP_400_BAD_REQUEST)


def del_recipe(request, recipe_id):

    recipes_item = get_object_or_404(Recipes, user=request.user)
    recipe_to_delete = get_object_or_404(Recipe, id=recipe_id)
    recipes_item.recipes.remove(recipe_to_delete)

    return redirect('Recipes')


def add_recipe(request, recipe_id):
    recipes_item = get_object_or_404(Recipes, user=request.user)
    recipe_to_add = get_object_or_404(Recipe, id=recipe_id)
    recipes_item.recipes.add(recipe_to_add)
    return redirect('Recipes')
