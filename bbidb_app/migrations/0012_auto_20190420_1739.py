# Generated by Django 2.2 on 2019-04-20 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbidb_app', '0011_auto_20190420_1523'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectcontact',
            old_name='quick_message',
            new_name='email_personal_message',
        ),
        migrations.AddField(
            model_name='project',
            name='email_attachment2',
            field=models.TextField(blank=True, default='To see a full tender documentation, please visit the link below:', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='email_attachment_full',
            field=models.TextField(blank=True, default='-- PASTE LINK FOR FULL TENDER DOCS --', null=True),
        ),
        migrations.AddField(
            model_name='projectcontact',
            name='email_attachment1',
            field=models.TextField(blank=True, default='Please see an extract from BoQ and other documents relevant to your works in a link below:', null=True),
        ),
        migrations.AddField(
            model_name='projectcontact',
            name='email_attachment_category_specific',
            field=models.TextField(blank=True, default='-- PASTE WORKS SPECIFIC DOCS LINK HERE --', null=True),
        ),
    ]
