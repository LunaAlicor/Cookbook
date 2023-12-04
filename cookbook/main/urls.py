from django.urls import path, include
from . import views
from django_select2.views import AutoResponseView
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from .views import ProductViewSet, RecipeViewSet, RecipesViewSet, InventoryItemViewSet, InventoryListViewSet, \
    Shopping_list_itemViewSet, Shopping_listViewSet, ProductSearchAPIView

router = DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'comments', RecipeViewSet)
router.register(r'likes', RecipesViewSet)
router.register(r'events', InventoryItemViewSet)
router.register(r'tags', InventoryListViewSet)
router.register(r'teams', Shopping_list_itemViewSet)
router.register(r'memberships', Shopping_listViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.products, name='products'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('register', views.register_view, name='register'),
    path('update_prices/', views.parse, name='update_prices'),
    path('decrease_quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('update_prices2/', views.parse2, name='update_prices2'),
    path('increase_quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('shopping', views.shopping, name='shopping'),
    path('remove/<int:item_id>/', views.remove_from_shopping_list, name='remove_from_shopping_list'),
    path('remove_from_shopping_list_in_products/<int:item_id>/', views.remove_from_shopping_list_in_products, name='remove_from_shopping_list_in_products'),
    path('Recipes', views.recipes, name='Recipes'),
    path('all_recipes', views.all_recipes, name='all_recipes'),
    path('recipe_detail/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('create_recipe', views.create_recipe, name='create_recipe'),
    path('api/', include(router.urls)),
    path('api/docs/', include_docs_urls(title='API Documentation')),
    path('api/products/', ProductSearchAPIView.as_view(), name='product_search'),
    # path('select2/', AutoResponseView.as_view(), name='django_select2'),
    path('del_recipe/<int:recipe_id>/', views.del_recipe, name='del_recipe'),
    path('add_recipe/<int:recipe_id>/', views.add_recipe, name='add_recipe'),
]
