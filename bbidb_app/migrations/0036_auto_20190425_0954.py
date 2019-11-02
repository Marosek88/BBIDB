# Generated by Django 2.2 on 2019-04-25 08:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bbidb_app', '0035_auto_20190425_0816'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectcontactworks',
            options={'verbose_name_plural': 'projectcontactworks'},
        ),
        migrations.AlterField(
            model_name='company',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 25, 8, 54, 47, 401325, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 25, 8, 54, 47, 401325, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_used',
            field=models.DateField(default=datetime.datetime(2019, 4, 25, 8, 54, 47, 401325, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 25, 8, 54, 47, 401325, tzinfo=utc), null=True),
        ),
    ]