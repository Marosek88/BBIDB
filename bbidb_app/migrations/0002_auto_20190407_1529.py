# Generated by Django 2.2 on 2019-04-07 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bbidb_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbidb_app.Category'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbidb_app.Company'),
        ),
        migrations.AlterField(
            model_name='projectlist',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbidb_app.Contact'),
        ),
        migrations.AlterField(
            model_name='projectlist',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbidb_app.Project'),
        ),
    ]