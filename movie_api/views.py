from django.shortcuts import render
import matplotlib
import pandas as pd
import io
import csv

import matplotlib.pyplot as plt

matplotlib.use("Agg")

from django.http import HttpResponse, FileResponse
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt

from .models import Genre, Movie, Actor, Director, MovieActor
from .models import Movie

# Views


def graph_endpoint(request):
    movies = list(Movie.objects.values("Title", "ReleaseYear"))
    chart_path = generate_movie_release_chart(movies)
    chart_file = open(chart_path, mode="rb")
    return FileResponse(chart_file)


def load_data_endpoint(request):

    if request.method == "GET":
        return render(request, 'upload_form.html', {})

    # Treat user uploaded data
    if request.method == "POST":

        uploaded_file = request.FILES["file"]
        file_name = uploaded_file.name
        file_path = default_storage.save(uploaded_file.name, uploaded_file)

        try:
            if file_name.endswith(".csv"):
                data = pd.read_csv(default_storage.open(file_path))
            elif file_name.endswith(".xlsx"):
                data = pd.read_excel(default_storage.open(file_path))
            else:
                return HttpResponse(f"Unsupported file format: {file_name}", status=400)

            # Parsing and saving data to the database
            for _, row in data.iterrows():
                director_name = row["director"]
                director, created = Director.objects.get_or_create(
                    Name=director_name,
                    defaults={
                        "BirthYear": None,  # Assuming BirthYear is not available in the data
                        "Nationality": None  # Assuming Nationality is not available in the data
                    }
                )


                # Fetch or create the movie without setting the genres yet
                movie, created = Movie.objects.get_or_create(
                    Title=row["title"],
                    ReleaseYear=row["year"],
                    Director=director,
                    Rating=row["avg_vote"],
                )
                
                if isinstance(row["genre"], str):
                    # Split the genres by comma and strip any extra whitespace
                    genres_list = [genre.strip() for genre in row["genre"].split(",")]

                    # Clear existing genres if the movie was already present
                    if not created:
                        movie.Genres.clear()

                    # Fetch or create each genre and add it to the movie
                    for genre_name in genres_list:
                        genre, _ = Genre.objects.get_or_create(Name=genre_name)
                        movie.Genres.add(genre)

                if isinstance(row["actors"], str):
                    actors_list = row["actors"].split(", ")
                    for actor_name in actors_list:
                        actor, created = Actor.objects.get_or_create(
                            Name=actor_name,
                            defaults={
                                "BirthYear": None,  # Assuming BirthYear is not available in the data
                                "Nationality": None  # Assuming Nationality is not available in the data
                            }
                        )
                        MovieActor.objects.get_or_create(MovieID=movie, ActorID=actor)

            return HttpResponse("Data loaded successfully", status=201)

        except Exception as e:
            return HttpResponse(f"Error when uploading the file: {e}", status=500)

    return HttpResponse("Invalid HTTP Method", status=400)


def export_data(request):
    # Set the response headers to indicate a CSV file download
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=movies.csv"

    # Create a CSV writer in memory
    writer = csv.writer(response)
    writer.writerow(["Title", "Release Year"])

    # Write each movie as a CSV row
    movies = list(Movie.objects.values("Title", "ReleaseYear"))
    for movie in movies:
        writer.writerow([movie["Title"], movie["ReleaseYear"]])

    return response


# Util Functions


def generate_movie_release_chart(movies):
    # Count the number of movies released each year
    release_years = [movie["ReleaseYear"] for movie in movies]
    year_counts = {year: release_years.count(year) for year in set(release_years)}

    # Prepare data for the bar chart
    years = list(year_counts.keys())
    counts = list(year_counts.values())

    # Generate the bar chart
    plt.bar(years, counts)
    plt.xlabel("Release Year")
    plt.ylabel("Number of Movies")
    plt.title("Number of Movies Released Each Year")
    plt.xticks(rotation=45)

    # Save the chart
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)

    chart_path = default_storage.save(f"charts/chart", buffer)
    return chart_path
