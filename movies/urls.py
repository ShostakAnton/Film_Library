from django.urls import path


from movies.views import *

urlpatterns = [
    path('', MoviesView.as_view()),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie-detail')
]