from django.urls import path

from movies.views import *

urlpatterns = [
    path('', MoviesView.as_view()),
    path("filter/", FilterMoviesView.as_view(), name='filter'),
    path("add-rating/", AddStarRating.as_view(), name='add_rating'),
    path("json-filter/", JsonFilterMoviesView.as_view(), name='json_filter'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie-detail'),
    path("review/<int:pk>/", AddReview.as_view(), name="add_review"),
    # path("actor/<slug:slug>/", ActorView.as_view(), name="actor_detail"),
    path("actor/<str:slug>/", ActorView.as_view(), name="actor_detail"),
]
