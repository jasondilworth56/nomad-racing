# Generated by Django 2.0 on 2018-01-12 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomadmain', '0017_article_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='slug',
            field=models.SlugField(blank=True, max_length=60),
        ),
    ]
