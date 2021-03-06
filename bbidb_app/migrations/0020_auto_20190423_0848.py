# Generated by Django 2.2 on 2019-04-23 07:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbidb_app', '0019_category_archivised'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.date(2019, 4, 23), null=True),
        ),
        migrations.RemoveField(
            model_name='contact',
            name='category',
        ),
        migrations.AddField(
            model_name='contact',
            name='category',
            field=models.ManyToManyField(to='bbidb_app.Category'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_used',
            field=models.DateField(default=datetime.date(2019, 4, 23)),
        ),
    ]
