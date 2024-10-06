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


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label="Не замужем", label="Муж")

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'is_published', 'cat', 'husband', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }
        labels = {
            'slug': "URL"
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise forms.ValidationError('Длина превышает 50 символов')

        return title


class UploadFiles(forms.Form):
    file = forms.FileField(label="Файл")