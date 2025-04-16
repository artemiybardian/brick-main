from django.urls import path
from brick_main.category.views import CategeorysView, CategoryDetailAPIView
from brick_main.product.views import (
    ProductsView, ProductDetaileView, ProductsByCategoryView,
    GetProductPatrsView, GetProductSetsView, GetProductMinigiureView,
    ProductSetDetaileView, GetProductByColorView, ObjProductsView,
    ObjProductDetaileView
)
from brick_main.wanted.views import WantedsListView, WantedListView


urlpatterns = [
    # Category
    path('categorys/main/', CategeorysView.as_view()),
    path('categories/<int:category_id>/', CategoryDetailAPIView.as_view()),
    # Obj
    path('products/', ProductsView.as_view()),
    path('product/<str:product_id>/', ProductDetaileView.as_view()),
    path('set/product/<str:product_id>/detaile/', ProductSetDetaileView.as_view()),
    path('product/by/ctageory/<int:category_id>/', ProductsByCategoryView.as_view()),
    path('product/<str:product_id>/parts/<int:part_id>/', GetProductPatrsView.as_view()),
    path('product/<str:product_id>/set/<int:set_id>/', GetProductSetsView.as_view()),
    path('product/<str:product_id>/minitfigure/<int:minifigure_id>/', GetProductMinigiureView.as_view()),
    path('product/by/color/<int:color_id>/', GetProductByColorView.as_view()),
    # Obj Pruduct
    path('obj/<str:product_id>/product/', ObjProductsView.as_view()),
    path('obj/product/<int:product_id>/detaile/', ObjProductDetaileView.as_view()),
    # Wanted
    path('wanted/list/', WantedsListView.as_view()),
    path('wanted/<int:pk>/list/', WantedListView.as_view()),


]