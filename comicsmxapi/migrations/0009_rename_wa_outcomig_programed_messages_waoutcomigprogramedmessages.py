# Generated by Django 4.1 on 2024-03-21 05:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "comicsmxapi",
            "0008_rename_waoutcomigprogramedmessage_wa_outcomig_programed_messages",
        ),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Wa_Outcomig_Programed_Messages",
            new_name="WaOutcomigProgramedMessages",
        ),
    ]