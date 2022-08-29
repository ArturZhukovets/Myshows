from django import forms

from .models import Reviews, Rating, RatingStar


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""

    class Meta:
        model = Reviews
        fields = ("name", "email", "text", )



class RatingForm(forms.ModelForm):
    """
    Форма для заполнения рейтинга.
    Чтобы выводить список добавленных звёзд, переопределяю поле star.
    В queryset собраны все созданные звёзды
    """
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect, empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star", )

