# Generated by Django 3.2.12 on 2023-07-11 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mastering_django', '0002_auto_20230711_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Not packed'), (4, 'delivered'), (2, 'ready for shipment'), (3, 'shipped')], default=1),
        ),
        migrations.AlterField(
            model_name='usertype',
            name='id',
            field=models.PositiveSmallIntegerField(choices=[(2, 'Seller'), (1, 'Customer')], primary_key=True, serialize=False),
        ),
    ]
