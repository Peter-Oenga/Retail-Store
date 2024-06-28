# Generated by Django 5.0.4 on 2024-06-21 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_order_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date',
            new_name='date_ordered',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='address',
            new_name='shipping_address',
        ),
        migrations.AddField(
            model_name='order',
            name='date_shipped',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
    ]
