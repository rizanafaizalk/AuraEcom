# Generated by Django 4.2.1 on 2023-07-12 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0008_product_discounted_price_product_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
