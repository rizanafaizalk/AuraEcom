# Generated by Django 4.2.1 on 2023-06-13 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0004_alter_product_prodetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photos/product/multipleimages')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productapp.product')),
            ],
        ),
    ]