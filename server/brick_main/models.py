from django.db import models
from authen.models import Country, CustomUser


class Statusorder(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'status_order'
        verbose_name = "Статус Заказ"
        verbose_name_plural = "Статус Заказ"


class Deliverys(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'deliverys'
        verbose_name = "Службы доставки"
        verbose_name_plural = "Службы доставки"


class Currency(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'valyuta'
        verbose_name = "Тип валюты"
        verbose_name_plural = "Тип валюты"


class ConditionType(models.TextChoices):
    NEW = "новое", "Новый"
    OLD = "б/у:", "б/у:"


class Shops(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    address = models.CharField(max_length=250, verbose_name="Адрес магазина")
    country = models.ManyToManyField(Country, blank=True, verbose_name="Выбор, в какие страны отправляешь")
    is_openid = models.BooleanField(default=False, verbose_name="Временно закрыт")
    delivery_service = models.ForeignKey(Deliverys, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Доставка")
    currency = models.ManyToManyField(Currency, blank=True, verbose_name="Валюта магазина")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Владелец")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'shops'
        verbose_name = "Магазин"
        verbose_name_plural = "Магазин"


class Alternate(models.Model):
    """
    Модель для хранения альтернативных идентификаторов объектов.
    """
    id = models.OneToOneField('Obj', models.CASCADE, db_column='id', primary_key=True, verbose_name="Основной объект")
    item_id = models.CharField(max_length=12, blank=True, null=True, verbose_name="Альтернативный идентификатор")

    class Meta:
        db_table = 'alternate'
        verbose_name = "Альтернативный идентификатор"
        verbose_name_plural = "Альтернативные идентификаторы"

    def __str__(self):
        return f"Альтернативный ID: {self.item_id} для объекта {self.id}"


class Images(models.Model):
    """
    Модель для хранения изображений, связанных с объектами.
    """
    item = models.ForeignKey('Obj', models.CASCADE, related_name='images', verbose_name="Объект")
    color = models.TextField(verbose_name="Цвет")
    address = models.TextField(blank=True, null=True, verbose_name="URL изображения")

    class Meta:
        db_table = 'images'
        unique_together = (('item', 'color'),)
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return f"Изображение для объекта {self.item_id}, цвет: {self.color}"


class Links(models.Model):
    """
    Модель для хранения связей между объектами (например, наборы и их части).
    """
    set = models.ForeignKey('Obj', models.CASCADE, related_name='links_as_set', verbose_name="Набор")
    part = models.ForeignKey('Obj', models.CASCADE, related_name='links_as_part', verbose_name="Часть")
    set_class = models.IntegerField(verbose_name="Класс набора")
    part_class = models.IntegerField(verbose_name="Класс части")
    part_count = models.IntegerField(blank=True, null=True, verbose_name="Количество частей")
    color = models.TextField(verbose_name="Цвет")

    class Meta:
        db_table = 'links'
        unique_together = (('set', 'part', 'color'),)
        verbose_name = "Связь"
        verbose_name_plural = "Связи"
        indexes = [
            models.Index(fields=['set']),
            models.Index(fields=['part']),
        ]

    def __str__(self):
        return f"Связь: {self.set} -> {self.part}"


class Obj(models.Model):
    """
    Основная модель для хранения объектов (например, наборы, детали и т.д.).
    """
    id = models.CharField(primary_key=True, max_length=24, verbose_name="Идентификатор")
    item_name = models.TextField(verbose_name="Название объекта")
    item_class = models.IntegerField(verbose_name="Класс объекта")
    year_first_release = models.IntegerField(blank=True, null=True, verbose_name="Год первого выпуска")
    year_last_release = models.IntegerField(blank=True, null=True, verbose_name="Год последнего выпуска")
    weight = models.FloatField(blank=True, null=True, verbose_name="Вес")
    item_dim = models.TextField(blank=True, null=True, verbose_name="Размеры объекта")
    pack_dim = models.TextField(blank=True, null=True, verbose_name="Размеры упаковки")
    flat_dim = models.TextField(blank=True, null=True, verbose_name="Плоские размеры")
    stud_dim = models.TextField(blank=True, null=True, verbose_name="Размеры шпильки")
    instructions = models.BooleanField(blank=True, null=True, verbose_name="Наличие инструкций")

    class Meta:
        db_table = 'obj'
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"

    def __str__(self):
        return f"{self.item_name} ({self.id})"


class Theme(models.Model):
    """
    Модель для хранения тематических коллекций.
    """
    id = models.IntegerField(primary_key=True, verbose_name="Идентификатор")
    collection_name = models.TextField(blank=True, null=True, verbose_name="Название коллекции")
    size = models.IntegerField(blank=True, null=True, verbose_name="Размер коллекции")

    def get_all_subcategories(self):
        """Возвращает все подкатегории, включая вложенные"""
        subcategories = set()
        direct_subcats = Theme.objects.filter(id__in=self.high_links.values('low'))
        
        for subcat in direct_subcats:
            subcategories.add(subcat)
            subcategories.update(subcat.get_all_subcategories())
        
        return subcategories

    def get_all_objects(self):
        """Возвращает все объекты категории и её подкатегорий"""
        # Получаем все категории (текущую и все подкатегории)
        categories = {self}.union(self.get_all_subcategories())
        category_ids = [cat.id for cat in categories]
        
        # Получаем все объекты из всех категорий
        return Obj.objects.filter(theme_obj_links__high_id__in=category_ids).distinct()

    def get_total_objects_count(self):
        """Подсчитывает общее количество объектов в категории и всех её подкатегориях"""
        return self.get_all_objects().count()

    def get_category_path(self):
        """Возвращает путь до текущей категории в виде списка кортежей (id, name)"""
        path = [(self.id, self.collection_name)]
        
        # Ищем родительскую категорию
        parent_link = ThemeLinks.objects.filter(low=self.id).first()
        
        # Рекурсивно строим путь
        while parent_link:
            parent = parent_link.high
            path.append((parent.id, parent.collection_name))
            parent_link = ThemeLinks.objects.filter(low=parent.id).first()
        
        # Возвращаем путь в обратном порядке (от корня до текущей категории)
        return list(reversed(path))

    class Meta:
        db_table = 'theme'
        verbose_name = "Тематическая коллекция"
        verbose_name_plural = "Тематические коллекции"

    def __str__(self):
        return f"{self.collection_name} ({self.id})"


class ThemeLinks(models.Model):
    """
    Модель для хранения связей между тематическими коллекциями.
    """
    high = models.ForeignKey(Theme, models.CASCADE, related_name='high_links', verbose_name="Родительская коллекция")
    low = models.ForeignKey(Theme, models.CASCADE, related_name='low_links', verbose_name="Дочерняя коллекция")

    class Meta:
        db_table = 'theme_links'
        unique_together = (('high', 'low'),)
        verbose_name = "Связь тематических коллекций"
        verbose_name_plural = "Связи тематических коллекций"
        indexes = [
            models.Index(fields=['high']),
            models.Index(fields=['low']),
        ]

    def __str__(self):
        return f"Связь: {self.high} -> {self.low}"


class ThemeObjLinks(models.Model):
    """
    Модель для хранения связей между тематическими коллекциями и объектами.
    """
    high = models.ForeignKey(Theme, models.CASCADE, related_name='theme_obj_links', verbose_name="Коллекция")
    obj = models.ForeignKey(Obj, models.CASCADE, related_name='theme_obj_links', verbose_name="Объект")

    class Meta:
        db_table = 'theme_obj_links'
        unique_together = (('high', 'obj'),)
        verbose_name = "Связь коллекции и объекта"
        verbose_name_plural = "Связи коллекций и объектов"
        indexes = [
            models.Index(fields=['high']),
            models.Index(fields=['obj']),
        ]

    def __str__(self):
        return f"Связь: {self.high} -> {self.obj}"


class Color(models.Model):
    """
    Официальные цвета LEGO.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    class Meta:
        db_table = 'color'
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"

    def __str__(self):
        return self.name


class KnownColor(models.Model):
    """
    Указывает, в каких цветах доступна определённая деталь (объект).
    """
    obj = models.ForeignKey(Obj, models.CASCADE, related_name='known_colors', verbose_name="Деталь")
    color = models.ForeignKey(Color, models.CASCADE, related_name='known_in_objects', verbose_name="Цвет")

    class Meta:
        db_table = 'known_color'
        unique_together = (('obj', 'color'),)
        verbose_name = "Известный цвет"
        verbose_name_plural = "Известные цвета"
        indexes = [
            models.Index(fields=['obj']),
            models.Index(fields=['color']),
        ]

    def __str__(self):
        return f"{self.obj} доступен в цвете: {self.color}"


class ObjProduct(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    description = models.CharField(max_length=250, verbose_name="Описание")
    image = models.URLField(null=True, blank=True, verbose_name="URL-адрес изображения")
    quantity = models.CharField(max_length=250, verbose_name="Количество")
    condition = models.CharField(max_length=100, null=True, blank=True, choices=ConditionType.choices, verbose_name="Состояние")
    obj = models.ForeignKey(Obj, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Объект")
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Магазин")
    country = models.ManyToManyField(Country, null=True, blank=True, verbose_name="Продавец отправляет товар")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Владелец")
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'obj_product'
        verbose_name = "Объект продукта"
        verbose_name_plural = "Объект продукта"


class ObjProductPrice(models.Model):
    product = models.ForeignKey(ObjProduct, on_delete=models.CASCADE, null=True, blank=True, related_name="product_price", verbose_name="Продукт")
    price = models.CharField(max_length=250, null=True, blank=True, verbose_name="Цена")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Валюта")

    class Meta:
        db_table = 'product_price'
        verbose_name = "Цена продукта"
        verbose_name_plural = "Цена продукта"


class WantedList(models.Model):
    name = models.CharField(max_length=250, verbose_name="имя")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Владелец")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'wanted_list'
        verbose_name = "Вишлисты"
        verbose_name_plural = "Вишлисты"


class WantedListProduct(models.Model):
    wanted = models.ForeignKey(WantedList, on_delete=models.CASCADE, null=True, blank=True, related_name="wanted_product", verbose_name="Вишлисты")
    product = models.ForeignKey(ObjProduct, on_delete=models.CASCADE, null=True, blank=True, verbose_name="продукта")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Цвета")
    quantity = models.IntegerField(null=True, blank=True, verbose_name="Количество")

    def __str__(self):
        return f"Вишлисты: {self.wanted.name} - продукт: {self.product.name}"
    
    class Meta:
        db_table = 'wanted_list_product'
        verbose_name = "Вишлисты продукт"
        verbose_name_plural = "Вишлисты продукта"


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Клиент")
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE, verbose_name="Магазин")
    is_new = models.BooleanField(default=True, verbose_name="Новый заказ")
    delivery = models.ForeignKey(Deliverys, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(Statusorder, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"{self.user.username} - {self.shop.name} - {self.created_at.strftime('%Y-%m-%d')}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items_product", verbose_name="Заказ")
    product = models.ForeignKey(ObjProduct, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(verbose_name="Число")

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    class Meta:
        db_table = "order_item"
        verbose_name = "Заказать продукцию"
        verbose_name_plural = "Заказать продукцию"