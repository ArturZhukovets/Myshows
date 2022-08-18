from django import template
from movies.models import Category, Movie

"""Здесь регистрируются теги для шаблонов.
Для того, чтобы использовать теги, например, моделей в шаблоне html
Создаем функцию, которая возращает Объект модели и имя данной функции используем для включения модели в шаблон
Не забыть {% load name_of_tag %}
Есть возможность рендерить simple_tag И inclusion_teg"""


# Создаём экземпляр Library для регистрации template тега
register = template.Library()


@register.simple_tag()
def get_categories():
    """Создал и зарегистрировал шаблон с моделью всех категорий"""
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movies.html')
def get_last_movies(count=5):
    """
    Шаблон рендера всех последних добавленных фильмов
    Регистрируем тег и передаем в него тот шаблон, который мы хотим, чтобы этот тег рендерил
    """

    movies = Movie.objects.order_by("id")[:count]
    return {"last_movies": movies}
