# Generated by Django 5.0.3 on 2024-03-27 05:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_alter_category_options_product_is_on_sale_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "categories"},
        ),
    ]
