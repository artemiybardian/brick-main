from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.pagination import PaginationList

from brick_main.models import Obj, Theme, Links, KnownColor
from brick_main.product.serializers import (
    ProductsSerializer, ProductDetaileSerializer,
    LinksSerializer, ProductPartsDetaileSerializer
)


class ProductsView(GenericAPIView):
    serializer_class = ProductsSerializer
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=["Product"],
        operation_description="Все продукты, Paganiation, Поиск",
        manual_parameters=[
            openapi.Parameter("search", openapi.IN_QUERY, description="Поиск по item_name", type=openapi.TYPE_STRING),
            openapi.Parameter("page", openapi.IN_QUERY, description="Номер страницы", type=openapi.TYPE_INTEGER),
            openapi.Parameter("limit", openapi.IN_QUERY, description="Элементов на странице (по умолчанию: 10): 10 можно изменить динамически", type=openapi.TYPE_INTEGER),
        ],
        responses={200: ProductsSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get("search", None)
        queryset = Obj.objects.all().order_by("id")

        if search_query:
            queryset = queryset.filter(Q(item_name__icontains=search_query))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetaileView(APIView):

    @swagger_auto_schema(
        tags=["Product"],
        operation_description="Подробнее о продукте, (например, наборы и их части)",
        responses={200: ProductDetaileSerializer(many=False)}
    )
    def get(self, request, product_id):
        objects = get_object_or_404(Obj, id=product_id)
        serializer = ProductDetaileSerializer(objects, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProductSetDetaileView(APIView):

    @swagger_auto_schema(
        tags=["Product"],
        operation_description="Подробнее о продукте наборы",
        responses={200: ProductPartsDetaileSerializer(many=False)}
    )
    def get(self, request, product_id):
        objects = get_object_or_404(Obj, id=product_id)
        serializer = ProductPartsDetaileSerializer(objects, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductsByCategoryView(APIView):

    @swagger_auto_schema(
        tags=["Product"],
        operation_description="Все продукты в соответствующей категории (включая продукты в подкатегориях)",
        responses={200: ProductsSerializer(many=True)}
    )
    def get(self, request, category_id):
        theme = get_object_or_404(Theme, id=category_id)

        # Все (те же и подкатегории) идентификаторы
        categories = {theme}.union(theme.get_all_subcategories())
        category_ids = [cat.id for cat in categories]

        # Товары, относящиеся к этим категориям
        products = Obj.objects.filter(theme_obj_links__high_id__in=category_ids).distinct()

        serializer = ProductsSerializer(products, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Parts
class GetProductPatrsView(GenericAPIView):
    serializer_class = LinksSerializer
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=["Product"],
        operation_description="Список деталей продукта Parts",
        manual_parameters=[
            openapi.Parameter("page", openapi.IN_QUERY, description="Номер страницы", type=openapi.TYPE_INTEGER),
            openapi.Parameter("limit", openapi.IN_QUERY, description="Элементов на странице (по умолчанию: 10): 10 можно изменить динамически", type=openapi.TYPE_INTEGER),
        ],
        responses={200: LinksSerializer(many=True)}
    )
    def get(self, request, product_id, part_id):
        queryset = Links.objects.filter(set=product_id, part_class=part_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProductSetsView(GenericAPIView):
    serializer_class = LinksSerializer
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=["Product"],
        operation_description="Список деталей продукта Sets",
        manual_parameters=[
            openapi.Parameter("page", openapi.IN_QUERY, description="Номер страницы", type=openapi.TYPE_INTEGER),
            openapi.Parameter("limit", openapi.IN_QUERY, description="Элементов на странице (по умолчанию: 10): 10 можно изменить динамически", type=openapi.TYPE_INTEGER),
        ],
        responses={200: LinksSerializer(many=True)}
    )
    def get(self, request, product_id, set_id):
        queryset = Links.objects.filter(set=product_id, part_class=set_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProductMinigiureView(GenericAPIView):
    serializer_class = LinksSerializer
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=["Product"],
        operation_description="Список деталей продукта Minifigures",
        manual_parameters=[
            openapi.Parameter("page", openapi.IN_QUERY, description="Номер страницы", type=openapi.TYPE_INTEGER),
            openapi.Parameter("limit", openapi.IN_QUERY, description="Элементов на странице (по умолчанию: 10): 10 можно изменить динамически", type=openapi.TYPE_INTEGER),
        ],
        responses={200: LinksSerializer(many=True)}
    )
    def get(self, request, product_id, minifigure_id):
        queryset = Links.objects.filter(set=product_id, part_class=minifigure_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetProductByColorView(GenericAPIView):
    serializer_class = ProductDetaileSerializer
    pagination_class = PaginationList

    @swagger_auto_schema(
        tags=["Product"],
        operation_description="Получить продукт по цвету",
        manual_parameters=[
            openapi.Parameter("page", openapi.IN_QUERY, description="Номер страницы", type=openapi.TYPE_INTEGER),
            openapi.Parameter("limit", openapi.IN_QUERY, description="Элементов на странице (по умолчанию: 10): 10 можно изменить динамически", type=openapi.TYPE_INTEGER),
        ],
        responses={200: ProductDetaileSerializer(many=True)}
    )
    def get(self, request, color_id):
        known_colors = KnownColor.objects.filter(color__id=color_id)
        obj_ids = known_colors.values_list('obj_id', flat=True).distinct()
        queryset = Obj.objects.filter(id__in=obj_ids)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)