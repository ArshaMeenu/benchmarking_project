# Generated by Django 3.2.12 on 2023-07-11 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mastering_django', '0003_auto_20230711_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Not packed'), (3, 'shipped'), (4, 'delivered'), (2, 'ready for shipment')], default=1),
        ),
    ]
