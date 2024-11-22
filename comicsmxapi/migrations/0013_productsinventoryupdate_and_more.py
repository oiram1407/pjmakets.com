# Generated by Django 4.1 on 2024-03-27 05:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("comicsmxapi", "0012_alter_productsinventory_quantity_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductsInventoryUpdate",
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
                ("quantity", models.IntegerField(default=0)),
                (
                    "method_update",
                    models.CharField(
                        choices=[
                            ("Manually", "Manually"),
                            ("Meli", "Meli"),
                            ("WooCommerce", "WooCommerce"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "date_published",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date published"
                    ),
                ),
                (
                    "date_updated",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
            ],
        ),
        migrations.RenameField(
            model_name="productsinventory",
            old_name="sku",
            new_name="product",
        ),
        migrations.AddField(
            model_name="wamessagestemplates",
            name="status",
            field=models.IntegerField(
                choices=[(1, "Active"), (0, "Inactive")], default=1
            ),
        ),
        migrations.RenameModel(
            old_name="Products",
            new_name="Product",
        ),
        migrations.DeleteModel(
            name="Products_Inventory_Update",
        ),
        migrations.AddField(
            model_name="productsinventoryupdate",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="comicsmxapi.product"
            ),
        ),
        migrations.AddField(
            model_name="productsinventoryupdate",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]