from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    availability = models.BooleanField()
    quantity = models.IntegerField()
    date_of_purchase = models.DateField(null=True)
    expiry_date = models.TimeField()


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
