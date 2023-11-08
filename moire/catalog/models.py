from django.db import models
from django.db.models import Count
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название цвета")
    code = models.CharField(max_length=50, verbose_name="Код цвета")

    def __str__(self):
        return self.name


class Galery(models.Model):
    img = models.URLField(verbose_name="Адрес изображения")


class Category(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(unique=True, verbose_name="Символьный код")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["-id"]

    def __str__(self):
        return self.title

    def count_items(self):
        return self.items.count()


class Item(models.Model):
    class Material(models.TextChoices):
        LINEN = "LN", _("Лен")
        COTTON = "CT", _("Хлопок")
        WOOL = "WL", _("Шерсть")
        SILK = "SL", _("Шелк")

    class Collections(models.TextChoices):
        SUMMER = "SM", _("Лето")
        WINTER = "WN", _("Зима")
        AUTUMN = "AU", _("Осень")
        SPRING = "SP", _("Весна")

    material = models.CharField(
        max_length=200,
        choices=Material.choices,
        blank=True,
        default=Material.SILK,
        verbose_name="Материал",
    )
    collection = models.CharField(
        max_length=200,
        choices=Collections.choices,
        blank=True,
        default=Collections.WINTER,
        verbose_name="Коллекция",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Категория товара",
    )
    title = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(unique=True, verbose_name="Символьный код")
    image = models.URLField(verbose_name="Адрес изображения")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Цена"
    )
    quantity = models.PositiveIntegerField(
        default=0, verbose_name="Количество на складе"
    )
    availability = models.BooleanField(default=True, verbose_name="Доступность")
    number_of_views = models.PositiveIntegerField(
        default=0, verbose_name="Кол-во просмотров"
    )
    number_of_sales = models.PositiveIntegerField(
        default=0, verbose_name="Кол-во покупок"
    )
    colors = models.ManyToManyField(Color, blank=True, verbose_name="Цвета")
    images = models.ManyToManyField(Galery, blank=True, verbose_name="Галерея")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-id"]

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.availability == True:
            self.availability = False
        if self.availability == False:
            self.hard_delete()
        self.save()

    def hard_delete(self, *args, **kwargs):
        self.delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "catalog_app:product_detail",
            args=[self.slug],
        )

    def add_view(self):
        self.number_of_views += 1
        self.save()

    def add_sels(self):
        self.number_of_sales += 1
        self.save()
