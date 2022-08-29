from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from django.views.generic.base import View
from .models import Movie, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm



class GenreYear:
    """
    Жанры и года фильмов
    Наследование этого класса дополняет get_context_data
    """

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year") # .values -> Qs [{'year': year},]  .values_list -> Qs []




class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    template_name = "movies/movie_list.html"    # Ищет по дефолту шаблон movie_list.html
    queryset = Movie.objects.filter(draft=False)

    # def get_context_data(self, *args, **kwargs):
    #     """Добавление категорий в словарь контекста."""
    #     context = super().get_context_data()
    #     context["categories"] = Category.objects.all()
    #     return context


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    template_name = "movies/movie_detail.html"
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context


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


class ActorView(GenreYear, DetailView):
    """Вывод информации об актёре"""
    model = Actor
    template_name = "movies/actor.html"
    slug_field = "name"  # slug from field name


class FilterMovieView(GenreYear, ListView):
    """
    Фильтр фильмов
    Логическое ИЛИ Q(item) | Q(item)
    Логическое И Q(item), Q(item)
    """

    def get_queryset(self):
        if 'year' in self.request.GET and 'genre' in self.request.GET:
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")),
                Q(genres__in=self.request.GET.getlist('genre')))

        elif 'year' in self.request.GET:
                queryset = Movie.objects.filter(year__in=self.request.GET.getlist("year"))
        elif 'genre' in self.request.GET:
                queryset = Movie.objects.filter(genres__in=self.request.GET.getlist("genre"))
        else:
            queryset = Movie.objects.all()

        return queryset

class AddStarRating(View):
    """Добавление рейтинга к фильму"""

    def get_client_ip(self, request):
        """В данном методе получаем ip клиента, который отправил запрос"""
        x_forwarder_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarder_for:
            ip = x_forwarder_for.split(',')[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")), # Поле из запроса
                defaults={"star_id": int(request.POST.get("star"))} # Поле которое хотим изменить
            )
            return redirect(form.Meta.model.get_absolute_url())
        else:
            return HttpResponse(status=400)




