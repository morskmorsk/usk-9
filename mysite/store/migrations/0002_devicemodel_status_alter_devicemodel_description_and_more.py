# Generated by Django 4.1.5 on 2023-11-17 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicemodel',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.devicestatus'),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='description',
            field=models.TextField(blank=True, default='N/A', null=True),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.devicegrade'),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.devicemanufacturer'),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='model_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='model_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='warranty_period',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
