from django.urls import path
from . import views

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
]
