from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(null=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    recipe = models.TextField(default='1)\n2)\n3)\n4)\n5)\n')
    products = models.ManyToManyField(Product)
    cooking_time = models.TimeField()
    cuisine = models.CharField(max_length=50)
    classification = models.CharField(max_length=50)
    likes = models.IntegerField(default=0)
    description = models.TextField(null=True, max_length=500)
    # Добавить автора рецепта


class Recipes(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)


class InventoryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    availability = models.BooleanField(null=True)
    quantity = models.IntegerField(null=True)
    date_of_purchase = models.DateField(null=True)
    expiry_date = models.DateField(null=True)


class InventoryList(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(InventoryItem)


class Shopping_list_item(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)


class Shopping_list(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    items = models.ManyToManyField(Shopping_list_item, related_name='shopping_lists')

    def all_items(self):
        return self.items.all()


class Check_list(models.Model):
    pass
