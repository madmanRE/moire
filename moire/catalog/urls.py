from django.urls import path
from .views import index, CatalogView, CategoryView, product_filter, ItemDetailView

app_name = "catalog_app"

urlpatterns = [
    path("", index, name="index"),
    path("catalog/filter/", product_filter, name="product_filter"),
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("catalog/<slug:cat_slug>/", CategoryView.as_view(), name="category"),
    path(
        "catalog/product/<int:pk>/",
        ItemDetailView.as_view(),
        name="item_detail",
    ),
]
