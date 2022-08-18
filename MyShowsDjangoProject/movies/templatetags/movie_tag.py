from django import template
from movies.models import Category

"""Здесь регистрируются теги для шаблонов.
Для того, чтобы использовать теги, например, моделей в шаблоне html
Создаем функцию, которая возращает Объект модели и имя данной функции используем для включения модели в шаблон
Не забыть {% load name_of_tag %}"""


# Создаём экземпляр Library для регистрации template тега
register = template.Library()


@register.simple_tag()
def get_categories():
    """Создал и зарегистрировал шаблон с моделью категорий"""
    return Category.objects.all()
