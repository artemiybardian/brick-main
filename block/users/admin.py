from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.apps import apps
from front.models import MainCategory, SubCategory

# Перечень моделей, которые вы хотите оставить в админке
EXCLUDE_MODELS = [
    'CustomUser',  # Пример модели, которую оставляем в админке
]


# Получаем список всех моделей, зарегистрированных в проекте
all_models = apps.get_models()

for model in all_models:
    model_name = model.__name__
    
    # Проверяем, если модель не входит в список оставляемых, то убираем её из админки
    if model_name not in EXCLUDE_MODELS:
        try:
            admin.site.unregister(model)
        except admin.sites.NotRegistered:
            pass  # Если модель не зарегистрирована, игнорируем ошибку

admin.site.register(MainCategory)
admin.site.register(SubCategory)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Убираем поле 'id' из списка и не добавляем action_checkbox вручную
    list_display = ('id', 'username', 'email', 'user_group', 'country', 'city')

    # Определяем только поля, которые нужно отображать в формах
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('email', 'date_of_birth', 'country', 'city')}),
        ('Настройки', {'fields': ('currency', 'language', 'user_group')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

