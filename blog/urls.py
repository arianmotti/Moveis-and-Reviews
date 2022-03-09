from django.conf.urls.static import static
from django.urls import path

from tamrin1 import settings
from . import views

urlpatterns = [
    # path('get-movies/', views.get_movies, name='blog-get-movies'),
    # path('add-comment/', views.add_comment, name='blog-add-comment'),
    # path('get-comments/', views.get_comments, name='blog-get-comments'),
    path('home', views.home, name='blog-home'),
    path('comment/<int:movie_id>', views.add_comment),
    path('movies/<int:movie_id>/comments', views.get_comments)


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.BASE_DIR)
