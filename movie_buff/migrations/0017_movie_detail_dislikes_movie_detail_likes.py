# Generated by Django 4.2.3 on 2023-10-20 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_buff', '0016_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie_detail',
            name='dislikes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie_detail',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]