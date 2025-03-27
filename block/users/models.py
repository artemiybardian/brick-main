from django.db import models
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from database.models import Obj
from datetime import date
from django.utils import timezone
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import os
from .data.cities import CITIES_DATA
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    # Группы пользователя
    class UserGroup(models.TextChoices):
        BUYER = 'buyer', _('Покупатель')
        SELLER = 'seller', _('Продавец')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')

    # Валюты
    class Currency(models.TextChoices):
        RUB = 'RUB', _('Российский рубль')
        USD = 'USD', _('Доллар США')
        EUR = 'EUR', _('Евро')

    # Языки
    class Language(models.TextChoices):
        RU = 'ru', _('Русский')
        EN = 'en', _('Английский')

    # Дополнительные поля
    email = models.EmailField(unique=True, verbose_name="Электронная почта", db_index=True)
    #nickname = models.CharField(max_length=50, verbose_name="Имя", db_index=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    #country = models.CharField(max_length=100, verbose_name="Страна", blank=True)
    country = models.CharField(
        max_length=2,
        choices=[(code, data['name']) for code, data in CITIES_DATA.items()],
        default='RU',
        verbose_name="Страна"
    )

    city = models.CharField(max_length=100, verbose_name="Город", blank=True)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.RUB, verbose_name="Валюта")
    language = models.CharField(max_length=20, choices=Language.choices, default=Language.RU, verbose_name="Язык")
    user_group = models.CharField(max_length=20, choices=UserGroup.choices, default=UserGroup.BUYER, verbose_name="Группа пользователя")
    collection = models.ManyToManyField(Obj, related_name="collection_users", blank=True, verbose_name="Коллекция")
    # Переопределение полей для исключения конфликтов
    groups = models.ManyToManyField(Group, related_name="custom_users", blank=True, verbose_name="Группы")
    user_permissions = models.ManyToManyField(Permission, related_name="custom_users", blank=True, verbose_name="Права пользователя")
    email_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")

    def clean(self):
            print("Запуск clean()")
            super().clean()
            print(self.date_of_birth)
            if self.date_of_birth and self.date_of_birth > date.today():
                raise ValidationError({'date_of_birth': 'Дата рождения не может быть в будущем'})
            
            if self.country not in dict(CITIES_DATA).keys():
                raise ValidationError({'country': 'Неверный код страны.'})

            if self.city and self.country in CITIES_DATA:
                allowed_cities = CITIES_DATA[self.country]['cities']
                if self.city not in allowed_cities:
                    raise ValidationError({'city': f"Город '{self.city}' не относится к стране {CITIES_DATA[self.country]['name']}"})

    def save(self, *args, **kwargs):
        skip_clean = kwargs.pop('skip_clean', False)

        # Проверяем, новый ли это пользователь
        if not self.pk:  
            must_validate = True  # Новый пользователь, выполняем валидацию
        else:
            old_user = CustomUser.objects.filter(pk=self.pk).first()
            must_validate = old_user and (
                old_user.country != self.country or old_user.city != self.city
            )

        if not skip_clean and must_validate:
            self.clean()

        super().save(*args, **kwargs)


    def add_to_wishlist(self, obj, quantity=1):
        """Добавить предмет в вишлист"""
        WishlistItem.objects.update_or_create(
            user=self,
            obj=obj,
            defaults={'quantity': quantity}
        )

    def remove_from_wishlist(self, obj):
        """Удалить предмет из вишлиста"""
        WishlistItem.objects.filter(user=self, obj=obj).delete()

    def get_wishlist_items(self):
        """Получить все предметы в вишлисте"""
        return self.wishlist_items.all()

    def __str__(self):
        return self.username

    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/static/users/images/default-avatar.png'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
        ]


User = get_user_model()

class WishlistItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="wishlist_items")
    obj = models.ForeignKey(Obj, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        verbose_name="Количество"
    )
    color = models.CharField(max_length=50, default='Default', verbose_name="Цвет")
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "obj", "color")
        verbose_name = "Предмет вишлиста"
        verbose_name_plural = "Предметы вишлиста"

    def __str__(self):
        return f"{self.obj.item_name} ({self.color}) x{self.quantity} ({self.user.username})"

class CollectionItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="collection_items")
    obj = models.ForeignKey(Obj, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        verbose_name="Количество"
    )
    color = models.CharField(max_length=50, default='Default', verbose_name="Цвет")
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "obj", "color")
        verbose_name = "Предмет коллекции"
        verbose_name_plural = "Предметы коллекции"

    def __str__(self):
        return f"{self.obj.item_name} ({self.color}) x{self.quantity} ({self.user.username})"

class LoginVerificationCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()
    

