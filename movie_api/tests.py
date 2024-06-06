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

    def test_export_data(self):
        response = self.client.get(reverse("export_data"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Disposition"], "attachment; filename=movies.csv"
        )

        content = response.content.decode("utf-8")
        reader = csv.reader(io.StringIO(content))
        header = next(reader)
        self.assertEqual(
            header, ["Title", "Release Year", "Directors", "Genres", "Actors", "Rating"]
        )
        row = next(reader)
        self.assertEqual(
            row, ["Test Movie", "2020", "Test Director", "Action", "Test Actor", "8.5"]
        )
