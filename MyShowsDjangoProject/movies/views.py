from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from django.views.generic.base import View
from .models import Movie
from .forms import ReviewForm


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


class AddReviews(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)      # todo Приостановить сохранение формы (разобраться как с этим работать)
            if request.POST.get("parent", None):  # None - обязательно, чтобы не отвалиться с ошибкой):
                form.parent_id = int(request.POST.get("parent"))
            # form.movie_id = pk      # В бд поле movie записано как movie.id
            form.movie = movie      # Здесь хранится объект фильма, который помещается в поле Reviews.movie
            form.save()

        return redirect(movie.get_absolute_url())

