# Generated by Django 3.2.3 on 2021-06-11 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_auto_20210607_1434'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Buyer',
            new_name='Profile',
        ),
    ]
