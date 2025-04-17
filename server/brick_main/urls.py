from django.urls import path
from brick_main.category.views import CategeorysView, CategoryDetailAPIView
from brick_main.product.views import (
    ProductsView, ProductDetaileView, ProductsByCategoryView,
    GetProductPatrsView, GetProductSetsView, GetProductMinigiureView,
    ProductSetDetaileView, GetProductByColorView, ObjProductsView,
    ObjProductDetaileView
)
from brick_main.wanted.views import (
    WantedsListView, WantedListView, AddProductToWishlistAPIView,
    WantedListProductsView, WantedListProducView
)
from brick_main.shop.views import (
    DeliveryView, ShopsView, ShopView, ShopIsActiveView, 
    ShopProductsForSellerView, ShopProductView, ShopProductsView
)


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
    path('wanted/list/product/add/', AddProductToWishlistAPIView.as_view()),
    path('wanted/<int:wanted_id>/products/', WantedListProductsView.as_view()),
    path('wanted/products/<int:wanted_product_id>/', WantedListProducView.as_view()),
    # Shop
    path('delivery/list/', DeliveryView.as_view()),
    path('shop/for/owner/', ShopsView.as_view()),
    path('shop/<int:shop_id>/for/owner/', ShopView.as_view()),
    path('shop/<int:shop_id>/activate/', ShopIsActiveView.as_view()),
    path('shop/prodcut/for/seller/', ShopProductsForSellerView.as_view()),
    path('shop/product/<int:product_id>/for/seller/', ShopProductView.as_view()),
    path('shop/<int:shop_id>/products/', ShopProductsView.as_view()),


]