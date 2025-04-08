import random

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.utils import send_verification_email

from authen.models import CustomUser, Country, City
from authen.auth.serializers import (
    RegisterSerializer, LoginSerializer,
    CountrySerializer, CitySerializer
)


class CountryView(APIView):

    @swagger_auto_schema(
        tags=["Auth"],
        operation_description="Страны",
    )
    def get(self, request):
        country = Country.objects.all()
        serializer = CountrySerializer(country, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CityView(APIView):

    @swagger_auto_schema(
        tags=["Auth"],
        operation_description="Города. Получить города по идентификатору страны",
    )
    def get(self, request, country_id):
        country = City.objects.filter(country=country_id)
        serializer = CitySerializer(country, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(APIView):

    @swagger_auto_schema(request_body=RegisterSerializer, tags=["Auth"], responses={201: "Зарегистрирован. Подтвердите адрес электронной почты."})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user, request)
            return Response({"message": "Создано пользователем. Подтвердите адрес электронной почты."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):

    @swagger_auto_schema(
        tags=["Auth"],
        manual_parameters=[
            openapi.Parameter('uidb64', openapi.IN_PATH, description="Пользователь, закодированный в Base64", type=openapi.TYPE_STRING),
            openapi.Parameter('token', openapi.IN_PATH, description="Проверочный токен", type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response(description="Электронная почта подтверждена"),
            400: "Ошибка или истек срок действия токена"
        }
    )
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_email_verified = True
            user.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Электронная почта подтверждена',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Ссылка недействительна или срок ее действия истек.'}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(description="Код подтверждения отправлен по электронной почте"),
            400: openapi.Response(description="Электронная почта не проверена или неверные данные для входа")
        },
        tags=["Auth"]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username_or_email = serializer.validated_data['username_or_email']
            password = serializer.validated_data['password']

            user = None
            if '@' in username_or_email:
                user = authenticate(request, username=username_or_email, password=password)
            else:
                user = authenticate(request, username=username_or_email, password=password)

            if user:
                if not user.is_email_verified:
                    return Response({'error': 'Подтвердите адрес электронной почты.'}, status=status.HTTP_400_BAD_REQUEST)

                verification_code = random.randint(100000, 999999)
                user.verification_code = verification_code
                user.save()
                
                send_mail(
                    'Ваш проверочный код',
                    f'Ваш код подтверждения: {verification_code}',
                    'from@example.com',
                    [user.email],
                    fail_silently=False,
                )

                return Response({
                    'message': 'Пожалуйста, проверьте свою электронную почту на наличие проверочного кода.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Неверные учетные данные или адрес электронной почты не проверен.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="Адрес электронной почты пользователя"),
                'verification_code': openapi.Schema(type=openapi.TYPE_STRING, description="Код подтверждения отправлен на электронную почту пользователя")
            },
        ),
        responses={
            200: openapi.Response(description="Проверка прошла успешно. Токен JWT возвращен."),
            400: openapi.Response(description="Неверный код подтверждения или пользователь не найден.")
        },
        tags=["Auth"]
    )
    def post(self, request):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')

        try:
            user = CustomUser.objects.get(email=email)
            if user.verification_code == verification_code:

                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Проверка прошла успешно.',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Неверный проверочный код.'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_400_BAD_REQUEST)