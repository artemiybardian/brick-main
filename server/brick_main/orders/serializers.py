from rest_framework import serializers

from brick_main.models import Order, OrderItem


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity']


class OrdersSerializer(serializers.ModelSerializer):
    items_product = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'shop', 'is_new', 'items_product', 'status', 'created_at']


class OrderStatusChangeSellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'is_new', 'status']
    
    def update(self, instance, validated_data):
        instance.is_new = validated_data.get("is_new", instance.is_new)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


class OrderStatusChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'status']
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


class OrderCreateSerializer(serializers.ModelSerializer):
    items_product = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'shop', 'created_at', 'delivery', 'status', 'items_product']
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        items_data = validated_data.pop('items_product')
        order = Order.objects.create(user=self.context['request'].user, **validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order