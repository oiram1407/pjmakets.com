# Generated by Django 4.1 on 2024-03-31 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comicsmxapi", "0016_productsprice"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productsinventoryupdate",
            name="method_update",
            field=models.CharField(
                choices=[
                    ("manually", "Manually"),
                    ("mercado libre", "Mercado Libre"),
                    ("woocommerce", "WooCommerce"),
                ],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="productsprice",
            name="plataform_name",
            field=models.CharField(
                choices=[
                    ("manually", "Manually"),
                    ("mercado libre", "Mercado Libre"),
                    ("woocommerce", "WooCommerce"),
                ],
                max_length=100,
            ),
        ),
    ]