# Generated by Django 4.2 on 2023-04-21 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='total_cost',
            new_name='total',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='total_cost',
            new_name='sub_total',
        ),
    ]
