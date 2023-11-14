import django_filters
from .models import InventoryItem


class InventoryItemFilter(django_filters.FilterSet):
    product__name = django_filters.CharFilter(lookup_expr='icontains', label='Product Name')

    class Meta:
        model = InventoryItem
        fields = ['product__name', 'quantity']
