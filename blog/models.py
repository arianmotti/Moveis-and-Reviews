from django.db import models


# Create your models here.
class Movie(models.Model):
    name = models.TextField()
    image = models.URLField()
    director = models.TextField()


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, related_name="comments")
    author = models.TextField(null=True)
    voice = models.FileField()
    text = models.TextField(null=True)
