# Generated by Django 4.2.1 on 2024-06-01 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comicsmxapi', '0039_alter_orderplataformrelated_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplataformrelated',
            name='status',
            field=models.CharField(choices=[('shipping', 'Shipping'), ('pendding', 'Pendding to pay'), ('delivery', 'Delivery'), ('failed', 'Failed'), ('paid', 'Paid'), ('completed', 'Completed')], default='pending', max_length=50),
        ),
    ]