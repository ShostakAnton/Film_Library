from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import *


# class MoviesView(View):
#     """Список фильмов"""
#
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, "movies/movie_list.html", {"movie_list": movies})

class MoviesView(ListView):
    """Список фильмов"""

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movie_list.html'


# class MovieDetailView(View):
#     """Полное описание фильма"""
#
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, 'movies/movie_detail.html', {'movie': movie})

class MovieDetailView(DetailView):
    """Полное описание фильма"""

    model = Movie
    slug_field = 'url'  # по какому полю искать запись
    template_name = 'movies/movie_detail.html'
