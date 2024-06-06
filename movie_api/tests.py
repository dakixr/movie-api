from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage

from .models import Genre, Movie, Actor, Director, MovieActor
from .views import generate_movie_release_chart
import csv
import io


class MovieAPITests(TestCase):

    def setUp(self):
        self.client = Client()
        self.movie = Movie.objects.create(
            Title="Test Movie", ReleaseYear=2020, Rating=8.5
        )
        self.director = Director.objects.create(Name="Test Director")
        self.actor = Actor.objects.create(Name="Test Actor")
        self.genre = Genre.objects.create(Name="Action")
        self.movie.Directors.add(self.director)
        self.movie.Genres.add(self.genre)
        MovieActor.objects.create(MovieID=self.movie, ActorID=self.actor)