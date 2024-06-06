from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage

from .models import Genre, Movie, Actor, Director, MovieActor
from .views import generate_movie_release_chart
import csv
import io


class MovieAPITests(TestCase):

    # This function is ran before the testcases
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

    def test_load_data_endpoint_get(self):
        response = self.client.get(reverse("load_data"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "upload_form.html")

    def test_load_data_endpoint_post_csv(self):
        # Using hardcoded csv data colocate the data near the test and avoid syncing issues
        csv_file = SimpleUploadedFile(
            "test.csv",
            b"title,year,director,genre,actors,avg_vote\nTest Movie 2,2021,Director 1,Drama,Actor 1,9.0",
        )
        response = self.client.post(reverse("load_data"), {"file": csv_file})
        self.assertEqual(response.status_code, 201)

        movie = Movie.objects.get(Title="Test Movie 2")
        self.assertEqual(movie.ReleaseYear, 2021)
        self.assertEqual(movie.Rating, 9.0)
        self.assertEqual(movie.Directors.first().Name, "Director 1")
        self.assertEqual(movie.Genres.first().Name, "Drama")
        self.assertEqual(movie.movieactor_set.first().ActorID.Name, "Actor 1")

