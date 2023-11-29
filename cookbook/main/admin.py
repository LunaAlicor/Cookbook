from django.contrib import admin
from .models import *
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    # list_filter = ('availability', 'date_of_purchase', 'expiry_date')
    search_fields = ('name', 'price')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuisine', 'classification')
    search_fields = ('name', 'cuisine', 'classification')


admin.site.register(Product, ProductAdmin)
admin.site.register(InventoryItem)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Recipes)
admin.site.register(Shopping_list)
admin.site.register(Check_list)
admin.site.register(InventoryList)
