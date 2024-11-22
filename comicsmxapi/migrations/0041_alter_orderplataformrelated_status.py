# Generated by Django 4.2.1 on 2024-06-06 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comicsmxapi', '0040_alter_orderplataformrelated_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplataformrelated',
            name='status',
            field=models.CharField(choices=[('delivery', 'Delivery'), ('completed', 'Completed'), ('failed', 'Failed'), ('pendding', 'Pendding to pay'), ('shipping', 'Shipping'), ('paid', 'Paid')], default='pending', max_length=50),
        ),
    ]