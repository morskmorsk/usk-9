# Generated by Django 4.1.5 on 2023-11-21 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_workorderdetail_service'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workorderdetail',
            old_name='service',
            new_name='service_detail',
        ),
    ]
