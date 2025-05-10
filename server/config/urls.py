from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.i18n import i18n_patterns
from rest_framework_simplejwt import views as jwt_views

schema_view = get_schema_view(
   openapi.Info(
      title="Brick-main API",
      default_version='v 1.0.0',
      description="Brick-main",
      terms_of_service="1",
      contact=openapi.Contact(email="istamovibrohim8@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('authen/', include('authen.urls')),
    path('api/', include('brick_main.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add media URLs for serving media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT,},),]