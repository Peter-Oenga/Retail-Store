# Generated by Django 5.0.4 on 2024-06-27 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_alter_orderitem_order_alter_orderitem_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(max_length=15000),
        ),
    ]
