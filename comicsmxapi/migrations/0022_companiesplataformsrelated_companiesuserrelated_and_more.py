# Generated by Django 4.1 on 2024-04-10 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("comicsmxapi", "0021_companieuserrelated_company"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompaniesPlataformsRelated",
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
                (
                    "plataform",
                    models.CharField(
                        choices=[
                            ("mercado-libre", "Mercado Libre"),
                            ("woocommerce", "WooCommerce"),
                        ],
                        max_length=250,
                    ),
                ),
                ("data", models.TextField(max_length=10000)),
                (
                    "status",
                    models.CharField(
                        choices=[("Active", "Active"), ("Inactive", "Inactive")],
                        default="Active",
                        max_length=50,
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
        migrations.CreateModel(
            name="CompaniesUserRelated",
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
                (
                    "status",
                    models.CharField(
                        choices=[("Active", "Active"), ("Inactive", "Inactive")],
                        default="Active",
                        max_length=50,
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
        migrations.AddField(
            model_name="companie",
            name="status",
            field=models.CharField(
                choices=[("Active", "Active"), ("Inactive", "Inactive")],
                default="Active",
                max_length=50,
            ),
        ),
        migrations.DeleteModel(
            name="CompanieUserRelated",
        ),
        migrations.AddField(
            model_name="companiesuserrelated",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="comicsmxapi.companie"
            ),
        ),
        migrations.AddField(
            model_name="companiesuserrelated",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="companiesuserrelated",
            name="user_company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_company",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="companiesplataformsrelated",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="comicsmxapi.companie"
            ),
        ),
        migrations.AddField(
            model_name="companiesplataformsrelated",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
