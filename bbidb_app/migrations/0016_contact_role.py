# Generated by Django 2.2 on 2019-04-20 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbidb_app', '0015_auto_20190421_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='role',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]