# Generated by Django 3.2.12 on 2023-07-20 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mastering_django', '0009_auto_20230718_0500'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]