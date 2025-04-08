from rest_framework import serializers
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
    gorups = GroupsSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'avatar', 'birth_date', 'country', 'city', 'gorups']