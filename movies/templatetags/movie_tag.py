from django import template
from movies.models import Category, Movie

register = template.Library()  # для регистрации template тегов


@register.simple_tag()  # регистрация ф-ции как темплейт тег
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movies.html')  # регистрация ф-ции как темплейт тег
# inclusion_tag - рендерит указаный шаблон
def get_last_movies(count=5):
    movies = Movie.objects.order_by("-id")[:count]
    return {"last_movies": movies}
