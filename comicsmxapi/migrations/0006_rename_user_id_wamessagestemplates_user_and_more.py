# Generated by Django 4.1 on 2024-03-20 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("comicsmxapi", "0005_wamessagestemplates_user_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="wamessagestemplates",
            old_name="user_id",
            new_name="user",
        ),
        migrations.RenameField(
            model_name="waoutcomminglog",
            old_name="template_sent",
            new_name="template",
        ),
        migrations.RenameField(
            model_name="waoutcomminglog",
            old_name="user_id",
            new_name="user",
        ),
    ]