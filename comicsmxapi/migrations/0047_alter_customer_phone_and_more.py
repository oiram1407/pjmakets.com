# Generated by Django 4.2.1 on 2024-06-11 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comicsmxapi', '0046_apilog_url_alter_apilog_origin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='orderplataformrelated',
            name='status',
            field=models.CharField(choices=[('completed', 'Completed'), ('pendding', 'Pendding to pay'), ('shipping', 'Shipping'), ('failed', 'Failed'), ('paid', 'Paid'), ('delivery', 'Delivery')], default='pending', max_length=50),
        ),
    ]
