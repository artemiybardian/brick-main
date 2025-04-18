from rest_framework import serializers

class TopProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(source='product__id')
    name = serializers.CharField(source='product__name')
    total_quantity = serializers.IntegerField()