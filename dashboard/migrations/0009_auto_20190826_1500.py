# Generated by Django 2.2.3 on 2019-08-26 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20190826_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='monthday',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='plant',
            name='monthon',
            field=models.BooleanField(default=False, verbose_name='True if watering once every month'),
        ),
    ]
