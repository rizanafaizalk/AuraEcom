# Generated by Django 4.2.1 on 2023-07-18 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0003_cart_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
