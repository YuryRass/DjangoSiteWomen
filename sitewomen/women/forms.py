from typing import Any
from django import forms
from django.utils.deconstruct import deconstructible
from .models import Category, Husband, Women


@deconstructible
class RussianValidator:
    code = "russian"
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '

    def __init__(self, message: str | None = None) -> None:
        self.message = (
            message
            if message
            else "Должны присутствовать только русские символы, дефис и пробел."
        )

    def __call__(self, value: str, *args: Any, **kwds: Any) -> Any:
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise forms.ValidationError(self.message, self.code)


class AddPostForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        min_length=5,
        widget=forms.TextInput(attrs={"class": "form-input"}),
        label="Заголовок",
        validators=[RussianValidator()],
        error_messages={
            "min_length": "Слишком короткое название (min = 5 символов)",
        },
    )
    slug = forms.SlugField(
        max_length=255,
        label="URL",
        error_messages={
            "required": "Данное поле обязательное для заполнения",
        },
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={"cols": 70, "rows": 20}),
        required=False,
        label="Контент",
    )
    is_published = forms.BooleanField(required=False, label="Статус", initial=True)
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категории",
        empty_label="Категория не выбрана",
    )
    husband = forms.ModelChoiceField(
        queryset=Husband.objects.all(),
        required=False,
        label="Муж",
        empty_label="Не замужем",
    )

    def clean_husband(self):
        current_husband = self.cleaned_data.get('husband')

        if current_husband and Women.objects.filter(husband=current_husband).exists():
            raise forms.ValidationError(f"{current_husband} - уже занят другой женщиной")
        return current_husband
