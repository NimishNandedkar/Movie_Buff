# Generated by Django 4.2.3 on 2023-10-19 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_buff', '0014_userprofile_gender_userprofile_viewing_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='viewing_history',
        ),
    ]