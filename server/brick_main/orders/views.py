from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.pagination import PaginationList
from utils.permissions import IsSellerRole

from brick_main.models import Order, Shops
from brick_main.orders.serializers import (
    OrdersSerializer,
    OrderStatusChangeSellerSerializer,
    OrderStatusChangeSerializer,
    OrderCreateSerializer
)


class OrdersForSellerView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSellerRole]
    serializer_class = OrdersSerializer
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=["Order"],
        operation_description="Заказы для продавца, новый заказ и все",
        manual_parameters=[
            openapi.Parameter("is_new", openapi.IN_QUERY, description="Новые заказы is_new = True", type=openapi.TYPE_STRING),
            openapi.Parameter("page", openapi.IN_QUERY, description="Номер страницы", type=openapi.TYPE_INTEGER),
            openapi.Parameter("limit", openapi.IN_QUERY, description="Элементов на странице (по умолчанию: 10): 10 можно изменить динамически", type=openapi.TYPE_INTEGER),
        ],
        responses={200: OrdersSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        shop = get_object_or_404(Shops, owner=user)
        search_query = request.query_params.get("search", None)
        queryset = Order.objects.filter(shop=shop).order_by("id")

        if search_query:
            queryset = queryset.filter(Q(is_new__icontains=search_query))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderForSellerView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSellerRole]

    @swagger_auto_schema(
        tags=["Order"],
        operation_description="Подробности заказа Seller",
        responses={200: OrdersSerializer(many=False)}
    )
    def get(self, request, order_id):
        objects = get_object_or_404(Order, id=order_id)
        serializer = OrdersSerializer(objects, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=["Order"],
        operation_description="Изменить статус заказа / для роли продавца",
        request_body=OrderStatusChangeSellerSerializer,
    )
    def put(self, request, order_id):
        instance = get_object_or_404(Order, id=order_id)
        serializer = OrderStatusChangeSellerSerializer(instance=instance, data=request.data, context={"request": request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersForuserView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrdersSerializer
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=["Order"],
        operation_description="Все заказы, принадлежащие пользователю",
        manual_parameters=[
            openapi.Parameter("page", openapi.IN_QUERY, description="Номер страницы", type=openapi.TYPE_INTEGER),
            openapi.Parameter("limit", openapi.IN_QUERY, description="Элементов на странице (по умолчанию: 10): 10 можно изменить динамически", type=openapi.TYPE_INTEGER),
        ],
        responses={200: OrdersSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        queryset = Order.objects.filter(owner=request.user).order_by("id")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=["Order"],
        operation_description="Для заказывающего пользователя",
        request_body=OrderCreateSerializer)
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderForUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Order"],
        operation_description="Подробности заказа User",
        responses={200: OrdersSerializer(many=False)}
    )
    def get(self, request, order_id):
        objects = get_object_or_404(Order, id=order_id)
        serializer = OrdersSerializer(objects, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=["Order"],
        operation_description="Изменить статус заказа / для роли User",
        request_body=OrderStatusChangeSerializer,
    )
    def patch(self, request, order_id):
        instance = get_object_or_404(Order, id=order_id)
        serializer = OrderStatusChangeSerializer(instance=instance, data=request.data, context={"request": request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)