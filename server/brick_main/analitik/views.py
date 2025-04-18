# analytics/views.py
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from brick_main.models import OrderItem
from brick_main.analitik.serializers import TopProductSerializer

TYPE_MAPPING = {
    'detal': 1,
    'nabor': 2,
    'minifigurka': 3,
    'instruktsiya': 4
}

PERIOD_MAPPING = {
    'year': 365,
    'half_year': 180,
    '3month': 90,
    'month': 30,
    'week': 7
}

def get_top_products_by_type_and_period(obj_type: int, days: int):
    now = timezone.now()
    start_date = now - timedelta(days=days)

    queryset = OrderItem.objects.filter(
        order__created_at__range=(start_date, now),
        product__obj=obj_type
    ).values(
        'product__id',
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity')[:5]

    return queryset

class ProductAnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Analitik"],
        manual_parameters=[
            openapi.Parameter('type', openapi.IN_QUERY, description="Тип продукта (detal, nabor, minifigurka, instruktsiya)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('period', openapi.IN_QUERY, description="Временные интервалы (year, half_year, 3month, month, week)", type=openapi.TYPE_STRING, required=True),
        ]
    )
    def get(self, request):
        obj_type_str = request.GET.get('type')
        period = request.GET.get('period')

        obj_type = TYPE_MAPPING.get(obj_type_str)

        if not obj_type or period not in PERIOD_MAPPING:
            return Response({'detail': 'Указан неверный тип или период'}, status=400)

        days = PERIOD_MAPPING[period]
        stats = get_top_products_by_type_and_period(obj_type, days)
        serializer = TopProductSerializer(stats, many=True)
        return Response(serializer.data)

