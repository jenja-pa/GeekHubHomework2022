# Generated by Django 4.1.5 on 2023-01-15 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0003_rename_products_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='ulr_image_prewiew',
            new_name='ulr_image_preview',
        ),
    ]
