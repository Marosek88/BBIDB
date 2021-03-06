# Generated by Django 2.2 on 2019-04-23 11:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bbidb_app', '0026_auto_20190423_1247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectcontactworks',
            name='category',
        ),
        migrations.AddField(
            model_name='projectcontactworks',
            name='name',
            field=models.CharField(default='Works', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 23, 11, 50, 47, 894163, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_used',
            field=models.DateField(default=datetime.datetime(2019, 4, 23, 11, 50, 47, 894163, tzinfo=utc)),
        ),
    ]
