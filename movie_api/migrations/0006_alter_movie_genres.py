# Generated by Django 5.0.6 on 2024-06-06 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_api', '0005_alter_movie_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='Genres',
            field=models.ManyToManyField(to='movie_api.genre'),
        ),
    ]
