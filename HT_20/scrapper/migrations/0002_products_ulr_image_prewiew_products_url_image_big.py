# Generated by Django 4.1.5 on 2023-01-15 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='ulr_image_prewiew',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='url_image_big',
            field=models.TextField(null=True),
        ),
    ]
