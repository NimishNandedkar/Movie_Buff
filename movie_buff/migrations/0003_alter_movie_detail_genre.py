# Generated by Django 4.2.3 on 2023-08-28 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_buff', '0002_movie_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie_detail',
            name='genre',
            field=models.CharField(max_length=15),
        ),
    ]