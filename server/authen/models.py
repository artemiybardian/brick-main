from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    name = models.CharField(max_length=250, verbose_name="Страна")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "country"
        verbose_name = "01. Страна"
        verbose_name_plural = "01. Страна"


class City(models.Model):
    name = models.CharField(max_length=250, verbose_name="Город")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Страна")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "city"
        verbose_name = "02. Город"
        verbose_name_plural = "02. Город"


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True, verbose_name="Аватар")
    birth_date = models.DateField(verbose_name="День рождения", null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Страна")
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Город")
    is_email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=250, null=True, blank=True, verbose_name="проверочный код")

    def __str__(self):
        return self.username

    class Meta:
        db_table = "custumer_user"
        verbose_name = "03. Пользователи"
        verbose_name_plural = "03. Пользователи"