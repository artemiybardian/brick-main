"""
URL-маршруты приложения базы данных BRICK.

Этот файл определяет все URL-маршруты, связанные с работой с базой данных:
- API-эндпоинты для работы с объектами
- API-эндпоинты для работы с категориями
- API-эндпоинты для работы с наборами
- API-эндпоинты для работы с цветами
- API-эндпоинты для работы с годами выпуска

Все маршруты используют представления из views.py и возвращают данные в формате JSON.
API версионируется для обеспечения обратной совместимости при обновлении.
"""

from django.urls import path
from . import views

urlpatterns = [
    # API v1 - текущая версия
    path('api/v1/objects/', views.api_object_list, name='api_v1_object_list'),  # Список всех объектов
    path('api/v1/objects/<int:obj_id>/', views.api_object_detail, name='api_v1_object_detail'),  # Детальная информация об объекте
    
    # API v1 - категории
    path('api/v1/categories/', views.api_category_list, name='api_v1_category_list'),  # Список всех категорий
    path('api/v1/categories/<int:category_id>/', views.api_category_detail, name='api_v1_category_detail'),  # Детальная информация о категории
    path('api/v1/categories/<int:category_id>/objects/', views.api_category_objects, name='api_v1_category_objects'),  # Объекты в категории
    
    # API v1 - наборы
    path('api/v1/sets/', views.api_set_list, name='api_v1_set_list'),  # Список всех наборов
    path('api/v1/sets/<int:set_id>/', views.api_set_detail, name='api_v1_set_detail'),  # Детальная информация о наборе
    path('api/v1/sets/<int:set_id>/parts/', views.api_set_parts, name='api_v1_set_parts'),  # Части набора
    
    # API v1 - цвета
    path('api/v1/colors/', views.api_color_list, name='api_v1_color_list'),  # Список всех цветов
    path('api/v1/colors/<int:color_id>/', views.api_color_detail, name='api_v1_color_detail'),  # Детальная информация о цвете
    
    # API v1 - годы выпуска
    path('api/v1/years/', views.api_year_list, name='api_v1_year_list'),  # Список всех годов выпуска
    path('api/v1/years/<int:year>/', views.api_year_detail, name='api_v1_year_detail'),  # Детальная информация о годе выпуска
    
    # Редирект со старой версии API на новую
    path('api/objects/', views.api_object_list, name='api_object_list'),  # Редирект на v1
    path('api/categories/', views.api_category_list, name='api_category_list'),  # Редирект на v1
    path('api/sets/', views.api_set_list, name='api_set_list'),  # Редирект на v1
    path('api/colors/', views.api_color_list, name='api_color_list'),  # Редирект на v1
    path('api/years/', views.api_year_list, name='api_year_list'),  # Редирект на v1
] 