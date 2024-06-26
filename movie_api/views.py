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
    chart_file = default_storage.open(chart_path, mode="rb")
    return FileResponse(chart_file)


# In a production environment all of the preprocessing would be done by a background worker
# To avoid long wait times
@csrf_exempt
def load_data_endpoint(request):
    if request.method == "GET":
        return render(request, "upload_form.html", {})

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

                # Fetch or create the movie without setting the genres yet
                rating = pd.to_numeric(
                    row["avg_vote"], errors="coerce"
                )  # Transform to None if value is non-numeric
                rating = rating if pd.notna(rating) else None
                movie, created = Movie.objects.get_or_create(
                    Title=row["title"],
                    Rating=rating,
                    ReleaseYear=row["year"],
                )

                # Parsing and adding the directors
                if isinstance(row["director"], str):
                    directors_names = [
                        director.strip() for director in row["director"].split(",")
                    ]

                    for director_name in directors_names:
                        director, created = Director.objects.get_or_create(
                            Name=director_name,
                            defaults={
                                "BirthYear": None,  # Assuming BirthYear is not available in the data
                                "Nationality": None,  # Assuming Nationality is not available in the data
                            },
                        )
                        movie.Directors.add(director)

                # Adding the genres
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
                                "Nationality": None,  # Assuming Nationality is not available in the data
                            },
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
    writer.writerow(
        ["Title", "Release Year", "Directors", "Genres", "Actors", "Rating"]
    )

    # Write each movie as a CSV row
    movies = Movie.objects.all()
    for movie in movies:
        title = movie.Title
        release_year = movie.ReleaseYear
        rating = movie.Rating

        # Get directors
        directors = ", ".join([director.Name for director in movie.Directors.all()])

        # Get genres
        genres = ", ".join([genre.Name for genre in movie.Genres.all()])

        # Get actors
        actors = ", ".join([ma.ActorID.Name for ma in movie.movieactor_set.all()])

        writer.writerow([title, release_year, directors, genres, actors, rating])

    return response


# Util Functions


def generate_movie_release_chart(movies):
    # Count the number of movies released each year
    release_years = [movie["ReleaseYear"] for movie in movies]
    year_counts = {year: release_years.count(year) for year in set(release_years)}

    # Prepare data for the bar chart
    years = sorted(year_counts.keys())
    counts = [year_counts[year] for year in years]

    # Generate the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(years, counts, color="skyblue", edgecolor="black")
    plt.xlabel("Release Year", fontsize=14, fontweight="bold")
    plt.ylabel("Number of Movies", fontsize=14, fontweight="bold")
    plt.title("Number of Movies Released Each Year", fontsize=16, fontweight="bold")
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    # Save the chart
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)

    chart_path = default_storage.save(f"charts/chart.png", buffer)
    return chart_path
