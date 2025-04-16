from rest_framework import serializers

from brick_main.models import WantedList


class WantedsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WantedList
        fields = ['id', 'name', 'description', 'owner']


class WantedListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WantedList
        fields = ['id', 'name', 'description', 'owner']
    
    def create(self, validated_data):
        wanted = WantedList.objects.create(**validated_data)
        wanted.owner = self.context.get("owner")
        wanted.save()
        return validated_data
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)

        instance.save()
        return instance

