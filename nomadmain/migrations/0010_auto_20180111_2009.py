# Generated by Django 2.0 on 2018-01-11 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomadmain', '0009_auto_20180111_1950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='image',
        ),
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ManyToManyField(to='nomadmain.Media'),
        ),
    ]
