# Generated by Django 4.2.1 on 2024-05-01 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comicsmxapi", "0031_alter_productsrelatedplataform_product_plataform_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderplataformrelated",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("completed", "Completed"),
                    ("paid", "Paid"),
                    ("delivery", "Delivery"),
                    ("failed", "Faild"),
                    ("shipping", "Shipping"),
                ],
                default="pending",
                max_length=50,
            ),
        ),
    ]