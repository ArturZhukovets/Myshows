from django.shortcuts import render
from django.views.generic import ListView, DetailView

from django.views.generic.base import View
from .models import Movie



class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    template_name = "movies/movie_list.html"    # Ищет по дефолту шаблон movie_list.html
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(DetailView):
    """Полное описание фильма"""
    model = Movie
    template_name = "movies/movie_detail.html"
    slug_field = "url"
    # def get(self, request, slug):
    #     movie = Movie.objects.get(url=slug)
    #     return render(request, "movies/movie_detail.html", context={"movie":movie})
