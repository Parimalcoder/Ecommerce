# Generated by Django 4.0.3 on 2024-04-05 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shooper_app', '0034_product_main_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='main_category',
        ),
    ]
