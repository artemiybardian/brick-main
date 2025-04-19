from rest_framework import serializers

from brick_main.models import Theme, Obj


class ThemesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Theme
        fields = ['id', 'collection_name', 'size']


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obj
        fields = ['id', 'item_name', 'description'] 
