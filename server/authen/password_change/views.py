from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action

from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import update_session_auth_hash
from django.utils.encoding import smart_bytes

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.permissions import IsLogin
from utils.utils import Util

from authen.models import CustomUser
from authen.password_change.serializers import  ChangePasswordSerializer, ResetPasswordSerializer, PasswordResetCompleteSerializer


class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(
        tags=['User Profile'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='Новый пароль'),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='Подтвердите пароль'),
            }
        )
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.data.get("new_password"))
            user.save()
            update_session_auth_hash(request, user)
            return Response({"error": "Пароль успешно изменен."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordRestEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(tags=['Forget Password'], request_body=ResetPasswordSerializer)
    @action(methods=['post'], detail=False)
    def post(self, request):
        email = request.data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            absurl = f"http://localhost:5173/reset-password/{uidb64}/{token}"
            email_body = f"Здравствуйте! \n Используйте ссылку ниже, чтобы сбросить пароль. \n link: {absurl}"
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Reset your password",
            }

            Util.send(data)

            return Response({"message": "На ваш адрес электронной почты было отправлено письмо для сброса пароля."}, status=status.HTTP_200_OK)
        return Response({"error": "Этот адрес электронной почты не найден."}, status=status.HTTP_404_NOT_FOUND)


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = PasswordResetCompleteSerializer

    @swagger_auto_schema(tags=['Forget Password'], request_body=PasswordResetCompleteSerializer)
    @action(methods=['patch'], detail=False)
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Пароль изменен."}, status=status.HTTP_200_OK)