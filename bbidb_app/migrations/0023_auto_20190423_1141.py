# Generated by Django 2.2 on 2019-04-23 10:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bbidb_app', '0022_auto_20190423_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 23, 10, 41, 27, 364861, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_used',
            field=models.DateField(default=datetime.datetime(2019, 4, 23, 10, 41, 27, 380481, tzinfo=utc)),
        ),
    ]
