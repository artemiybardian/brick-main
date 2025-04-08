from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.permissions import IsLogin

from authen.profile.serializers import UserProfileSerializer


class ProfileAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(tags=["User Profile"], responses={200: UserProfileSerializer(many=True)})
    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)