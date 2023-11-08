# Generated by Django 4.2.6 on 2023-11-08 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("catalog", "0006_galery_alter_item_collection_alter_item_material_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="ФИО")),
                ("address", models.CharField(max_length=250, verbose_name="Адрес")),
                ("phone", models.CharField(max_length=50, verbose_name="Телефон")),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="Электронная почта"),
                ),
                (
                    "comment",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Комментарий",
                    ),
                ),
                (
                    "delivery",
                    models.CharField(
                        choices=[("SD", "Self Delivery"), ("CO", "Courier")],
                        default="SD",
                        max_length=150,
                        verbose_name="Способ доставки",
                    ),
                ),
                (
                    "paid_variant",
                    models.CharField(
                        choices=[("CARD", "Card"), ("CASH", "Cash")],
                        default="CARD",
                        max_length=150,
                        verbose_name="Способ оплаты",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("paid", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="orders.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_item",
                        to="catalog.item",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="order",
            index=models.Index(
                fields=["-created_at"], name="orders_orde_created_f0ce29_idx"
            ),
        ),
    ]