# Generated by Django 4.2.1 on 2024-05-09 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comicsmxapi", "0034_alter_orderplataformrelated_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderplataformrelated",
            name="status",
            field=models.CharField(
                choices=[
                    ("pendding", "Pendding to pay"),
                    ("completed", "Completed"),
                    ("paid", "Paid"),
                    ("shipping", "Shipping"),
                    ("failed", "Failed"),
                    ("delivery", "Delivery"),
                ],
                default="pending",
                max_length=50,
            ),
        ),
    ]