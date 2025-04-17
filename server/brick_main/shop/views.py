from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.permissions import IsSellerRole

from brick_main.models import Deliverys, Shops
from brick_main.shop.serializers import DeliverysSerializer, ShopsSerializer, ShopSerializer, ShopIsActiveSerializer


class DeliveryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Shop"],
        operation_description="Для владельцев магазинов, служб доставки",
        responses={200: DeliverysSerializer(many=True)}
    )
    def get(self, request):
        objects = Deliverys.objects.all().order_by("-id")
        serializer = DeliverysSerializer(objects, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSellerRole]

    @swagger_auto_schema(
        tags=["Shop"],
        operation_description="Магазин, принадлежащий продавцу",
        responses={200: ShopsSerializer(many=True)}
    )
    def get(self, request):
        objects = Shops.objects.filter(owner=request.user).order_by("-id")
        serializer = ShopsSerializer(objects, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=["Shop"],
        operation_description="Создание магазина для роли продавца",
        request_body=ShopSerializer
    )
    def post(self, request):
        serializer = ShopSerializer(data=request.data, context={"owner":request.user, "request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSellerRole]

    @swagger_auto_schema(
        tags=["Shop"],
        operation_description=["Информация о магазине для роли продавца"],
        responses={200: ShopsSerializer(many=False)}
    )
    def get(self, request, shop_id):
        objects = get_object_or_404(Shops, id=shop_id)
        serializer = ShopsSerializer(objects, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=["Shop"],
        operation_description=["Обновление информации о магазине для роли продавца"],
        request_body=ShopSerializer,
    )
    def put(self, request, shop_id):
        instance = get_object_or_404(Shops, id=shop_id)
        serializer = ShopSerializer(instance=instance, data=request.data, context={"request": request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=["Shop"],
        operation_description=["Удалить магазин для роли продавца"],
        responses={204:  "No Content"}
    )
    def delete(self, request, shop_id):
        shop = get_object_or_404(Shops, id=shop_id)
        shop.delete()
        return Response({"message": "Удалить успешно"}, status=status.HTTP_204_NO_CONTENT)


class ShopIsActiveView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSellerRole]

    @swagger_auto_schema(
        tags=["Shop"],
        operation_description=["Открыть/закрыть магазин. True = открыто / False = закрыто"],
        request_body=ShopIsActiveSerializer,
    )
    def patch(self, request, shop_id):
        instance = get_object_or_404(Shops, id=shop_id)
        serializer = ShopIsActiveSerializer(instance=instance, data=request.data, context={"request": request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
