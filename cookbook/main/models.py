from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(null=True)
    availability = models.BooleanField(null=True)
    quantity = models.IntegerField(null=True)
    date_of_purchase = models.DateField(null=True)
    expiry_date = models.DateField(null=True)


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)
    cooking_time = models.TimeField()
    cuisine = models.CharField(max_length=50)
    classification = models.CharField(max_length=50)
    likes = models.IntegerField(default=0)


class Recipes(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)


class InventoryList(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)


class Shopping_list(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)


class Check_list(models.Model):
    pass
