# Generated by Django 2.0 on 2017-12-06 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.FileField(upload_to='')),
                ('content', models.TextField()),
                ('category', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('iRating', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('series', models.CharField(max_length=60)),
                ('circuit', models.CharField(max_length=128)),
                ('race_type', models.CharField(max_length=30)),
                ('start_pos', models.IntegerField()),
                ('finish_pos', models.IntegerField()),
                ('iRating_change', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('iRacing_number', models.CharField(max_length=10)),
                ('profile_photo', models.FileField(upload_to='')),
                ('date_of_birth', models.DateField()),
                ('biography', models.TextField()),
                ('twitch_channel', models.CharField(max_length=30)),
                ('youtube_channel', models.CharField(max_length=30)),
                ('personal_site', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='team_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomadmain.TeamMember'),
        ),
        migrations.AddField(
            model_name='progress',
            name='team_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomadmain.TeamMember'),
        ),
        migrations.AddField(
            model_name='media',
            name='team_members',
            field=models.ManyToManyField(to='nomadmain.TeamMember'),
        ),
        migrations.AddField(
            model_name='article',
            name='team_members',
            field=models.ManyToManyField(to='nomadmain.TeamMember'),
        ),
    ]