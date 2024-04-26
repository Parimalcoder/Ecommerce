# Generated by Django 4.2.10 on 2024-02-21 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shooper_app', '0011_price_filter'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_filter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shooper_app.price_filter'),
        ),
    ]
