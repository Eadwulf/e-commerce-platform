# Generated by Django 4.2 on 2023-05-11 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_product_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]