from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Category"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Actor(models.Model):
    """Actors"""
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")


    def get_absolute_url(self):
        return reverse("actor_detail", kwargs={"slug": self.name})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актёры и режиссеры"
        verbose_name_plural = "Актёры и режиссеры"


class Genre(models.Model):
    """Genres"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Movie(models.Model):
    """Movies"""
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = models.TextField('Описание')
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2015)
    country = models.CharField('Страна', max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режиссер", related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name="актёры", related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premier = models.DateField("Премьера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="Указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField("Сборы в США", default=0, help_text="Указывать сумму в долларах")
    fees_in_world = models.PositiveIntegerField("Сборы в мире", default=0, help_text="Указывать сумму в долларах")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)

    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Черновой вариант", default=False)

    def __str__(self):
        return self.title


    def get_parent_review(self):
        """Возвращает set элементов, у которых отсутствуют родительские эл.
        Т.е возвращает родительские комментарии, а не ответные ком."""

        return self.reviews_set.filter(parent__isnull=True)


    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug":self.url})

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    """Photo stills from the movie"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movie_shorts/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField("Значение", default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг, который добавил пользователь с определённым ip"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Reviews"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Отзыв", max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм")

    def __str__(self):
        return f"{self.name} - {self.movie} | {self.email}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

