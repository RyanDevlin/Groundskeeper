# Generated by Django 2.2.3 on 2019-08-12 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20190811_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='schedule',
            field=models.DateTimeField(verbose_name='Scheduled watering time'),
        ),
    ]
