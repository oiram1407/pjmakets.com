# Generated by Django 4.2.1 on 2024-05-08 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comicsmxapi", "0033_alter_companiesplataformsrelated_plataform_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderplataformrelated",
            name="status",
            field=models.CharField(
                choices=[
                    ("pendding", "Pendding to pay"),
                    ("paid", "Paid"),
                    ("delivery", "Delivery"),
                    ("failed", "Failed"),
                    ("completed", "Completed"),
                    ("shipping", "Shipping"),
                ],
                default="pending",
                max_length=50,
            ),
        ),
    ]
