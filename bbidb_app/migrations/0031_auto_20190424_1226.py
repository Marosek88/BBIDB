# Generated by Django 2.2 on 2019-04-24 11:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bbidb_app', '0030_auto_20190424_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='archivised_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 24, 11, 26, 30, 866037, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_used',
            field=models.DateField(default=datetime.datetime(2019, 4, 24, 11, 26, 30, 866037, tzinfo=utc)),
        ),
    ]
