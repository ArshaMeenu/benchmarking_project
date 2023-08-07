# Generated by Django 3.2.12 on 2023-08-04 04:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mastering_django', '0013_auto_20230803_0518'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='datetime_of_payment',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.IntegerField(choices=[(1, 'SUCCESS'), (2, 'FAILURE'), (3, 'PENDING')], default=3),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_signature',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='total_amount',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(3, 'shipped'), (2, 'ready for shipment'), (1, 'Not packed'), (4, 'delivered')], default=1),
        ),
        migrations.CreateModel(
            name='ProductInOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.FloatField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mastering_django.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mastering_django.product')),
            ],
            options={
                'unique_together': {('order', 'product')},
            },
        ),
    ]
