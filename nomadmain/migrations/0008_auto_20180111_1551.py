# Generated by Django 2.0 on 2018-01-11 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomadmain', '0007_auto_20180110_2159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teammember',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='last_name',
        ),
    ]
