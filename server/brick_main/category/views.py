from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404
from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from brick_main.models import Theme, ThemeLinks
from brick_main.category.serializers import ThemesSerializer, ObjectSerializer


class CategeorysView(APIView):

    @swagger_auto_schema(
        tags=["Category"],
        operation_description="Все категории",
        responses={200: ThemesSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        root_categories = Theme.objects.exclude(
            id__in=ThemeLinks.objects.values('low')
        )
        serializer = ThemesSerializer(root_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDetailAPIView(APIView):
    """
    Полная информация о категории: подкатегории и объекты
    """
    @swagger_auto_schema(
        tags=["Category"],
        operation_description="Полная информация о категории: подкатегории и объекты",
        responses={200: ThemesSerializer(many=True)}
    )
    def get(self, request, category_id):
        category = get_object_or_404(Theme, id=category_id)

        subcategories = Theme.objects.filter(
            id__in=ThemeLinks.objects.filter(high=category).values('low')
        )

        objects = category.get_all_objects().order_by('item_name')

        return Response({
            'current_category': ThemesSerializer(category).data,
            'subcategories': ThemesSerializer(subcategories, many=True).data,
            'objects': ObjectSerializer(objects, many=True).data
        }, status=status.HTTP_200_OK)