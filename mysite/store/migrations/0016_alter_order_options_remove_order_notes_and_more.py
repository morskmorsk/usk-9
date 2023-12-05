# Generated by Django 4.1.5 on 2023-12-03 00:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0015_payment_paymentorder'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-updated_at'], 'verbose_name_plural': 'Orders'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipped_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_cost',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_method',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_phone',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_state',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_zip_code',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.RemoveField(
            model_name='order',
            name='subtotal',
        ),
        migrations.RemoveField(
            model_name='order',
            name='tracking_number',
        ),
        migrations.RemoveField(
            model_name='order',
            name='tracking_url',
        ),
        migrations.AddField(
            model_name='order',
            name='sub_total',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]