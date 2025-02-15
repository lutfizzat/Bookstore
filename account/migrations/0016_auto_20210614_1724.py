# Generated by Django 3.2.3 on 2021-06-14 09:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('account', '0015_auto_20210611_2221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=200, null=True)),
                ('apartment_address', models.CharField(max_length=200, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('zip', models.CharField(max_length=200)),
                ('save_info', models.BooleanField(default=False)),
                ('default', models.BooleanField(default=False)),
                ('use_default', models.BooleanField(default=False)),
                ('payment_choice', models.CharField(choices=[('S', 'Stripe'), ('P', 'Paypal')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('category', models.CharField(choices=[('horror', 'horror'), ('thriller', 'thriller'), ('romance', 'romance'), ('supernatural', 'supernatural'), ('action', 'action')], max_length=20, null=True)),
                ('price', models.PositiveIntegerField(default=False, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('quantity', models.PositiveIntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('digital', models.BooleanField(default=False, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('description', models.TextField(default=False, null=True)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='ebooks',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='order',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='owner',
        ),
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='date_ordered',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.AddField(
            model_name='account',
            name='address1',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address line 1'),
        ),
        migrations.AddField(
            model_name='account',
            name='address2',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address line 2'),
        ),
        migrations.AddField(
            model_name='account',
            name='city',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='account',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Date of birth'),
        ),
        migrations.AddField(
            model_name='account',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='account',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='account',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AddField(
            model_name='account',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='account',
            name='zip_code',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Postal Code'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='ShippingAddress',
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.address'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='item',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.item'),
        ),
    ]
