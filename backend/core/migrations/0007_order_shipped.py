# Generated by Django 5.0.4 on 2024-06-27 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_profile_old_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
    ]
