# Generated by Django 3.2 on 2023-11-14 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20231102_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorylist',
            name='products',
            field=models.ManyToManyField(to='main.InventoryItem'),
        ),
    ]