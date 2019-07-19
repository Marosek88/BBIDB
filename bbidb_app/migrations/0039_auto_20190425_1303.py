# Generated by Django 2.2 on 2019-04-25 12:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bbidb_app', '0038_auto_20190425_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcontact',
            name='will_price_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 25, 12, 3, 26, 588494, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 25, 12, 3, 26, 588494, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_used',
            field=models.DateField(default=datetime.datetime(2019, 4, 25, 12, 3, 26, 588494, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 25, 12, 3, 26, 588494, tzinfo=utc), null=True),
        ),
    ]
