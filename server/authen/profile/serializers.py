from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import Group

from authen.models import CustomUser
from authen.auth.serializers import CountrySerializer, CitySerializer


class GroupsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    city = CitySerializer(read_only=True)
    groups = GroupsSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'avatar', 'birth_date', 'country', 'city', 'groups']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, max_length=100, validators=[UniqueValidator(queryset=CustomUser.objects.all()),
            MaxLengthValidator(limit_value=100, message="The email address cannot exceed 30 characters.")])
    avatar = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'birth_date', 'avatar', 'country', 'city']
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)

        if instance.avatar == None:
            instance.avatar = self.context.get("avatar")
        else:
            instance.avatar = validated_data.get("avatar", instance.avatar)

        instance.save()
        return instance