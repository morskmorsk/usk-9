# Generated by Django 4.1.5 on 2023-11-30 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_workorder_customer_workorder_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ['id'], 'verbose_name_plural': 'Departments'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['id'], 'verbose_name_plural': 'Products'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_on_sale',
        ),
    ]