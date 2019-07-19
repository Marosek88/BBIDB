# Generated by Django 2.2 on 2019-04-25 07:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bbidb_app', '0033_auto_20190424_1248'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectcontactworks',
            old_name='name',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='company',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 25, 7, 15, 11, 878709, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 25, 7, 15, 11, 894142, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_used',
            field=models.DateField(default=datetime.datetime(2019, 4, 25, 7, 15, 11, 894142, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 25, 7, 15, 11, 894142, tzinfo=utc), null=True),
        ),
    ]
