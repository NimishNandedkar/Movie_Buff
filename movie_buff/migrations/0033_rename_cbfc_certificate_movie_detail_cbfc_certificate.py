# Generated by Django 4.2.3 on 2023-10-22 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_buff', '0032_remove_movie_detail_test_genre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie_detail',
            old_name='cbfc_certificate',
            new_name='CBFC_certificate',
        ),
    ]