# Generated by Django 4.2.1 on 2024-06-15 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comicsmxapi', '0047_alter_customer_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='apilog',
            name='method',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='orderplataformrelated',
            name='status',
            field=models.CharField(choices=[('delivery', 'Delivery'), ('paid', 'Paid'), ('failed', 'Failed'), ('shipping', 'Shipping'), ('pendding', 'Pendding to pay'), ('completed', 'Completed')], default='pending', max_length=50),
        ),
    ]
