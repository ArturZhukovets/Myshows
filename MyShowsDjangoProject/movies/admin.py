from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import Category, Movie, MovieShots, Actor, Genre, Rating, RatingStar, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    """Форма для написания описания в админке
    Взята из приложения ckeditor"""
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'



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
    actions = ("publish", "unpublish") # Добавляем 2 действия pub / unpub
    form = MovieAdminForm
    inlines = [ReviewInline] # Передаём классы, которые хотим прикрепить
    save_on_top = True  # Разместить кнопки сохранения и изменения вверху страницы
    save_as = True # Добавляет возможность в случае редактирования сохранять как новый объект
    list_editable = ("draft", "category") # Поля можно редактировать прямо из списка
    readonly_fields = ("get_image",)
    # Здесь группировка полей в нужном порядке в качестве первого аргумента кортежа будет выступать название поля
    fieldsets = (
        (None, {
            "fields":(('title', 'tagline'), )
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
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
            "fields":("url", "draft")
        })

    )

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.poster.url}" width="150" height="210"')


    def unpublish(self, request, queryset):
        """Добавление Action. Снимает публикации у записей."""
        row_update = queryset.update(draft=True)
        message_bit = f"{row_update} записей было обновлено"
        self.message_user(request, message_bit)

    def publish(self, request, queryset):
        """Добавление Action. Публикует выбранные записи."""
        row_update = queryset.update(draft=False)
        message_bit = f"{row_update} записей было обновлено"
        self.message_user(request, f"{message_bit}")




    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', ) # Права пользователя в админке допускают изменения
    unpublish.short_description = "Снять с публикации"
    get_image.short_description = 'Постер' # Поменять имя отображения в админке


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
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj:Actor):
        """Возвращает путь к изображению в виде тега. Добавляем данный метод в list_display"""
        # Вернет в html формате (как тег) указанный путь.
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ('movie', 'ip')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj:MovieShots):
        # Вернет в html формате (как тег) указанный путь.
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="60"')

    get_image.short_description = 'Изображение'

admin.site.register(RatingStar)
admin.site.site_title = "MyShows"
admin.site.site_header = "MyShows"
