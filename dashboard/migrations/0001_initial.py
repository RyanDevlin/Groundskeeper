# Generated by Django 2.2.3 on 2019-08-09 00:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Garden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('garden_name', models.CharField(max_length=100)),
                ('fnotif_global', models.BooleanField(default=True, verbose_name='Low Reservoir Notifications')),
                ('wnotif_global', models.BooleanField(default=True, verbose_name='Watering Notifications')),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ptype', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('moisture', models.IntegerField(default=100)),
                ('wlevel', models.IntegerField(default=100)),
                ('wlow', models.IntegerField(default=20)),
                ('wtime', models.DurationField(default=datetime.timedelta(0, 120))),
                ('has_schedule', models.BooleanField(default=False)),
                ('schedule', models.CharField(max_length=100)),
                ('fnotif', models.BooleanField(default=True, verbose_name='Low Reservoir Notifications')),
                ('wnotif', models.BooleanField(default=True, verbose_name='Watering Notifications')),
                ('prev_water', models.DateTimeField(verbose_name='Last watered')),
                ('linked', models.BooleanField(default=False, verbose_name='Plant connected to network')),
                ('wtoday', models.BooleanField(default=False, verbose_name='Watered today')),
                ('wonce', models.BooleanField(default=False, verbose_name='Watered at least once')),
                ('garden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Garden')),
            ],
        ),
    ]