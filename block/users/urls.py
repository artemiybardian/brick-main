from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('verify-login/', views.verify_login, name='verify_login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-avatar/', views.change_avatar, name='change_avatar'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/clear/', views.clear_wishlist, name='clear_wishlist'),
    path('collection/', views.collection_view, name='collection'),
    path('collection/add/', views.add_to_collection, name='add_to_collection'),
    path('collection/remove/', views.remove_from_collection, name='remove_from_collection'),
    path('collection/clear/', views.clear_collection, name='clear_collection'),
] 