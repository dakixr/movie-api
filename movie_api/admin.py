from django.contrib import admin
from movie_api.models import Actor, Director, Movie, MovieActor

# Register your models here.

admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(MovieActor)
