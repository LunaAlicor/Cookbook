from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = '__all__'


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'


class InventoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryList
        fields = '__all__'


class Shopping_list_itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopping_list_item
        fields = '__all__'


class Shopping_listSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopping_list
        fields = '__all__'

# class Check_list
