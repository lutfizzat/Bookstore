# Generated by Django 3.2.3 on 2021-06-02 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_buyer_order_orderitem_product_shippingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
