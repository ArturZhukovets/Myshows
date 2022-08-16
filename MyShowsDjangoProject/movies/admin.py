from django.contrib import admin
from .models import Category, Movie, MovieShots, Actor, Genre, Rating, RatingStar, Reviews


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отобразить панель с указанными столбцами, зарегистрировать данный класс с помощью декоратора"""
    list_display = ('id', 'name', 'url')
    list_display_links = ("name",)  # Указать какие поля являются ссылками на категорию



class ReviewInline(admin.TabularInline):
    """Для того чтобы видеть список отзывов у указанного фильма"""
    model = Reviews
    extra = 1 # количество дополнительных полей
    readonly_fields = ('name', 'email')



@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Указывает поля в админ панели. Даёт возможность фильтрации по полям category, year.
    Возможность поиска по названию фильма или по категории"""
    list_display = ("title", "category", "url", "draft",)
    list_filter = ("category", "year")
    search_fields = ('title', 'category__name')
    inlines = [ReviewInline] # Передаём классы, которые хотим прикрепить
    save_on_top = True  # Разместить кнопки сохранения и изменения вверху страницы
    save_as = True # Добавляет возможность в случае редактирования сохранять как новый объект
    list_editable = ("draft", "category") # Поля можно редактировать прямо из списка
    # Здесь группировка полей в нужном порядке
    fieldsets = (
        (None, {
            "fields":(('title', 'tagline'), )
        }),
        (None, {
            "fields": ("description", "poster")
        }),
        (None, {
            "fields": (("year", "world_premier", "country"),)
        }),
        ("Актёры, режиссеры ", {
            "classes": ("collapse", ),   # Сворачивает поле
            "fields": (('actors', 'directors'), 'genres', 'category')
        }),
        ("Сборы", {
            "fields":(('fees_in_usa', 'fees_in_world'),)
        }),
        ("Options", {
            "fields":("url", "draft" )
        })

    )



@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы, поиск отзыва"""
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    search_fields = ('name',)
    readonly_fields = ('name', 'email')  # hide from editing


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ('name', 'description', 'url')

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актёры"""
    list_display = ('name', 'age', )

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ('movie', 'ip')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ('title', 'movie')


admin.site.register(RatingStar)
