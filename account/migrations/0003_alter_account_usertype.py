# Generated by Django 3.2.3 on 2021-06-02 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_account_usertype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='usertype',
            field=models.CharField(choices=[('Administrator', 'Administrator'), ('Buyer', 'Buyer')], default='Administrator', max_length=30),
        ),
    ]
