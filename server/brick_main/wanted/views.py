from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from brick_main.models import WantedList
from brick_main.wanted.serializers import WantedsListSerializer, WantedListSerializer


class WantedsListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Wanted List"],
        operation_description="Вишлисты пользователь",
        responses={200: WantedsListSerializer(many=True)}
    )
    def get(self, request):
        objects = WantedList.objects.filter(owner=request.user).order_by("-id")
        serializer = WantedsListSerializer(objects, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Wanted List"],
        operation_description="Вишлисты пользователь Создание",
        request_body=WantedListSerializer
    )
    def post(self, request):
        serializer = WantedListSerializer(data=request.data, context={"owner":request.user, "request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WantedListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Wanted List"],
        responses={200: WantedsListSerializer(many=False)}
    )
    def get(self, request, pk):
        objects = get_object_or_404(WantedList, id=pk)
        serializer = WantedsListSerializer(objects, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=["Wanted List"],
        request_body=WantedListSerializer,
    )
    def put(self, request, pk):
        instance = get_object_or_404(WantedList, id=pk)
        serializer = WantedListSerializer(instance=instance, data=request.data, context={"request": request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=["Wanted List"],
        responses={204:  "No Content"}
    )
    def delete(self, request, pk):
        wanted = get_object_or_404(WantedList, id=pk)
        wanted.delete()
        return Response({"message": "Удалить успешно"}, status=status.HTTP_204_NO_CONTENT)


