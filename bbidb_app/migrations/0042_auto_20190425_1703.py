# Generated by Django 2.2 on 2019-04-25 16:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bbidb_app', '0041_auto_20190425_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectcontact',
            name='email_attachment1',
        ),
        migrations.RemoveField(
            model_name='projectcontact',
            name='email_attachment_category_specific',
        ),
        migrations.AddField(
            model_name='projectcontactworks',
            name='email_attachment_message',
            field=models.TextField(blank=True, default='Please see an extract from BoQ and other documents relevant to your works in a link below:', null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 25, 16, 3, 57, 326436, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 25, 16, 3, 57, 328430, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_used',
            field=models.DateField(default=datetime.datetime(2019, 4, 25, 16, 3, 57, 328430, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 4, 25, 16, 3, 57, 329427, tzinfo=utc), null=True),
        ),
    ]
