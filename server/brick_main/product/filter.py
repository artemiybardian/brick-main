from django_filters import rest_framework as filters
from brick_main.models import ObjProduct
from authen.models import Country


class ObjProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='product_price__price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='product_price__price', lookup_expr='lte')
    condition = filters.CharFilter(field_name='condition', lookup_expr='iexact')
    country = filters.ModelMultipleChoiceFilter(field_name='country', to_field_name='id', queryset=Country.objects.all())

    class Meta:
        model = ObjProduct
        fields = ['condition', 'min_price', 'max_price', 'country']
