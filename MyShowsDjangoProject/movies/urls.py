from django.urls import path
from . import views


urlpatterns = [
    path("", views.MoviesView.as_view(), name='movie_list'),
    path("filter/", views.FilterMovieView.as_view(), name="filter_list"),
    path("add-rating/", views.AddStarRating.as_view(), name="add_rating"),

    path("<slug:slug>/", views.MovieDetailView.as_view(), name='movie_detail'),
    path("review/<int:pk>/", views.AddReviews.as_view(), name="add_review"),
    path("actor/<str:slug>", views.ActorView.as_view(), name="actor_detail"),

]
