from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group

from authen.models import CustomUser, Country, City


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ["id", "name"]


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ["id", "name", "country"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "password2", "birth_date", "country", "city"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли должны совпадать."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            birth_date=validated_data["birth_date"],
            country=validated_data["country"],
            city=validated_data["city"],
        )
        user.set_password(validated_data["password"])
        user.is_active = False
        user.is_email_verified = False
        user.save()
        groups_data = Group.objects.get(name="buyer")
        user.groups.add(groups_data)
        return user


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)


class LoginSuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    email = serializers.EmailField()
