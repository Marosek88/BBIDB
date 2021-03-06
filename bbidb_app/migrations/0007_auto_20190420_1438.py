# Generated by Django 2.2 on 2019-04-20 13:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbidb_app', '0006_auto_20190414_1347'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='footer',
            new_name='email_notes',
        ),
        migrations.AddField(
            model_name='project',
            name='quotations_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_used',
            field=models.DateField(default=datetime.date(2019, 4, 20)),
        ),
    ]
