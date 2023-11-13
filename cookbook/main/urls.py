from django.contrib import admin
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
]
