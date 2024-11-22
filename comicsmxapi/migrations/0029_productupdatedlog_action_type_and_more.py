# Generated by Django 4.1 on 2024-04-21 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comicsmxapi", "0028_orderplataformrelated_date_order_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productupdatedlog",
            name="action_type",
            field=models.CharField(
                choices=[("increment", "Increment"), ("decrement", "Decrement")],
                default="increment",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="orderplataformrelated",
            name="order_plataform_id",
            field=models.CharField(max_length=500, unique=True),
        ),
    ]
