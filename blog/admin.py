from django.contrib import admin
from blog.models import Comment, Movie

# Register your models here.
admin.site.register(Comment)
admin.site.register(Movie)