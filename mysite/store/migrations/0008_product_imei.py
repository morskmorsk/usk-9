# Generated by Django 4.1.5 on 2023-12-01 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_delete_category_delete_device_imei_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='imei',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
