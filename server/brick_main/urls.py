from django.urls import path
from brick_main.category.views import CategeorysView, CategoryDetailAPIView


urlpatterns = [
    path('categorys/main/', CategeorysView.as_view()),
    path('categories/<int:category_id>/', CategoryDetailAPIView.as_view()),


]