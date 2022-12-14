# Generated by Django 4.1.2 on 2022-11-03 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceApp', '0002_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerceApp.product')),
            ],
        ),
    ]
