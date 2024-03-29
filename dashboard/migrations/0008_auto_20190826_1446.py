# Generated by Django 2.2.3 on 2019-08-26 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20190826_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='weekon',
            field=models.BooleanField(default=False, verbose_name='True if watering once every week'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='schedule_freq',
            field=models.CharField(choices=[('1', 'day'), ('2', 'other day'), ('3', 'week'), ('4', 'month from today')], default='1', max_length=3, verbose_name='Scheduled watering frequency'),
        ),
    ]
