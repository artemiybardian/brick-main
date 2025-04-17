from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from brick_main.models import WantedList, WantedListProduct
from brick_main.wanted.serializers import WantedsListSerializer, WantedListSerializer, WantedListProductSerializer


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


class AddProductToWishlistAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Wanted List / Product"],
        request_body=WantedListProductSerializer,
        responses={
            201: openapi.Response("Продукт добавлен", WantedListProductSerializer),
            400: "Bad Request",
        },
        operation_description="Добавить продукт в Вишлисты пользователя"
    )
    def post(self, request):
        serializer = WantedListProductSerializer(data=request.data)
        if serializer.is_valid():
            wanted_list, created = WantedList.objects.get_or_create(owner=request.user)
            serializer.save(wanted=wanted_list)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WantedListProductsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Wanted List / Product"],
        operation_description="Продукт в Вишлисты пользователя",
        responses={200: WantedListProductSerializer(many=False)}
    )
    def get(self, request, wanted_id):
        wanted = get_object_or_404(WantedList, id=wanted_id)
        products = WantedListProduct.objects.filter(wanted=wanted)
        serializer = WantedListProductSerializer(products, many=True, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class WantedListProducView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Wanted List / Product"],
        operation_description="Деталь Продукт в Вишлисты пользователя",
        responses={200: WantedListProductSerializer(many=False)}
    )
    def get(self, request, wanted_product_id):
        objects = get_object_or_404(WantedListProduct, id=wanted_product_id)
        serializer = WantedListProductSerializer(objects, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=["Wanted List / Product"],
        operation_description="Обновлять Продукт в Вишлисты пользователя",
        request_body=WantedListProductSerializer,
    )
    def put(self, request, wanted_product_id):
        instance = get_object_or_404(WantedList, id=wanted_product_id)
        serializer = WantedListProductSerializer(instance=instance, data=request.data, context={"request": request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=["Wanted List / Product"],
        responses={204:  "No Content"}
    )
    def delete(self, request, wanted_product_id):
        wanted = get_object_or_404(WantedListProduct, id=wanted_product_id)
        wanted.delete()
        return Response({"message": "Удалить успешно"}, status=status.HTTP_204_NO_CONTENT)