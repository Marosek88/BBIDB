# Generated by Django 2.2 on 2019-04-29 16:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bbidb_app', '0048_auto_20190429_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 29, 16, 10, 57, 263118, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='added_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 29, 16, 10, 57, 263118, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_used',
            field=models.DateField(default=datetime.datetime(2019, 4, 29, 16, 10, 57, 263118, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='contact',
            name='role',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='surname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='updated_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 29, 16, 10, 57, 263118, tzinfo=utc), null=True),
        ),
    ]
