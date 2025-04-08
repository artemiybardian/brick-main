from django.db import models
from django.contrib.auth import get_user_model


class MainCategory(models.Model):
    name = models.CharField(max_length=250, verbose_name="Имя")
    logo = models.ImageField(upload_to="category")

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=250, verbose_name="Имя")
    category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, null=True, blank=True, related_name="sub_category", verbose_name="Основная категория")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return f"Основная категория: {self.category.name} - подкатегория: {self.name}"