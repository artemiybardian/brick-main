from rest_framework import serializers

from brick_main.models import Shops, Deliverys, Currency, Country


class DeliverysSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deliverys
        fields = ['id', 'name']


class ShopsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shops
        fields = ['id', 'name', 'address', 'country', 'is_openid', 'delivery_service', 'currency', 'owner']


class ShopSerializer(serializers.ModelSerializer):
    currency = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(), many=True
    )
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), many=True
    )

    class Meta:
        model = Shops
        fields = ['id', 'name', 'address', 'country', 'delivery_service', 'currency', 'owner']
    

    def create(self, validated_data):
        countries = validated_data.pop('country', [])
        currencies = validated_data.pop('currency', [])
        shop = Shops.objects.create(**validated_data)
        shop.owner = self.context.get("owner")
        shop.save()
        shop.currency.set(currencies) 
        shop.country.set(countries)
        return shop
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.country = validated_data.get("country", instance.country)
        instance.delivery_service = validated_data.get("delivery_service", instance.delivery_service)
        instance.currency = validated_data.get("currency", instance.currency)

        currencies = validated_data.pop('currency', None)
        countries = validated_data.pop('country', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if currencies is not None:
            instance.currency.set(currencies)

        if countries is not None:
            instance.country.set(countries)

        instance.save()
        return instance


class ShopIsActiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shops
        fields = ['id', 'is_openid', 'owner']