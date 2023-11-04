from django.contrib import admin
from .models import *
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    # list_filter = ('availability', 'date_of_purchase', 'expiry_date')
    search_fields = ('name', 'price')


admin.site.register(Product, ProductAdmin)
admin.site.register(InventoryList)
admin.site.register(Recipe)
admin.site.register(Recipes)
admin.site.register(Shopping_list)
admin.site.register(Check_list)
