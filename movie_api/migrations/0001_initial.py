# Generated by Django 5.0.6 on 2024-06-06 17:48

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('ActorID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=255)),
                ('BirthYear', models.IntegerField(null=True)),
                ('Nationality', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('DirectorID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=255)),
                ('BirthYear', models.IntegerField(null=True)),
                ('Nationality', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('GenreID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('MovieID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('Title', models.CharField(max_length=255)),
                ('ReleaseYear', models.IntegerField()),
                ('Rating', models.DecimalField(decimal_places=1, max_digits=3)),
                ('Directors', models.ManyToManyField(to='movie_api.director')),
                ('Genres', models.ManyToManyField(to='movie_api.genre')),
            ],
        ),
        migrations.CreateModel(
            name='MovieActor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ActorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_api.actor')),
                ('MovieID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_api.movie')),
            ],
            options={
                'unique_together': {('MovieID', 'ActorID')},
            },
        ),
    ]
