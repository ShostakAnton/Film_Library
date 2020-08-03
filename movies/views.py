from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .forms import ReviewForm
from .models import *
from django.db.models import Q


class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):  # получение всех жанров
        return Genre.objects.all()

    def get_years(self):  # получение годов всех фильмов которые не в черновиках
        return Movie.objects.filter(draft=False).values("year")


# class MoviesView(View):
#     """Список фильмов"""
#
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, "movies/movie_list.html", {"movie_list": movies})

class MoviesView(GenreYear, ListView):
    """Список фильмов"""

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movie_list.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)     # получаем словарь
    #     context["categories"] = Category.objects.all()      # добавляем все категории в словарь
    #     return context


# class MovieDetailView(View):
#     """Полное описание фильма"""
#
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, 'movies/movie_detail.html', {'movie': movie})

class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""

    model = Movie
    slug_field = 'url'  # по какому полю искать запись
    template_name = 'movies/movie_detail.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)  # получаем словарь
    #     context["categories"] = Category.objects.all()  # добавляем все категории в словарь
    #     return context


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))  # присваиваем значение ключа parent
            # form.movie_id = pk       # присвоение id обьекта
            form.movie = movie  # присвоение обьекта
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации о актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        )
        return queryset
