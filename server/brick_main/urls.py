from django.urls import path
from brick_main.category.views import CategeorysView, CategoryDetailAPIView
from brick_main.product.views import ProductsView, ProductDetaileView, ProductsByCategoryView


urlpatterns = [
    # Category
    path('categorys/main/', CategeorysView.as_view()),
    path('categories/<int:category_id>/', CategoryDetailAPIView.as_view()),
    # Product
    path('products/', ProductsView.as_view()),
    path('product/<str:product_id>/', ProductDetaileView.as_view()),
    path('product/by/ctageory/<int:category_id>/', ProductsByCategoryView.as_view()),


]