from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('object/', views.object_detail, name='object_detail'),
    path('objects/', views.object_list, name='object_list'),
    path('search/', views.object_search, name='object_search'),
    path('api/objects/', views.api_object_list, name='api_object_list'),
] 