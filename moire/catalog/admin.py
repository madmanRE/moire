from django.contrib import admin
from .models import Item, Category, Color, Galery


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Galery)
class GaleryAdmin(admin.ModelAdmin):
    list_display = ["img"]


class ColorInline(admin.TabularInline):
    model = Item.colors.through
    extra = 3


class GaleryInline(admin.TabularInline):
    model = Item.images.through
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "description", "show_how_many_items_in"]
    prepopulated_fields = {"slug": ("title",)}

    def show_how_many_items_in(self, cat):
        return cat.count_items()

    show_how_many_items_in.short_description = "Товаров в категории"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
        "image",
        "price",
        "quantity",
        "availability",
        "category",
        "material",
        "collection",
    ]
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ["category"]
    search_fields = ["title", "description"]
    inlines = [ColorInline, GaleryInline]
