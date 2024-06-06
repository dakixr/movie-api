from django.db import models
import uuid

# Notes:

# Using UUIDs to not expose to the client the number of entries in each table
# the default id in django in an autoincrement BigInt 

# I am using camel case to fulfill the contract of the DB names
# In a normal project i would use snake-case for table columns names

class Genre(models.Model):
    GenreID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.Name

class Movie(models.Model):
    MovieID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Title = models.CharField(max_length=255)
    ReleaseYear = models.IntegerField()
    Director = models.ForeignKey('Director', on_delete=models.CASCADE)
    Genres = models.ManyToManyField(Genre)
    Rating = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return self.Title

class Actor(models.Model):
    ActorID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=255)
    BirthYear = models.IntegerField(null=True)
    Nationality = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.Name} {self.BirthYear}"

class Director(models.Model):
    DirectorID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=255)
    BirthYear = models.IntegerField(null=True)
    Nationality = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.Name

class MovieActor(models.Model):
    MovieID = models.ForeignKey(Movie, on_delete=models.CASCADE)
    ActorID = models.ForeignKey(Actor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('MovieID', 'ActorID')