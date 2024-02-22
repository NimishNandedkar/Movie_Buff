# Generated by Django 4.2.3 on 2023-08-28 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_buff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='movie_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_name', models.CharField(max_length=50)),
                ('genre', models.CharField(max_length=10)),
                ('desc', models.CharField(max_length=100)),
                ('poster', models.ImageField(upload_to='movie_buff/posters')),
                ('video', models.FileField(upload_to='movie_buff/videos')),
            ],
        ),
    ]
