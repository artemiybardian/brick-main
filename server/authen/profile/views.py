from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404

from utils.permissions import IsLogin

from authen.models import CustomUser
from authen.profile.serializers import UserProfileSerializer, UserProfileUpdateSerializer


class ProfileAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(tags=["User Profile"], responses={200: UserProfileSerializer(many=True)})
    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(tags=["User Profile"], request_body=UserProfileUpdateSerializer)
    def put(self, request):
        queryset = get_object_or_404(CustomUser, id=request.user.id)
        serializer = UserProfileUpdateSerializer(context={"request": request}, instance=queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["User Profile"], responses={204:  'No Content'})
    def delete(self, request):
        user_delete = CustomUser.objects.get(id=request.user.id)
        user_delete.delete()
        return Response({"message": "delete success"}, status=status.HTTP_204_NO_CONTENT)