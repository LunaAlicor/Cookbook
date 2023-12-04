from django.contrib import admin
from .models import *


# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    # list_filter = ('availability', 'date_of_purchase', 'expiry_date')
    search_fields = ('name', 'price')


class ProductInLine(admin.TabularInline):
    model = Recipe.products.through


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        ProductInLine
    ]
    list_display = ('name', 'recipe_short', 'description_short', 'cuisine', 'classification')
    search_fields = ('name', 'cuisine', 'classification', 'description_short')

    def recipe_short(self, obj: Recipe) -> str:
        if len(obj.recipe) < 48:
            return obj.recipe
        return obj.recipe[:48] + '...'

    def description_short(self, obj: Recipe) -> str:
        if len(obj.description) < 48:
            return obj.recipe
        return obj.recipe[:48] + '...'


admin.site.register(Product, ProductAdmin)
admin.site.register(InventoryItem)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Recipes)
admin.site.register(Shopping_list)
admin.site.register(Check_list)
admin.site.register(InventoryList)
