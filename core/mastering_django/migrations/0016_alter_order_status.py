# Generated by Django 3.2.12 on 2023-08-11 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mastering_django', '0015_auto_20230804_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(3, 'shipped'), (4, 'delivered'), (1, 'not packed'), (2, 'ready for shipment')], default=1),
        ),
    ]
