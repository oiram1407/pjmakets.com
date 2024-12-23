# Generated by Django 4.2.1 on 2024-06-06 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comicsmxapi', '0045_apilog_origin_alter_orderplataformrelated_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='apilog',
            name='url',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='apilog',
            name='origin',
            field=models.CharField(default=None, max_length=300),
        ),
        migrations.AlterField(
            model_name='orderplataformrelated',
            name='status',
            field=models.CharField(choices=[('pendding', 'Pendding to pay'), ('delivery', 'Delivery'), ('failed', 'Failed'), ('completed', 'Completed'), ('shipping', 'Shipping'), ('paid', 'Paid')], default='pending', max_length=50),
        ),
    ]
