# Generated by Django 3.2 on 2023-11-16 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_inventorylist_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventorylist',
            name='quantity',
        ),
        migrations.AddField(
            model_name='shopping_list_item',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]